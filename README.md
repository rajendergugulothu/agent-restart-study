# agent-restart-study

**How close to the true failure step does a restart need to be to repair a failed LLM agent run?**

When an LLM agent fails a multi-step task, a common fix is to rewind to the step where
things went wrong and let the agent try again from there. Failure attribution methods
try to find that step, and they are usually scored on whether they name it exactly.
This project tests whether exact matters: it restarts failed runs from different points
and measures how often the repair works and what it costs.

> **Status:** early stage. Literature review and project setup. No results yet.

## Research questions

1. How does repair success change with the distance between the restart step and the annotated failure step?
2. Does restarting from a predicted failure step repair runs as well as restarting from the annotated one?
3. Which restart point gives the best repair success per token spent?
4. What share of failures cannot be repaired by restarting, even from the annotated step?

## Study design

Each failed run is replayed up to a restart step, and the agent then continues under
the same step budget and the same repair prompt. Only the restart point changes.

| Restart condition | Restart point |
|---|---|
| Scratch | Step 1, the full task again |
| Random | A uniformly random step |
| Predicted | The step named by a failure attribution method |
| Annotated | The human-annotated failure step |
| Offset | The annotated step shifted earlier or later by k steps |

Every condition is repeated several times per run. Outcomes recorded: task success,
steps taken and tokens used, reported with confidence intervals.

## Data and environments

The study uses public resources and links to them rather than copying them here.

| Resource | Role in this study | License |
|---|---|---|
| [AgentErrorBench](https://github.com/ulab-uiuc/AgentDebug) | Failed trajectories with annotated critical error steps | MIT |
| [ALFWorld](https://github.com/alfworld/alfworld) | Text-based household tasks, replayable offline | MIT |
| [WebShop](https://github.com/princeton-nlp/WebShop) | Simulated online shopping tasks | MIT |
| [Who&When](https://github.com/ag2ai/Agents_Failure_Attribution) | Failure attribution baselines and annotated failure logs | MIT (code) |

## Repository layout

```
agent-restart-study/
├── src/restart_study/   Python package
│   ├── envs/            environment adapters (reset a task, apply actions)
│   ├── replay/          replay logged actions up to a restart step
│   ├── agents/          model clients and the continuation loop
│   ├── attribution/     methods that predict the failure step
│   └── metrics/         repair success, token cost, confidence intervals
├── configs/             one YAML file per experiment
├── scripts/             command-line entry points
├── tests/               unit tests
├── results/             summary result files (raw logs are not tracked)
├── analysis/            scripts that produce the paper's tables and figures
└── docs/
    ├── research_log.md  dated working notes
    └── notes/           reading notes, one file per paper
```

## Getting started

Requires Python 3.10 or newer.

```bash
git clone https://github.com/rajendergugulothu/agent-restart-study.git
cd agent-restart-study
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Copy `.env.example` to `.env` and add API keys if you use hosted models.
Environment and dataset setup instructions will be added with the replay harness.

## Roadmap

- [x] Project setup
- [ ] Literature review and novelty check
- [ ] Verify that logged trajectories replay deterministically
- [ ] Replay harness
- [ ] Pilot on a small set of failed runs
- [ ] Full experiments
- [ ] Analysis and write-up

## Related work

- Zhang et al., [Which Agent Causes Task Failures and When?](https://arxiv.org/abs/2505.00212) (Who&When)
- Zhu et al., [Where LLM Agents Fail and How They Can Learn From Failures](https://arxiv.org/abs/2509.25370) (AgentDebug, AgentErrorBench)
- Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) (MAST)
- [DoVer](https://arxiv.org/abs/2512.06749), intervention-based checking of failure attributions

## Principles

- Hypotheses are written down before the experiments that test them.
- Every reported number can be regenerated from `results/` by a script in `analysis/`.
- Baselines include the simple ones: restart from scratch and restart from a random step.

## License

MIT. See [LICENSE](LICENSE).
