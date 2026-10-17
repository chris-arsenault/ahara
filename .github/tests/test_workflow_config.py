"""Exercise the config script used by the shared workflow, without AWS calls."""

import json
import os
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / "workflows/ci.yml"


def configure(manifest, extra_env=None, cargo=False):
    workflow = yaml.safe_load(WORKFLOW.read_text())
    step = next(
        step
        for step in workflow["jobs"]["ci"]["steps"]
        if step.get("name") == "Read platform.yml"
    )
    script = step["run"].split("python3 << 'PYEOF'\n", 1)[1].rsplit("\nPYEOF", 1)[0]
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "platform.yml").write_text(yaml.safe_dump(manifest))
        if cargo:
            (root / "backend").mkdir()
            (root / "backend/Cargo.toml").write_text("[workspace]\nmembers = []\n")
        env = {
            "GITHUB_OUTPUT": str(root / "outputs"),
            "BROWSER_CONFIG": "{}",
            "TERRAFORM_PATTERNS_REF": "",
            "TERRAFORM_VARIABLES": "{}",
        }
        env.update(extra_env or {})
        previous = Path.cwd()
        try:
            os.chdir(root)
            with patch.dict(os.environ, env):
                exec(compile(script, str(WORKFLOW), "exec"), {})
            return dict(
                line.split("=", 1)
                for line in (root / "outputs").read_text().splitlines()
            )
        finally:
            os.chdir(previous)


class WorkflowConfigTests(unittest.TestCase):
    def test_terraform_variable_file_preserves_types_and_quoting(self):
        workflow = yaml.safe_load(WORKFLOW.read_text())
        step = next(
            step
            for step in workflow["jobs"]["ci"]["steps"]
            if step.get("name") == "Terraform deploy"
        )
        command = shlex.split(step["run"].splitlines()[0])
        with tempfile.TemporaryDirectory() as temporary:
            for values in ({}, {"hostname": 'quoted"value', "schedule_enabled": False}):
                with patch.dict(
                    os.environ,
                    {
                        "RUNNER_TEMP": temporary,
                        "TERRAFORM_VARIABLES": json.dumps(values),
                    },
                ):
                    exec(compile(command[2], str(WORKFLOW), "exec"), {})
                self.assertEqual(
                    json.loads((Path(temporary) / "ahara.tfvars.json").read_text()),
                    values,
                )

    def test_existing_python_consumer_keeps_backend_src_defaults(self):
        output = configure({"project": "existing", "stack": ["python"]}, cargo=True)
        self.assertEqual(output["python_dir"], "backend")
        self.assertEqual(output["python_source_dir"], "src/")
        self.assertEqual(output["has_python"], "true")

    def test_non_python_consumer_stays_disabled(self):
        output = configure(
            {"project": "existing", "stack": ["typescript", "terraform"]}
        )
        self.assertEqual(output["has_python"], "false")

    def test_atlas_declares_its_actual_python_paths(self):
        output = configure(
            {
                "project": "atlas",
                "stack": ["python", "typescript", "terraform"],
                "python_dir": "tools/data",
                "python_source_dir": ".",
            },
            {
                "TERRAFORM_PATTERNS_REF": "a" * 40,
                "TERRAFORM_VARIABLES": json.dumps(
                    {"hostname": "atlas.ahara.io", "schedule_enabled": False}
                ),
            },
        )
        self.assertEqual(output["python_dir"], "tools/data")
        self.assertEqual(output["python_source_dir"], ".")
        self.assertEqual(output["has_terraform"], "true")

    def test_mutable_module_reference_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "commit SHA"):
            configure({"project": "atlas"}, {"TERRAFORM_PATTERNS_REF": "main"})

    def test_non_object_terraform_variables_are_rejected(self):
        with self.assertRaisesRegex(SystemExit, "JSON object"):
            configure({"project": "atlas"}, {"TERRAFORM_VARIABLES": "[]"})

    def test_malformed_terraform_variables_are_rejected(self):
        with self.assertRaises(json.JSONDecodeError):
            configure({"project": "atlas"}, {"TERRAFORM_VARIABLES": "not json"})


if __name__ == "__main__":
    unittest.main()
