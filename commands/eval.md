---
description: Evaluate a Phinite graph with LLM judges and report the failures with fixes
argument-hint: "<graph name or flow id> [what to focus on]"
---
Evaluate this Phinite graph: $ARGUMENTS

Load the `phinite-quality` skill first.

1. Find the flow with `list_flows`; note whether it is conversational or autonomous, and which version to test
   (draft "0" unless the user names one).
2. Metrics: `list_eval_metrics(flow=...)` shows the built-in metrics and the flow's custom ones. Propose a short set
   for this use case. If the user's rules need a custom metric, draft it, show its criteria, and create it with
   `create_custom_metric` once they agree.
3. Cases:
   - Conversational: `generate_eval_scenarios(flow, count=5, context=<the focus>)`, then add the user's own cases.
   - Autonomous: write 3-5 `{user_message, user_variables}` cases from the flow's inputs, including a bad input.
   Show the cases in one short list and say the run uses LLM credits; start when the user agrees. If the project
   folder exists, save them as `evals/cases.json`.
4. `run_eval(flow, cases, metrics, context=<what the agents should do>)`. If it is still running, check
   `list_eval_runs` and then `get_eval_run(run_id)`.
5. Report: pass count, each metric's average against its threshold, and for each failing case what went wrong
   (`investigate_session` or `get_logs` on its session_id) and the fix you propose. Apply fixes when the user agrees,
   then run the same cases again.
