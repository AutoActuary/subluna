# Delegation guide

Use this only when the compact policy does not clearly place the work. The aim is fewer lead-model execution tokens without weakening its decisions.

## Mapping

| Work | Owner | Reason |
| --- | --- | --- |
| List files or run literal searches | Luna high | Rote collection with directly checkable output. |
| Run fixed commands, formatters, or known tests | Luna high | The steps and pass condition are explicit. |
| Apply an exact mechanical edit | Luna high | Little inference and a deterministic check. |
| Find callers, usages, or affected tests | Luna xhigh | The search is bounded but interpreting relevance takes judgment. |
| Read several files and report the existing pattern | Luna xhigh | Luna can compress repository context before the lead decides. |
| Implement a named function against existing tests | Luna xhigh | Explicit contract and pass condition. |
| Make a small edit that follows a nearby pattern | Luna xhigh | The pattern supplies the contract and review stays cheap. |
| Apply an explicit multi-file refactor or rename | Luna xhigh | Boundaries and checks are clear; the lead verifies integration. |
| Isolate a test failure | Luna xhigh | Commands constrain the answer, but diagnosis needs reasoning. |
| Investigate a scoped bug with a known symptom | Luna xhigh | The fault domain is narrow enough to inspect cheaply. |
| Draft docs from settled behavior | Luna xhigh | The facts are fixed and the lead can review the result quickly. |
| Review a finished change for missed cases | Luna xhigh, then lead | Luna expands coverage; the lead judges significance. |
| Convert an agreed design into one component | Luna xhigh | The lead already made the costly design decision. |
| Interpret a vague request | Lead | A wrong interpretation poisons downstream work. |
| Choose architecture or data ownership | Lead | Cross-cutting and expensive to reverse. |
| Debug an unknown, coupled interaction | Lead first | Delegate after narrowing the fault domain. |
| Integrate worker changes or decide completion | Lead | Requires the whole objective and tradeoffs. |

## Aggressive threshold

Use the user's 50:1 Astra/Luna cost assumption for routing, not as a measured end-to-end saving. Default to Luna whenever a bounded brief and check are possible. Send discovery before investigating yourself, and batch related work to amortize handoffs. Keep trivial work already in view and decisions requiring the whole picture. Check evidence rather than repeating the investigation.

Use `high` only when Luna can follow explicit operations without interpreting code or deciding what a failure means. Use `xhigh` when it must understand behavior, distinguish relevant evidence, diagnose, implement from a contract, or review. A cheap but underpowered handoff wastes both the Luna attempt and the lead's recovery tokens.

Luna may inspect before the lead has chosen an implementation, but it must not turn that inspection into an architectural decision. Ask for facts, options, or a scoped patch. The lead still chooses the direction and decides whether the whole task is done.

## Brief packing

Good:

```text
Update parse_date() in src/date.py to accept ISO dates with Z.
Keep naive-date behavior unchanged. Tests are in tests/test_date.py.
Success: that file's tests pass.
Return only outcome; changed paths or file:line evidence; verification and result; real blocker or risk. Do not narrate or paste available diffs.
```

Wasteful: repository history, the lead's investigation diary, code Luna can read, repeated requirements, or a request for a long report. A brief should transfer the contract, not the lead's entire context.

## Routing trial

A ten-scenario comparison on 2026-08-31 had Luna xhigh and a lead model agree on the clear cases: mechanical rename, caller tracing, contract-driven implementation, and test isolation went to Luna; architecture stayed with the lead. This policy resolves close calls toward Luna:

| Scenario | Decision |
| --- | --- |
| Two repository searches with results to compare | Luna gathers and compresses the evidence. |
| Deadlock with unknown fault domain | Lead until the fault domain is narrow. |
| Review three patches and decide completeness | Luna may check coverage; the lead decides completeness. |
| Apply an approved design to three adapters | Luna implements; the lead integrates. |

Luna tended to accept executable work even when delegation was uneconomical. The lead must still skip a handoff whose brief and review plainly exceed the task. One bounded review also stalled for over 90 seconds and returned nothing, which supports stopping rather than automatically retrying.

These are routing observations, not a price benchmark. Cached instructions and repository context differed between runs. Judge economy by whether the brief plus lead review is cheaper than direct lead execution.
