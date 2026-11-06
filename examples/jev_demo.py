"""Try Jev as a decision controller on three synthetic RNA benchmark tasks."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter

from agent_eval.controllers.rules import RuleController
from agent_eval.tool_gateway.rna import metrics, validate


ENDPOINT = "https://thejevai.com/v1/systemone"
TASKS = Path(__file__).resolve().parents[1] / "data/tasks/demo.jsonl"
EXPECTED_ROUTES = {
    "rna-partial": "rna_metrics",
    "lab-convention": "retrieve_protocol",
    "unrelated-crm": "out_of_scope",
}
QUESTIONS = {
    "in_scope": {
        "type": "noul",
        "instructions": (
            "Is the user's request about structural RNA research or work "
            "directly supporting it?"
        ),
    },
    "route": {
        "type": "choice",
        "instructions": "What should a structural RNA research assistant do next?",
        "criteria": {
            "rna_metrics": "Compute base-pair metrics from supplied structures.",
            "retrieve_protocol": "Look up a lab-specific protocol needed by the request.",
            "out_of_scope": "Decline unrelated work outside structural RNA research.",
            "clarify": "Ask for missing inputs or clarify an ambiguous request.",
        },
    },
}


def evaluate(payload, api_key):
    if "\r" in api_key or "\n" in api_key:
        raise RuntimeError("JEV_API_KEY must be a single line.")

    # Pass the credential on stdin so it does not appear in the command line.
    headers = f"Authorization: Bearer {api_key}\nContent-Type: application/json\n"
    start = perf_counter()
    try:
        response = subprocess.run(
            [
                "curl", "-q", "--silent", "--show-error", "--max-time", "30",
                "--request", "POST", "--header", "@-",
                "--data", json.dumps(payload),
                "--write-out", "\n%{http_code} %{content_type}", ENDPOINT,
            ],
            input=headers.encode("utf-8"),
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("The live demo requires curl on your PATH.") from None
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"curl could not complete the request (exit {error.returncode}).") from None

    wall_ms = round((perf_counter() - start) * 1000)
    raw_body, _, metadata = response.stdout.rpartition(b"\n")
    status, _, content_type = metadata.partition(b" ")
    if not status.startswith(b"2"):
        hint = {
            b"401": " Check that JEV_API_KEY was issued for this endpoint.",
            b"402": " Check the account credit balance.",
            b"403": " The request was refused. Compare the demo payload with a known-good request.",
            b"429": " Wait before rerunning the demo.",
        }.get(status, "")
        if content_type.lower().startswith(b"text/html"):
            hint += " The response was HTML."
        raise RuntimeError(f"Jev returned HTTP {status.decode('ascii')}.{hint}")

    try:
        body = json.loads(raw_body)
        if body["code"] != 0:
            raise RuntimeError("Jev returned an API error in the response envelope.")
        data = body["data"]
        answers = data["result"]["answers"]
        if answers["in_scope"]["type"] != "noul" or answers["route"]["type"] != "choice":
            raise ValueError("Unexpected Jev answer types")
        if answers["route"]["choice"] not in QUESTIONS["route"]["criteria"]:
            raise ValueError("Unexpected Jev route")
        return data, wall_ms
    except (KeyError, TypeError, ValueError):
        raise RuntimeError("Jev returned an unexpected response format.") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=EXPECTED_ROUTES, help="Run only this case.")
    parser.add_argument("--model", default="typesafe/jev-1.14")
    parser.add_argument("--dry-run", action="store_true", help="Print requests without calling Jev.")
    args = parser.parse_args()

    api_key = os.environ.get("JEV_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        parser.error("export JEV_API_KEY in your shell before running the live demo.")

    tasks = {}
    with TASKS.open(encoding="utf-8") as source:
        for line in source:
            task = json.loads(line)
            tasks[task["id"]] = task

    rules = RuleController()
    for case in [args.case] if args.case else EXPECTED_ROUTES:
        task = tasks[case]
        payload = {
            "model": args.model,
            "state": {"request": task["prompt"], "inputs": task["payload"]},
            "questions": QUESTIONS,
        }
        report = {
            "case": case,
            "request": task["prompt"],
            "model": args.model,
            "expected": {"scope": task["expected_scope"], "route": EXPECTED_ROUTES[case]},
        }
        if args.dry_run:
            print(json.dumps({"case": case, "payload": payload}, indent=2))
            continue

        try:
            data, wall_ms = evaluate(payload, api_key)
        except RuntimeError as error:
            print(f"{case}: {error}", file=sys.stderr)
            return 1

        result = data["result"]
        report.update(
            rule_baseline={
                "scope": rules.scope(task["prompt"]),
                "needs_retrieval": rules.needs_retrieval(task["prompt"]),
            },
            jev=result["answers"],
            route_matches_expected=result["answers"]["route"]["choice"] == EXPECTED_ROUTES[case],
            usage=result.get("usage"),
            credits_used=data.get("creditsUsed"),
            provider_ms=result.get("elapsedMs"),
            wall_ms=wall_ms,
        )
        if case == "rna-partial":
            validate(task["payload"])
            report["local_metrics_oracle"] = metrics(**task["payload"])
        print(json.dumps(report, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
