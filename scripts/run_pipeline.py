"""Execute the private-data notebook pipeline without modifying public notebooks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat
import pandas as pd
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
WORK_DIR = ROOT / "work" / "notebooks"
CONFIG_PATH = ROOT / "config" / "sites.csv"
TEMPLATE_PATH = NOTEBOOK_DIR / "04_site_alarm_parameter_analysis_template.ipynb"

PREPARATION_NOTEBOOKS = [
    NOTEBOOK_DIR / "01_prepare_telemetry.ipynb",
    NOTEBOOK_DIR / "02_prepare_alarm_logs.ipynb",
    NOTEBOOK_DIR / "03_match_alarms_to_telemetry.ipynb",
]

SUMMARY_NOTEBOOKS = [
    NOTEBOOK_DIR / "05_aggregate_results.ipynb",
    NOTEBOOK_DIR / "06_score_alarm_onset_evidence.ipynb",
]


def validate_inputs() -> pd.DataFrame:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "Copy config/sites.example.csv to config/sites.csv and add authorized site identifiers."
        )

    required_inputs = [
        ROOT / "data" / "raw" / "site_stats_part1.csv",
        ROOT / "data" / "raw" / "site_stats_part2.csv",
        ROOT / "data" / "raw" / "site_stats_part3.csv",
        ROOT / "data" / "raw" / "vrm_alarm_logs_clean.csv",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_inputs if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing private input files: " + ", ".join(missing))

    sites = pd.read_csv(CONFIG_PATH)
    expected_columns = {"site_id", "site_name"}
    if not expected_columns.issubset(sites.columns):
        raise ValueError("config/sites.csv must contain site_id and site_name columns")
    if sites.empty:
        raise ValueError("config/sites.csv contains no sites")
    sites["site_id"] = pd.to_numeric(sites["site_id"], errors="raise").astype(int)
    if sites["site_id"].duplicated().any():
        raise ValueError("config/sites.csv contains duplicate site_id values")
    return sites


def execute_notebook(notebook: nbformat.NotebookNode, output_path: Path) -> None:
    client = NotebookClient(
        notebook,
        timeout=1200,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(ROOT)}},
    )
    client.execute()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, output_path)


def execute_file(source_path: Path, output_path: Path) -> None:
    print(f"Executing {source_path.relative_to(ROOT)}")
    notebook = nbformat.read(source_path, as_version=4)
    execute_notebook(notebook, output_path)


def site_notebook(site_id: int, site_name: str) -> nbformat.NotebookNode:
    notebook = nbformat.read(TEMPLATE_PATH, as_version=4)
    id_replacements = 0
    name_replacements = 0

    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        cell.source, count = re.subn(
            r"^SITE_ID\s*=\s*\d+\s*$",
            f"SITE_ID = {site_id}",
            cell.source,
            count=1,
            flags=re.MULTILINE,
        )
        id_replacements += count
        cell.source, count = re.subn(
            r'^SITE_NAME\s*=\s*["\'].*?["\']\s*$',
            f"SITE_NAME = {site_name!r}",
            cell.source,
            count=1,
            flags=re.MULTILINE,
        )
        name_replacements += count

    if id_replacements != 1 or name_replacements != 1:
        raise RuntimeError(
            "The site-analysis template must contain one SITE_ID and one SITE_NAME assignment."
        )
    return notebook


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preparation-only",
        action="store_true",
        help="Run notebooks 01-03 and stop before per-site analysis.",
    )
    args = parser.parse_args()

    sites = validate_inputs()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "processed").mkdir(parents=True, exist_ok=True)
    (ROOT / "results").mkdir(parents=True, exist_ok=True)

    for path in PREPARATION_NOTEBOOKS:
        execute_file(path, WORK_DIR / f"executed_{path.name}")

    if args.preparation_only:
        print("Preparation completed.")
        return

    for row in sites.itertuples(index=False):
        notebook = site_notebook(int(row.site_id), str(row.site_name))
        output = WORK_DIR / f"site_{int(row.site_id)}_alarm_parameter_analysis.ipynb"
        print(f"Executing site analysis for {int(row.site_id)}")
        execute_notebook(notebook, output)

    for path in SUMMARY_NOTEBOOKS:
        execute_file(path, WORK_DIR / f"executed_{path.name}")

    print("Pipeline completed. Generated data and results remain outside Git tracking.")


if __name__ == "__main__":
    main()
