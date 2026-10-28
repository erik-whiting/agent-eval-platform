import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from agent_eval.configuration_registry.registry import load_configs
from agent_eval.experiment_runner.runner import run_experiment
from agent_eval.task_registry.registry import load_tasks
from agent_eval.tool_gateway.gateway import ToolGateway
from agent_eval.tool_gateway.rna import tool, metrics, validate

ROOT = Path(__file__).resolve().parents[1]

class PlatformTests(unittest.TestCase):
    def test_metrics(self):
        self.assertAlmostEqual(metrics("(....)", "((..))")["f1"], 2/3)
        self.assertEqual(metrics("....", "....")["f1"], 1)
        self.assertEqual(metrics("....", "(..)")["f1"], 0)
        for bad in [{"predicted": "(()", "reference": "..."},
                    {"predicted": "[..]", "reference": "...."},
                    {"predicted": "..", "reference": "."}]:
            with self.assertRaises(ValueError):
                validate(bad)

    def test_gateway_cache_and_permissions(self):
        gateway = ToolGateway([tool()], True)
        args = {"predicted": "(..)", "reference": "(..)"}
        gateway.begin_task(["rna_metrics"], 3)
        result = gateway.call("rna_metrics", args)
        result["f1"] = -1
        self.assertEqual(gateway.call("rna_metrics", args)["f1"], 1)
        self.assertTrue(gateway.events[-1]["cache_hit"])
        gateway.begin_task([], 3, clear_cache=False)
        with self.assertRaises(PermissionError):
            gateway.call("rna_metrics", args)
        self.assertFalse(gateway.events[-1]["executed"])
        gateway.begin_task(["rna_metrics"], 1)
        gateway.call("rna_metrics", args)
        self.assertFalse(gateway.events[-1]["cache_hit"])
        with self.assertRaises(RuntimeError):
            gateway.call("rna_metrics", args)

    def test_agent_input_excludes_labels(self):
        task = load_tasks(ROOT / "data/tasks/demo.jsonl")[0]
        self.assertEqual(set(asdict(task.agent_input())), {"id", "prompt", "payload"})

    def test_unimplemented_config_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps([{"id": "bad", "version": "1", "controller": "jev"}]))
            with self.assertRaises(ValueError):
                load_configs(path)

    def test_experiment(self):
        with tempfile.TemporaryDirectory() as directory:
            output = run_experiment(ROOT / "data/tasks/demo.jsonl", ROOT / "configs/demo.json",
                                    ROOT / "data/knowledge_base/demo.json", Path(directory))
            records = [json.loads(line) for line in (output / "records.jsonl").read_text().splitlines()]
            self.assertEqual(len(records), 32)
            self.assertTrue(all(r["error"] is None for r in records))
            self.assertTrue(any(e["cache_hit"] for r in records for e in r["tool_events"]))
            baseline = [r for r in records if r["config_id"] == "baseline" and r["task_id"] == "lab-convention"]
            self.assertTrue(all(not r["scores"]["success"] for r in baseline))
            conditional = [r for r in records if r["config_id"] == "conditional_retrieval"]
            self.assertTrue(all(r["scores"]["success"] for r in conditional))
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(len(manifest["schedule"]), 32)
            self.assertTrue(manifest["source_hashes"])

if __name__ == "__main__":
    unittest.main()
