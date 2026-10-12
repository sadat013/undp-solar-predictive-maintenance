# Contributing

This repository represents an academic project in progress.

Before proposing a change:

1. avoid committing private partner data, site identifiers, or credentials;
2. preserve UTC timestamps and documented units;
3. distinguish exploratory associations from validated prediction results;
4. do not change thresholds, aggregation rules, or alarm matching tolerances without documenting the reason and expected effect;
5. keep notebooks free of execution outputs before committing; and
6. run `python scripts/verify_repository.py` and `python -m unittest discover -s tests`.

Methodological changes that can affect results should be reviewed by the project team before merging.
