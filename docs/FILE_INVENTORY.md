# Publication file inventory

## Private working directory audit

The supplied working directory contained more than 1 GB of material, including:

- Python scripts and Jupyter notebooks;
- raw and processed telemetry and alarm CSVs;
- site-specific analysis results and figures;
- Word reports, a PDF report, and progress presentations;
- copied shared-folder materials and reference papers;
- ZIP archives and duplicated datasets;
- generated document-render folders and caches; and
- legacy data-collection scripts containing hard-coded access tokens.

## Included in the public folder

| Public item | Source role | Publication treatment |
|---|---|---|
| `notebooks/01_prepare_telemetry.ipynb` | Long-to-wide telemetry preparation | Outputs removed; site IDs and paths sanitized. |
| `notebooks/02_prepare_alarm_logs.ipynb` | Alarm split and date coverage | Outputs removed; site IDs and paths sanitized. |
| `notebooks/03_match_alarms_to_telemetry.ipynb` | Alarm interval matching | Outputs removed; site IDs and paths sanitized. |
| `notebooks/04_site_alarm_parameter_analysis_template.ipynb` | Per-site association analysis | Reduced to a reusable sanitized template. |
| `notebooks/05_aggregate_results.ipynb` | Cross-site aggregation | Outputs removed and result path adapted. |
| `notebooks/06_score_alarm_onset_evidence.ipynb` | Exploratory evidence ranking | Outputs removed and result path adapted. |
| `scripts/run_pipeline.py` | Reproducible notebook orchestration | New public wrapper; does not collect remote data. |
| `scripts/verify_repository.py` | Publication safety and integrity checks | New. |
| Markdown documentation | Report and presentation context | Rewritten without site identities or partner data. |

## Excluded

- all raw and processed CSVs;
- all site-specific executed notebooks and result directories;
- VRM site identifiers and names;
- API collection scripts and credentials;
- internal reports, presentations, meetings, and shared-folder copies;
- ZIP archives and duplicate data folders;
- generated DOCX/PDF render assets;
- cached Python files and temporary outputs; and
- unrelated academic or reference material.

## Not found as a publishable source file

The 9 October 2026 presentation documents a stricter five-check interpolation policy and its results. A standalone implementation matching all five documented checks was not located in the supplied directory. The repository therefore records the methodology and result boundary but does not recreate or claim to verify that code.
