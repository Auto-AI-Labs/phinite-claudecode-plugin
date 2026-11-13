---
name: phinite-quality
description: How to evaluate a Phinite graph with LLM judges — test cases (simulated conversations, autonomous runs, or real sessions), built-in and custom metrics, reading failures and fixing them, and scoring a shipped build's real sessions (live or scheduled, with Signals). Use when the user asks to evaluate, score, benchmark or regression-test a graph, to check answer quality, safety or tool use, to create a custom metric or judge, or to watch production quality.
---
# Evaluating a Phinite graph

Evaluations need the Professional plan (otherwise every eval tool says so) and use LLM credits: every case runs the
flow and several LLM judges. **Set them up only when the user asks.** You may offer once, before shipping to
production; don't add evals on your own.

**1. Pick the dataset (run_eval chooses from the flow type)**
- **Conversational → simulation.** A simulated user talks to the flow. `generate_eval_scenarios(flow, count)` writes
  cases from the graph itself (happy path, edge case, adversarial, tool failure, ...). Read them, drop or fix weak
  ones, and add the cases the user cares about. A good case has a concrete `expected_outcome` ("explains the 30-day
  policy and offers store credit"), never "responds well".
- **Autonomous → autonomous.** One case per trigger: `{user_message, user_variables}` with realistic session
  variables, including bad inputs (missing id, wrong format) the flow must refuse.
- **Real traffic → production.** `session_ids` from `list_sessions`, plus an optional `rubric {scenario,
  expected_outcome}`. Scoring production sessions needs the QA or superadmin role.

Keep runs small: up to 10 cases, `max_turns` 6 (raise it for long conversations).

**2. Pick the metrics** (`list_eval_metrics`; leave `metrics` out for the catalog defaults)
- Conversational: `goal_accuracy`, `turn_relevancy`, `role_adherence`; `topic_adherence` needs
  `metric_options.relevant_topics`; `knowledge_retention` for long chats.
- Autonomous or tool-heavy: `task_completion`, `tool_correctness`, `argument_correctness`, `step_efficiency`.
- RAG answers: `turn_faithfulness` (multi_turn) or `faithfulness`, `hallucination` (single_turn).
- `context` on run_eval tells the judges what the agents should do; it isn't sent to custom metrics.

**3. Custom metrics for the use case's own rules** (`create_custom_metric`, saved on the flow, shown in Studio)
- Use one when a rule matters and no built-in checks it: "never quotes a price without the lookup tool", "asks for
  the order id before changing an order", "hands off to a human after two failed attempts".
- `criteria`: what pass and fail look like, with the edge cases (what's acceptable, what isn't). Or
  `evaluation_steps` for an exact procedure. One rule per metric; snake_case names that aren't built-in.
- `eval_mode`: multi_turn for conversation behaviour, agentic for tool use and order, single_turn for one answer.
- `score_type`: numeric (default, passes at `threshold`), boolean for yes/no rules, category with `categories` and
  `pass_labels` to classify (e.g. tone: warm / neutral / rude, pass warm and neutral).
- Thresholds: 0.5-0.7 for quality, 0.9 or boolean for safety and compliance.
- Then pass its name in `metrics` to run_eval and set_build_scoring.

**4. Read the results and fix**
- `run_eval` answers with pass counts, each metric's average and the failing cases with the judges' reasons. A long
  run keeps going on the server: `list_eval_runs`, then `get_eval_run(run_id)`.
- For each failing case: `investigate_session(session_id)` or `get_logs(session_id)` to see what the flow did, then
  fix the cause (prompt, capture description, tool guard, edge label), not the metric.
- Re-run with **the same cases** to show the fix worked and nothing else broke. Keep the case list in the project
  folder (e.g. `evals/cases.json`) so later changes are checked against it.

**5. Watch production** (only when asked; needs a build assigned to that environment)
- `set_build_scoring(flow, env, metrics, mode)`: `live` scores every session as it finishes; `scheduled` scores the
  most unusual sessions of the last 1-7 days once a day. `signals=true` turns on Signals.
- `get_build_scoring` shows the setup and its latest runs; `get_signals` lists recurring problems across real
  sessions, with `refresh=true` to look again.
- Live scoring costs credits per session: prefer `scheduled` for busy flows.

Permissions: QA can run evaluations; creating custom metrics and build scoring need developer or above.
