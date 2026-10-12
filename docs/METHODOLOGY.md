# Methodology

## System boundary

The project studies remotely monitored decentralized solar PV, battery-storage, and hybrid energy systems. The current analytical boundary is the site level: telemetry describes aggregate energy flows and state variables rather than individual modules, strings, inverters, or battery cells.

## Data sources

### Maintenance records

The interim report describes 319 maintenance events from 117 sites, of which 219 included a cause. The records were useful for problem framing but too sparse and incomplete to support the main supervised-learning workflow.

### VRM alarm logs

Alarm events are used as proxy labels. This changes the prediction objective from confirmed failure prediction to identifying telemetry patterns associated with, or preceding, alarm activation.

### VRM telemetry

The primary predictors are site-level energy-flow measurements and battery state of charge when available. The usual interval is 15 minutes, but coverage and available channels differ by site.

## Data preparation

1. Parse all timestamps as UTC.
2. Normalize parameter codes, including case differences in grid-flow attributes.
3. Preserve true zero measurements.
4. Pivot long-format telemetry to one row per site and timestamp.
5. retain the union of channels while recording which channels are available at each site.
6. distinguish confirmed no-alarm rows from unknown alarm status.
7. repair alarm intervals cautiously when clear timestamps are missing or inconsistent.
8. attach active alarm intervals and exact onset information to telemetry.

## Five-check interpolation policy

The latest presentation defines a gap as eligible only when all conditions pass:

- duration is 30 minutes or less with observed values on both sides;
- no alarm is active, starts, or clears within 60 minutes;
- Total kWh at both edges is not unusually low for the corresponding hour;
- energy-flow and battery-level changes across the gap satisfy continuity checks; and
- no rejected gap lies within two hours.

Eligible values are linearly interpolated. Total kWh is reconstructed as the sum of directional flows rather than interpolated independently. Alarm columns are never modified. Long or rejected gaps remain missing, and the rejection reason is retained.

The supplied public notebooks contain the earlier data-preparation and alarm-association workflow. The exact latest five-check implementation was not located as a standalone source file and therefore has not been reconstructed here.

## Exploratory analysis

Per-site analysis separates:

- sampled alarm-active periods;
- exact alarm onsets mapped to the nearest telemetry row within 20 minutes;
- 15- and 60-minute pre-onset values; and
- non-alarm baseline periods.

The analysis calculates:

- point-biserial correlation with alarm-active status;
- baseline and alarm-onset medians;
- interquartile-range-normalized median shifts;
- proportions of alarm-onset values below baseline P10 or above baseline P90;
- alarm-rate lift across parameter quantiles; and
- alarm-class-specific summaries where enough events exist.

The exploratory onset evidence score is:

```text
E = min(|(median_alarm - median_baseline) / IQR_baseline|, 5)
    * ln(1 + n)
    * max(P_low, P_high)
```

where `n` is the number of mapped alarm-onset observations and `P_low` and `P_high` are the fractions below baseline P10 and above baseline P90. A candidate is promoted only when at least 10 mapped onset values are available.

This score is a ranking heuristic. It is not a probability, significance test, causal estimate, or manufacturer threshold.

## Planned modelling and validation

Candidate models include Logistic Regression, Decision Trees, Random Forest, gradient boosting, and forecasting-based anomaly detection. The final choice should follow data readiness rather than model complexity.

Validation should use time-aware splits. Classification metrics should include precision, recall, F1-score, and confusion matrices. Forecasting or regression approaches should report MAE, RMSE, and residual diagnostics. Interpolation should be tested by masking known values, reconstructing them, and measuring error before filled values are relied upon in modelling.
