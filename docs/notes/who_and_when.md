# Who & When — paper notes

Paper: Shaokun Zhang et al., *Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems* (2025).

Version reviewed: arXiv:2505.00212v3, 2 June 2025 (camera-ready).
Sources: [abstract](https://arxiv.org/abs/2505.00212), [full text](https://arxiv.org/html/2505.00212v3), [PDF](https://arxiv.org/pdf/2505.00212v3). Section, figure, and table references below refer to this version. Paper is licensed CC BY 4.0; these are paraphrased study notes with attributed numerical results.

## Problem and contribution

Given a failed multi-agent conversation, identify which agent caused the failure and the decisive step. The contribution is a human-annotated benchmark and evaluation of LLM-based attribution, rather than an executed recovery system. See abstract, §§1–2.

## 1. How is the decisive error step defined?

For a failed trajectory, replace the action at agent–step pair (i, t) with a correct action, preserve the earlier prefix, and adjust subsequent actions to ensure correctness. If the resulting hypothetical trajectory succeeds, that pair is a decisive error. If several qualify, choose the earliest in time. The agent and time become the failure-responsible agent and decisive error step. See §2, equations (3)–(5).

Important distinction: this is the earliest *decisive* mistake, not necessarily every run's first imperfect action. The definition allows downstream adjustments; it does not establish that changing one action and resuming the original policy will reliably recover the task.

## 2. Dataset, annotators, and confidence

Who&When contains 184 annotated failures from 127 systems: 126 task-specific CaptainAgent-generated configurations and one hand-crafted Magentic-One system. Queries come from GAIA and AssistantBench validation data. Only failures are retained. Each record includes the query, full failure log, attribution labels and explanation; generated-system records also include configuration information. See §3 and Appendix C, Table 5.

| System group | GAIA failures | AssistantBench failures | Log lengths |
| --- | ---: | ---: | --- |
| Algorithm-generated | 98 | 28 | 5–10 / 6–10 steps, respectively |
| Hand-crafted | 30 | 28 | 5–130 / 8–129 steps, respectively |

Three human AI-agent experts annotated the logs; the paper provides anonymized identifiers, not names. Round I divides logs among them, with labels for agent, step, explanation, and confident versus uncertain. Round II discusses uncertain cases until everyone is persuaded, rather than accepting a simple majority. Round III cross-checks another expert's annotations and resolves discrepancies through discussion/re-annotation. See §3.2 and Appendix F, Figure 10.

Initial uncertainty was approximately 15%–30% across annotators. Annotation time was 30.9, 30.2, and 23.2 hours (84.3 hours total). Figure 2 also shows pre-discussion disagreement. The final consensus is not an independently measured probability of correctness. No calibrated confidence scores or intervention-based validation of labels are reported. See §3.3, Figure 2.

## 3. Three attribution methods, one line each

| Method | Operation |
| --- | --- |
| All-at-once | Judge the entire failed log in one prompt and output the responsible agent and step. |
| Step-by-step | Judge successive growing log prefixes, stopping at the first step classified as an error. |
| Binary search | Repeatedly select the half of the remaining log judged to contain the error until one step remains. |

See §4.1 and Appendix A. Binary search is a search over stored log entries, not rollback or execution of alternate trajectories. Appendix A specifies querying the left subsegment to choose which half to retain.

## 4. Agent-level and exact-step accuracy

The abstract reports headline values of **53.5% agent accuracy** and **14.2% step accuracy**. These should not be interpreted as one universal result for one method/configuration. The 53.5% is consistent with the unweighted mean of the four all-at-once agent cells below (53.515%); 14.2% is consistent with the four step-by-step step cells (14.1525%). Those calculations are my reconciliation of the headline, not an explicitly documented aggregation rule.

Table 1 reports GPT-4o results below. Every entry is **agent accuracy / exact-step accuracy (%)**. “Ground truth” means availability of the original query's correct final answer to the judge, not access to the human attribution label.

| Method | Generated, with answer | Hand-crafted, with answer | Generated, without answer | Hand-crafted, without answer |
| --- | ---: | ---: | ---: | ---: |
| Random | 29.10 / 19.06 | 12.00 / 4.16 | 29.10 / 19.06 | 12.00 / 4.16 |
| All-at-once | 54.33 / 12.50 | 55.17 / 5.26 | 51.12 / 13.53 | 53.44 / 3.51 |
| Step-by-step | 35.20 / 25.51 | 34.48 / 7.02 | 26.02 / 15.31 | 32.75 / 8.77 |
| Binary search | 44.13 / 23.98 | 51.72 / 6.90 | 30.11 / 16.59 | 36.21 / 6.90 |

All-at-once is best for agent identification across these settings. Step-by-step wins exact localization in three of four settings; binary search wins on generated logs without the query answer. Some exact-step results are below random. See §§4.2–4.3, Table 1.

Additional experiments should be kept separate: Table 3's hybrid first predicts the agent with all-at-once, then searches that agent's steps with step-by-step. It reports 57.02% agent / 12.28% step accuracy and 149,177 tokens, versus 17,106 tokens for its all-at-once baseline. Table 4 reports o1 step-by-step at 36.21% agent / 13.79% step on hand-crafted logs. Stronger reasoning models do not consistently improve both metrics. These are not the abstract's aggregate results.

## 5. Do they evaluate accuracy within a few steps?

**Yes. This is already an explicit metric and experiment**, called step-level accuracy with tolerance (§3; §4.5, Table 2). A prediction is accepted when its step distance from the annotation is at most the tolerance.

| Tolerance | All-at-once (%) | Step-by-step (%) | Binary search (%) |
| --- | ---: | ---: | ---: |
| ±1 step | 12.07 | 14.66 | 13.79 |
| ±2 steps | 19.83 | 16.38 | 18.97 |
| ±3 steps | 30.17 | 18.10 | 22.41 |
| ±4 steps | 37.07 | 31.90 | 31.89 |
| ±5 steps | 43.10 | 33.62 | 36.21 |

Scope: hand-crafted-system logs, GPT-4o under the paper's default model setting; §4.2 says results average with/without query-answer settings unless otherwise specified. Generated systems are excluded because their maximum of 10 steps would make broad tolerance artificially easy. Figure 5 also plots predicted-versus-annotated step distances.

Study implication: near-step localization alone is not a novel contribution relative to this paper. Symmetric ±k agreement also differs from selecting a useful restart checkpoint: a prediction after the decisive error may already preserve corrupted state.

## 6. Do they restart or repair a failed run?

**They do not report an experiment that uses the predicted attribution to repair an action, restart/replay the failed run, and measure recovered task success.** Their evaluated outputs are agent/step labels and attribution costs, including the hybrid in §4.7. Appendix A operates on existing logs.

Two qualifications prevent an overly broad “no”:

- §2 explicitly defines decisive errors through a hypothetical correction/intervention and successful modified trajectory. Correction is conceptually present, but not empirically tested by the attribution experiments.
- §3.1 describes CaptainAgent's iterative configuration optimization during source-system construction. That is distinct from recovery driven by a predicted error location.

Defensible gap relative to this paper: **test whether an attributed step or nearby checkpoint enables successful, cost-effective recovery of the original failed task through actual intervention and replay.** This paper alone cannot establish novelty across the wider literature; its related-work section also discusses corrective agents.

## Results and limitations to retain

- Figures 3–4: broad context helps agent identification, while long logs degrade exact localization. At the longest hand-crafted log lengths, exact-step performance approaches zero.
- Figure 6: aggregate agent-failure frequencies can be useful even when individual attribution is unreliable; this does not demonstrate recovery of individual tasks.
- The benchmark is small (184 failures), includes only one hand-crafted system, and has very different log lengths across system groups. Generalization to other tasks, runtimes, and long-running workflows remains uncertain.
- Consensus labels depend on expert interpretation. The paper acknowledges subjectivity; label agreement is not proof of causal effect under an implemented intervention.
- One agent–step target compresses failures that can involve multiple agents and mistakes. A recovery study should examine that assumption.
- The main text's statement that query-answer availability improves every result has exceptions in Table 1 (e.g., all-at-once generated step accuracy and step-by-step hand-crafted step accuracy). Prefer the actual cells over that blanket statement.
- Table 3's all-at-once agent result (57.02%) differs from Table 4's GPT-4o result (54.31%); do not silently combine them into a single baseline.

## Proposed next experiment — my interpretation, not a paper result

Compare no repair, full restart, random checkpoint repair, predicted checkpoint repair, and human-label checkpoint repair under matched budgets. Preserve the prefix and environment snapshot, apply a specified repair policy, then execute the continuation rather than assuming later actions are correct. Report recovered-task success, extra tokens/tool calls/time, side effects, and repeated-run variability alongside exact and ±k attribution accuracy. Separate early from late localization errors. This directly tests whether localization is useful for recovery.
