from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicationSafetyTests(unittest.TestCase):
    def test_repository_verifier(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "verify_repository.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_notebooks_are_unexecuted(self) -> None:
        notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
        self.assertEqual(len(notebooks), 6)
        for path in notebooks:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    self.assertEqual(cell.get("outputs", []), [], path.name)
                    self.assertIsNone(cell.get("execution_count"), path.name)

    def test_readme_marks_project_incomplete(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("work-in-progress", readme)
        self.assertIn("not yet complete", readme)
        self.assertIn("no open-source license", readme)


if __name__ == "__main__":
    unittest.main()
