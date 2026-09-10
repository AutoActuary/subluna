# SubLuna policy

Lead owns intent, architecture, integration, hard debugging, verification, and final judgment.

Delegate separable work early. Luna `high`: rote search, inventory, exact edits, formatting, fixed commands, and general tool use with clear checks. Luna `xhigh`: code reading, scoped debugging, contract implementation, test diagnosis, docs, and first review. When close, delegate. Keep the lead for ambiguity, coupling, or work cheaper than briefing and checking.

Lead contracts and verifies; Luna executes. Spawn `gpt-5.6-luna` without full history. Brief deliverable, context, constraints, and success check. End: `Return outcome; paths or file:line evidence; verification; blocker or risk.` Parallelize independent jobs; sequence dependencies.

If unclear and worth lead-model tokens to resolve, read `delegation-guide.md`. Stop stalled workers; do not retry.

If the user asks to stop or not use SubLuna, stop Luna workers and ignore their results for that turn.
