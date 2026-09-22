# Delegation guide

Optimize cost per accepted deliverable, not delegation count or worker duration. Preserve correctness. Read this only when the compact policy leaves a worthwhile dispatch or blocker question.

## Choose a work package

Delegate when a short contract and checkable result replace substantial lead execution. Include briefing, review and likely repair in that decision. Cheap worker tokens do not justify repeated lead interventions.

| Work | Decision |
| --- | --- |
| One lookup or obvious correction already in view | Lead does it directly. |
| Related searches, inventory or exact edits with fixed checks | Batch for Luna high. |
| Component implementation, scoped diagnosis, refactor or docs from settled behavior | Luna xhigh owns the result and relevant tests. |
| Review of a finished change | Luna xhigh checks named risks; lead judges findings. Do not add a review worker by default. |
| Unclear requirements, architecture or coupled debugging | Lead resolves or narrows the question first. |

Cluster work sharing context and file ownership. Do not split implementation, tests and ordinary local fixes across fresh workers. Keep follow-ups with the same worker while its scope still fits. Parallelize disjoint owners; sequence dependencies. Do not give a worker a larger ambiguous task merely to keep it busy longer.

## Transfer the decisions, not the history

Give the outcome, owned files, necessary context, settled interfaces, non-goals and acceptance checks. Luna can read the code; do not paste it or the lead's investigation diary.

```text
Update parse_date() to accept ISO dates ending in Z.
Own src/date.py and tests/test_date.py. Keep naive-date behavior and the
public API unchanged. Add regression cases; run the date tests and fix
local failures. Escalate if this needs an API change or edits outside scope.
Return outcome, changed paths, checks/results and unresolved risks.
```

The worker handles ordinary implementation choices and local corrections. Escalate conflicting requirements, cross-owner changes or a blocker it cannot resolve within the contract. The lead supplies the missing decision, not a fresh transcript.

## Finish without babysitting

Prefer completion notifications while the lead does independent work. When waiting is necessary, use a bounded wait appropriate to the task. Do not alternate short waits, clock checks and empty-file checks. A timeout or quiet worker is not evidence of failure.

Intervene on a reported blocker, repeated failed approach, scope violation or agreed deadline. Stop or rescope unproductive work; do not blindly respawn the same failed brief. A bounded correction with a failing case is different from a blind retry.

Review the diff and verification receipt, then check integration and correctness-critical risks. Retain independent verification where warranted. Do not repeat the worker's search or test sequence unless evidence is missing, unreliable or affected by integration. Return local defects to their owner; the lead keeps hard diagnosis and final acceptance.

## Judge the result

When usage data is available, compare worker cost plus lead dispatch, review and repair against estimated direct lead work for the same accepted outcome. Separate observed overhead from assumed replacement cost. Count cached input and output at their respective rates; reasoning is already part of output. Do not infer savings from token counts or the worker price ratio alone, or promise a fixed saving percentage.
