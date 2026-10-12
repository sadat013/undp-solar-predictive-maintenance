# Portfolio summary

## Short title

Solar Site Predictive Maintenance Data Pipeline

## One-line description

Developing a data-quality and alarm-analysis workflow for multi-site solar predictive maintenance as part of my DENSYS master's Challenge-Based Module across semesters 2 and 3.

## Project summary

This is my Challenge-Based Module in the DENSYS master's programme, spanning semesters 2 and 3 and completed as a team project with the UNDP Information and Technology Management Green Energy Team. The project investigates how operational telemetry and alarm records can support preventive and predictive maintenance for decentralized solar PV, battery-storage, and hybrid systems. We assessed sparse maintenance labels, selected VRM alarms as practical proxy events, transformed long-format telemetry into site-level time series, and built a master table combining measurements, data-quality indicators, and alarm context. The latest project stage introduced a conservative five-check policy that fills only short, operationally plausible gaps and leaves long or suspicious outages missing. Predictive model training and validation are still pending, so the work is presented as a reproducible data-engineering and exploratory-analysis foundation rather than a completed AI product.

## Engineering challenge

Operational data is heterogeneous, incomplete, imbalanced across sites, and only indirectly labelled by alarms. The central challenge is to create trustworthy model inputs without hiding long outages or turning post-alarm behavior into false predictive evidence.

## Team contribution

The interim report lists Baleegha Fatima, Evelyn Ogbuka, and Md Atiq Aziz as team members. Replace the following placeholder before using this portfolio text:

`[Describe your own code, analysis, documentation, presentation, or coordination responsibilities.]`

## Tools and methods

- Python, pandas, NumPy, Matplotlib, Jupyter, nbformat, and nbclient
- time-series cleaning and UTC timestamp handling
- long-to-wide telemetry transformation
- alarm interval and event-onset matching
- missing-data auditing and constrained interpolation
- exploratory point-biserial correlation and quantile analysis
- reproducible notebooks and publication-safe repository packaging

## Achievement bullets

- Built a structured workflow for combining site-level solar telemetry with alarm intervals and exact alarm onsets.
- Documented a five-check interpolation policy that fills only short, operationally plausible gaps and preserves rejection reasons.
- Reported 963 accepted fills among 1,048 short gaps while retaining gaps longer than one day as missing.
- Quantified reporting, channel-availability, and alarm imbalance before model selection.
- Developed reusable per-site analyses and cross-site evidence ranking without presenting exploratory thresholds as validated rules.

## Verified or documented results

- 23 sites assessed for monitoring coverage.
- 12 sites selected for recent alarm/telemetry analysis.
- 97.4% of missing slots were in gaps longer than one day in the latest progress analysis.
- 5 sites accounted for 75% of alarm episodes in the latest progress analysis.

These are documented project results. Model performance metrics are not yet available.

## Skills demonstrated

Energy-systems data analysis, solar O&M, predictive-maintenance framing, time-series engineering, missing-data governance, exploratory statistics, reproducibility, technical writing, and responsible handling of operational data.

## What I learned

`[Add a first-person reflection after confirming your individual contribution. Suggested theme: reliable predictive maintenance begins with trustworthy data definitions, not model complexity.]`

## Suggested visuals

- project workflow from raw telemetry and alarms to candidate early-warning evidence;
- anonymized weekly reporting-coverage heatmap;
- anonymized missing-gap duration distribution;
- five-check interpolation decision flow;
- sanitized alarm-onset parameter ranking; and
- roadmap from data preparation to validation.

## Suggested GitHub topics

`predictive-maintenance`, `solar-energy`, `photovoltaics`, `battery-storage`, `time-series`, `data-quality`, `anomaly-detection`, `python`, `jupyter`, `energy-systems`

## CV bullet

Developed a Python/Jupyter pipeline that integrates multi-site solar telemetry with alarm events, audits missingness and site heterogeneity, and applies conservative short-gap interpolation as the data foundation for predictive-maintenance modelling.

## LinkedIn project description

As part of my DENSYS master's Challenge-Based Module across semesters 2 and 3, I am contributing to a team project with UNDP on predictive maintenance for decentralized solar and battery systems. The workflow cleans and restructures VRM telemetry, aligns alarm events with operating data, audits coverage and missingness, and applies a conservative five-check rule for short-gap interpolation. Current work focuses on defining prediction windows and alarm classes before training interpretable time-aware models.
