import argparse
import json
from pathlib import Path
from agent_eval.experiment_runner.runner import run_experiment
from agent_eval.results_interface.summary import load_records, summarize

def main():
    parser = argparse.ArgumentParser(description="Agent policy evaluation scaffold")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Run offline smoke fixtures")
    run.add_argument("--tasks", type=Path, default=Path("data/tasks/demo.jsonl"))
    run.add_argument("--configs", type=Path, default=Path("configs/demo.json"))
    run.add_argument("--corpus", type=Path, default=Path("data/knowledge_base/demo.json"))
    run.add_argument("--output", type=Path, default=Path("runs"))
    run.add_argument("--repetitions", type=int, default=2)
    run.add_argument("--seed", type=int, default=42)
    summary = commands.add_parser("summarize")
    summary.add_argument("records", type=Path)
    args = parser.parse_args()
    if args.command == "run":
        print(run_experiment(args.tasks, args.configs, args.corpus, args.output, args.repetitions, args.seed))
    else:
        print(json.dumps(summarize(load_records(args.records)), indent=2))

if __name__ == "__main__":
    main()
