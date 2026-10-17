import importlib.util
import itertools
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SPEC = importlib.util.spec_from_file_location(
    "browser_config", Path(__file__).with_name("config.py")
)
CONFIG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONFIG)


class BrowserConfigTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def project(self, manifest=None, scripts=None, directory="frontend"):
        (self.root / "platform.yml").write_text(
            yaml.safe_dump(manifest or {"stack": ["typescript"]})
        )
        package = self.root / directory / "package.json"
        package.parent.mkdir(parents=True, exist_ok=True)
        package.write_text(json.dumps({"scripts": scripts or {}}))

    def test_existing_non_browser_callers_skip_without_dependency_install(self):
        self.project(scripts={"test": "vitest run"})
        self.assertFalse(CONFIG.detect(self.root)["enabled"])
        (self.root / "platform.yml").write_text("stack: [rust, terraform]\n")
        self.assertFalse(CONFIG.detect(self.root)["enabled"])

    def test_discovers_scripts_and_defaults_without_playwright_config(self):
        self.project(
            scripts={
                "test:browser": "vitest run --project browser",
                "test:release": "vitest run --project release",
            }
        )
        config = CONFIG.detect(self.root)
        self.assertTrue(config["enabled"])
        self.assertEqual(config["runtime"], "container")
        self.assertTrue(config["release"])
        self.assertFalse(config["verify"])
        self.assertEqual(config["engines"], ["chromium", "firefox", "webkit"])
        self.assertEqual(
            config["artifact_paths"],
            "frontend/test-results/\nfrontend/playwright-report/",
        )

    def test_manifest_overrides_directory_engines_and_artifacts(self):
        self.project(
            {
                "stack": ["typescript"],
                "typescript_dir": "apps/web",
                "browser_tests": {
                    "engines": ["webkit"],
                    "artifacts": ["apps/web/results/"],
                },
            },
            {
                "test:browser": "playwright test",
                "test:browser:verify": "make native-check",
            },
            "apps/web",
        )
        config = CONFIG.detect(self.root)
        self.assertEqual(config["directory"], "apps/web")
        self.assertEqual(config["engines"], ["webkit"])
        self.assertTrue(config["verify"])
        self.assertFalse(config["release"])

    def test_autodetection_ignores_backend_and_installed_dependencies(self):
        self.project(scripts={"test:browser": "run-tests"}, directory="apps/web")
        self.project(scripts={}, directory="node_modules/unrelated")
        self.project(scripts={}, directory="backend")
        self.assertEqual(CONFIG.detect(self.root)["directory"], "apps/web")

    def test_root_package_is_supported(self):
        self.project(scripts={"test:browser": "run-tests"}, directory=".")
        self.assertEqual(CONFIG.detect(self.root)["directory"], ".")

    def test_action_outputs_preserve_multiline_artifact_paths(self):
        self.project(scripts={"test:browser": "run-tests"})
        output = self.root / "action-output"
        subprocess.run(
            [sys.executable, str(Path(__file__).with_name("config.py").resolve())],
            cwd=self.root,
            env={**os.environ, "GITHUB_OUTPUT": str(output)},
            check=True,
            capture_output=True,
        )
        values = dict(line.split("=", 1) for line in output.read_text().splitlines())
        self.assertEqual(values["enabled"], "true")
        config = json.loads(values["config"])
        self.assertEqual(config["artifact_paths"].splitlines(), config["artifacts"])

    def test_explicit_opt_out(self):
        self.project(
            {"stack": ["typescript"], "browser_tests": False},
            {"test:browser": "run-tests"},
        )
        self.assertFalse(CONFIG.detect(self.root)["enabled"])

    def test_host_runtime_is_explicit(self):
        self.project(
            {
                "stack": ["typescript"],
                "browser_tests": {"runtime": "host", "engines": ["chromium"]},
            },
            {"test:browser": "run-tests"},
        )
        self.assertEqual(CONFIG.detect(self.root)["runtime"], "host")

    def test_declared_capability_cannot_silently_skip_a_missing_script(self):
        self.project(
            {"stack": ["typescript"], "browser_tests": {"engines": ["chromium"]}}
        )
        with self.assertRaisesRegex(ValueError, "requires a test:browser"):
            CONFIG.detect(self.root)

    def test_bad_configuration_fails_detection(self):
        invalid = [
            {"engines": []},
            {"engines": ["chrome"]},
            {"engines": ["webkit", "webkit"]},
            {"engines": "chromium"},
            {"artifacts": []},
            {"artifacts": ["../private/"]},
            {"artifacts": ["/tmp/results"]},
            {"artifacts": ["results\n.env"]},
            {"enginies": ["chromium"]},
            {"runtime": "invalid"},
            "invalid",
        ]
        for settings in invalid:
            with self.subTest(settings=settings):
                self.project(
                    {"stack": ["typescript"], "browser_tests": settings},
                    {"test:browser": "run-tests"},
                )
                with self.assertRaises(ValueError):
                    CONFIG.detect(self.root)

    def test_directory_cannot_escape_checkout(self):
        self.project({"stack": ["typescript"], "typescript_dir": "../other"})
        with self.assertRaisesRegex(ValueError, "within the repository"):
            CONFIG.detect(self.root)


class DeploymentGateTests(unittest.TestCase):
    def test_ci_uses_the_same_package_as_browser_discovery(self):
        workflow = yaml.safe_load(
            (Path(__file__).parents[2] / "workflows/ci.yml").read_text()
        )
        step = next(
            s for s in workflow["jobs"]["ci"]["steps"] if s.get("id") == "config"
        )
        script = step["run"].split("python3 << 'PYEOF'\n", 1)[1].rsplit("\nPYEOF", 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "platform.yml").write_text(
                "project: example\nstack: [typescript]\n"
            )
            package = root / "backend-ui/package.json"
            package.parent.mkdir()
            package.write_text(json.dumps({"scripts": {"test:browser": "run-tests"}}))
            config = CONFIG.detect(root)
            output = root / "action-output"
            subprocess.run(
                [sys.executable, "-c", script],
                cwd=root,
                env={
                    **os.environ,
                    "GITHUB_OUTPUT": str(output),
                    "BROWSER_CONFIG": json.dumps(config),
                },
                check=True,
                capture_output=True,
            )
            values = dict(
                line.split("=", 1) for line in output.read_text().splitlines()
            )
            self.assertEqual(values["typescript_dir"], config["directory"])

    def test_only_success_or_explicit_absence_can_reach_deployment(self):
        workflow = yaml.safe_load(
            (Path(__file__).parents[2] / "workflows/ci.yml").read_text()
        )
        jobs = workflow["jobs"]
        self.assertEqual(set(jobs["ci"]["needs"]), {"browser-config", "browser"})
        self.assertEqual(jobs["browser"]["needs"], ["browser-config"])
        self.assertFalse(jobs["browser"]["strategy"]["fail-fast"])
        expression = jobs["ci"]["if"].removeprefix("${{").removesuffix("}}").strip()
        results = ["success", "failure", "skipped", "cancelled"]
        for enabled, detection, browser, cancelled in itertools.product(
            ["true", "false", ""], results, results, [False, True]
        ):
            replacements = {
                "needs.browser-config.outputs.enabled": repr(enabled),
                "needs.browser-config.result": repr(detection),
                "needs.browser.result": repr(browser),
                "!cancelled()": repr(not cancelled),
            }
            evaluated = expression
            for key, value in replacements.items():
                evaluated = evaluated.replace(key, value)
            evaluated = evaluated.replace("&&", "and").replace("||", "or")
            expected = (
                not cancelled
                and detection == "success"
                and (
                    (enabled == "true" and browser == "success")
                    or (enabled == "false" and browser == "skipped")
                )
            )
            with self.subTest(
                enabled=enabled,
                detection=detection,
                browser=browser,
                cancelled=cancelled,
            ):
                self.assertEqual(eval(f"({evaluated})", {"__builtins__": {}}), expected)


if __name__ == "__main__":
    unittest.main()
