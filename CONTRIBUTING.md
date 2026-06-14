# Contributing

This repository treats detections like software. Changes flow through pull
requests and must pass automated validation before they merge.

## Workflow

1. Create a branch for your change.
2. Add or edit a Sigma rule under `rules/`, grouped by ATT&CK tactic.
3. Open a pull request. The CI pipeline validates syntax and converts the rule
   to KQL.
4. A reviewer checks the logic and false positive notes.
5. Once CI passes and the review is approved, the change merges to main.

## Rule requirements

Every rule must include:

- A descriptive `title` and a stable `id`.
- A `description` explaining what the rule catches.
- A `references` link to the relevant ATT&CK technique.
- `falsepositives` notes.
- A `level` and ATT&CK `tags`.

## Validate locally before opening a PR

```
pip install sigma-cli pysigma-backend-kusto
sigma check rules/
sigma convert -t kusto -p pipelines/sentinel.yml rules/
```

If both commands succeed, your rule is ready for review.
