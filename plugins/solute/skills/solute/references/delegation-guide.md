# Delegation guide

Use this only when the compact policy does not clearly place the work. This variant lowers the delegation threshold. The aim is fewer Sol execution tokens without weakening Sol's decisions.

## Mapping

| Work | Owner | Reason |
| --- | --- | --- |
| List files or run literal searches | Luna high | Rote collection with directly checkable output. |
| Run fixed commands, formatters, or known tests | Luna high | The steps and pass condition are explicit. |
| Apply an exact mechanical edit | Luna high | Little inference and a deterministic check. |
| Find callers, usages, or affected tests | Luna xhigh | The search is bounded but interpreting relevance takes judgment. |
| Read several files and report the existing pattern | Luna xhigh | Luna can compress repository context before Sol decides. |
| Implement a named function against existing tests | Luna xhigh | Explicit contract and pass condition. |
| Make a small edit that follows a nearby pattern | Luna xhigh | The pattern supplies the contract and review stays cheap. |
| Isolate a test failure | Luna xhigh | Commands constrain the answer, but diagnosis needs reasoning. |
| Investigate a scoped bug with a known symptom | Luna xhigh | The fault domain is narrow enough to inspect cheaply. |
| Draft docs from settled behavior | Luna xhigh | The facts are fixed and Sol can review the result quickly. |
| Review a finished change for missed cases | Luna xhigh, then Sol | Luna expands coverage; Sol judges significance. |
| Convert an agreed design into one component | Luna xhigh | Sol already made the costly design decision. |
| Interpret a vague request | Sol | A wrong interpretation poisons downstream work. |
| Choose architecture or data ownership | Sol | Cross-cutting and expensive to reverse. |
| Debug an unknown, coupled interaction | Sol first | Delegate after narrowing the fault domain. |
| Integrate worker changes or decide completion | Sol | Requires the whole objective and tradeoffs. |

## Aggressive threshold

Delegate when Luna can start from a short contract and return evidence that Sol can check directly. If the cost is close, use Luna. Keep the task only when Sol can finish it more cheaply than writing the brief and checking the answer, such as one obvious lookup or a one-line local correction already in view.

Use `high` only when Luna can follow explicit operations without interpreting code or deciding what a failure means. Use `xhigh` when it must understand behavior, distinguish relevant evidence, diagnose, implement from a contract, or review. A cheap but underpowered handoff wastes both the Luna attempt and Sol's recovery tokens.

Luna may inspect before Sol has chosen an implementation, but it must not turn that inspection into an architectural decision. Ask for facts, options, or a scoped patch. Sol still chooses the direction and decides whether the whole task is done.

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

A ten-scenario comparison on 2026-08-31 had Luna xhigh and Sol high agree on the clear cases: mechanical rename, caller tracing, contract-driven implementation, and test isolation went to Luna; architecture stayed with Sol. This aggressive variant resolves close calls toward Luna:

| Scenario | Decision |
| --- | --- |
| Two repository searches with results to compare | Luna gathers and compresses the evidence. |
| Deadlock with unknown fault domain | Sol until the fault domain is narrow. |
| Review three patches and decide completeness | Luna may check coverage; Sol decides completeness. |
| Apply an approved design to three adapters | Luna implements; Sol integrates. |

Luna tended to accept executable work even when delegation was uneconomical. The lead must still skip a handoff whose brief and review plainly exceed the task. One bounded review also stalled for over 90 seconds and returned nothing, which supports stopping rather than automatically retrying.

These are routing observations, not a price benchmark. Cached instructions and repository context differed between runs. Judge economy by whether the Sol brief plus review is cheaper than direct Sol execution.
