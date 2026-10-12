# Data dictionary

## Raw telemetry files

Expected filename pattern: `data/raw/site_stats_part*.csv`

| Column | Type | Unit | Description |
|---|---|---|---|
| `site_id` | integer | - | Authorized site identifier. |
| `site_name` | string | - | Site label. Treat as private unless approved. |
| `attribute` | string | - | VRM parameter code. |
| `label` | string | - | Source parameter label. |
| `timestamp_utc` | datetime | UTC | Observation timestamp. |
| `value` | numeric | parameter-specific | Measured value. |

### Mapped attributes

| Attribute | Output column | Unit |
|---|---|---|
| `Pc` | Solar to Load | kWh |
| `Pb` | Solar to Battery | kWh |
| `Pg` | Solar to Grid | kWh |
| `Bc` | Battery to Load | kWh |
| `Bg` | Battery to Grid | kWh |
| `Gc` or source `gc` | Grid to Load | kWh |
| `Gb` or source `gb` | Grid to Battery | kWh |
| `kwh` | Total kWh | kWh |
| `bs` | Battery SoC | % |

Parameter availability differs by site. Units should be confirmed against the VRM export configuration before model development; directional energy fields are treated as interval energy in the current workflow.

## Cleaned alarm file

Expected filename: `data/raw/vrm_alarm_logs_clean.csv`

Required or used columns include:

| Column | Type | Unit | Description |
|---|---|---|---|
| `site_id` | integer | - | Site identifier matching telemetry. |
| `idAlarm` | string or integer | - | Alarm record identifier. |
| `alarm_started_at` | datetime | UTC | Alarm start. |
| `alarm_cleared_at` | datetime | UTC | Alarm clearance; may be missing. |
| `description` | string | - | Alarm description. |
| `device` | string | - | Reporting device class. |
| `classification` | string | - | Engineering alarm group. |
| `duration_seconds` | numeric | s | Alarm duration when available. |

Optional columns used in summaries include `site_name`, `isActive`, and `alarm_type`.

## Processed telemetry

The pipeline writes one row per site and UTC timestamp. Generated alarm fields include:

- `alarm_active`: 1 when a telemetry timestamp falls within an alarm interval;
- `alarm_overlap_count`: number of overlapping alarms;
- `alarm_idAlarm`, `alarm_description`, `alarm_device`, `alarm_classification`, and `alarm_duration_seconds`: unique alarm details joined for the interval; and
- `sampled_alarm_onset`: transition from inactive to active at sampled resolution.

## Missingness and quality fields

The latest documented master table also carries data-quality and alarm-status indicators. Blank alarm fields must not automatically be interpreted as missing data: confirmed inactive rows are `no_alarm`, while unresolved status remains `unknown`.
