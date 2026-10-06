import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "env_template_audit.py"


class CommandLineTests(unittest.TestCase):
    def test_json_mode_reports_drift_without_printing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / ".env.example"
            env = root / ".env"
            template.write_text("API_TOKEN=\nREGION=\n", encoding="utf-8")
            env.write_text("API_TOKEN=super-secret\nDEBUG=true\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(template), str(env), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "env_duplicates": [],
                "extra": ["DEBUG"],
                "missing": ["REGION"],
                "template_duplicates": [],
            },
        )
        self.assertNotIn("super-secret", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
