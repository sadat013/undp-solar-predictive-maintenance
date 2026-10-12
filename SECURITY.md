# Security and responsible disclosure

## Credentials

Never commit VRM access tokens, API keys, passwords, authorization headers, `.env` files, or exported credentials. Configure secrets through environment variables or an approved secret-management service.

The private working directory contained legacy scripts with hard-coded VRM access tokens. Those scripts and values are not included here. The affected tokens should be revoked or rotated before this repository is published, even if the scripts have never been pushed to GitHub.

## Operational data

Telemetry, alarm logs, maintenance tickets, site names, site identifiers, and timestamps may reveal operational information. Keep them outside Git unless the data owner provides explicit publication approval and an appropriate anonymization review has been completed.

## Reporting a problem

Before publication, replace this section with an approved security contact. Do not include sensitive evidence in a public issue.
