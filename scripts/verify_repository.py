"""Check the public repository for structural and publication-safety issues."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "__pycache__", "work"}
PRIVATE_OUTPUT_DIRS = {
    ROOT / "data" / "raw",
    ROOT / "data" / "processed",
    ROOT / "results",
}

REQUIRED = [
    ROOT / "README.md",
    ROOT / ".gitignore",
    ROOT / "requirements.txt",
    ROOT / "config" / "sites.example.csv",
    ROOT / "docs" / "PROJECT_STATUS.md",
    ROOT / "docs" / "METHODOLOGY.md",
    ROOT / "docs" / "DATA_DICTIONARY.md",
    ROOT / "docs" / "VERIFICATION.md",
    ROOT / "notebooks" / "01_prepare_telemetry.ipynb",
    ROOT / "notebooks" / "02_prepare_alarm_logs.ipynb",
    ROOT / "notebooks" / "03_match_alarms_to_telemetry.ipynb",
    ROOT / "notebooks" / "04_site_alarm_parameter_analysis_template.ipynb",
    ROOT / "notebooks" / "05_aggregate_results.ipynb",
    ROOT / "notebooks" / "06_score_alarm_onset_evidence.ipynb",
]

FORBIDDEN_TEXT_PATTERNS = {
    "absolute Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "hard-coded credential assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*=\s*[\"'][^\"']+[\"']",
        re.IGNORECASE,
    ),
    "private site naming convention": re.compile(
        r"GP\d+|STATE_HOSPITAL|KATOR|KUAJOK|RUMBEK|TORIT|YAMBIO|"
        r"IMPRESS_SAMOA|KIKAGATI|PINCHINAT|COG_FAO_CO|ZWE_UNDP_CO|"
        r"MRT_UNDP_CO|SLE_FAO_CO",
        re.IGNORECASE,
    ),
}


def public_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if any(parent == path or parent in path.parents for parent in PRIVATE_OUTPUT_DIRS):
            if path.name != "README.md":
                continue
        files.append(path)
    return files


def check_required(errors: list[str]) -> None:
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")


def check_notebooks(errors: list[str]) -> None:
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid notebook JSON in {path.name}: {exc}")
            continue
        for index, cell in enumerate(notebook.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            if cell.get("outputs"):
                errors.append(f"Notebook output present: {path.name} cell {index}")
            if cell.get("execution_count") is not None:
                errors.append(f"Execution count present: {path.name} cell {index}")
            source = "".join(cell.get("source", []))
            try:
                compile(source, f"{path.name}:cell_{index}", "exec")
            except SyntaxError as exc:
                errors.append(f"Notebook syntax error: {path.name} cell {index}: {exc}")


def check_scripts(errors: list[str]) -> None:
    for path in sorted((ROOT / "scripts").glob("*.py")):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            errors.append(f"Script syntax error: {path.name}: {exc}")


def check_text(errors: list[str]) -> None:
    text_suffixes = {".md", ".py", ".ipynb", ".txt", ".csv", ".yml", ".yaml"}
    for path in public_files():
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in text_suffixes and path.name not in {".gitignore", ".gitattributes"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Unexpected binary file in public text set: {path.relative_to(ROOT)}")
            continue
        for label, pattern in FORBIDDEN_TEXT_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} found in {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_notebooks(errors)
    check_scripts(errors)
    check_text(errors)

    if errors:
        print("Repository verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository verification passed.")
    print(f"Checked {len(public_files())} public files and 6 sanitized notebooks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
