# Restart-point study for failed LLM agent runs

Working question: when an LLM agent fails a task, how close to the true failure step
does a restart need to be for the repair to succeed, and what does each restart point cost?

Status: literature review (started 2026-11-11)

## Layout

- `research_log.md`  dated notes, one entry per working day
- `notes/`           one file per paper read
- `prereg/`          hypotheses and experiment table, committed before any runs
- `harness/`         replay code (reset, replay to step k, continue, log)
- `results/`         raw result files, never edited by hand
- `analysis/`        scripts that turn results into figures

## Ground rules

- Personal time, personal equipment, public data only.
- Every number in the paper must be reproducible from `results/` by a script in `analysis/`.
- Hypotheses are written down before the experiments that test them.
