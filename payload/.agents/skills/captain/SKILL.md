---
name: captain
description: "Use when the user says captain, mode captain, pakai captain, or asks you to captain workers through Herdr. Coordinate OMP workers using Google Gemini Flash, choose thinking effort by task complexity, integrate results, and verify completion."
---

# Captain

Treat `pakai captain: <goal>` as the following standing instruction. Respond in the user's language. Explicit user overrides and higher-priority instructions take precedence.

## Role and defaults

- You are captain: own discovery, decomposition, decisions, integration, verification, and final delivery. Workers execute bounded assignments; they do not own the overall plan.
- Use **Herdr** to coordinate visible worker agents, **OMP** as their runtime, and **Google Gemini Flash** as their default model. Do not silently replace Herdr with hidden subagents or switch providers/models.
- Choose worker thinking effort yourself; do not repeatedly ask the user to restate these defaults.
- Keep simple work inline. Delegate only genuinely independent, substantial slices when allowed by the host agent's delegation rules. Never create ceremonial workers for trivial edits.
- Default to at most two simultaneous workers. Reuse available workers you created when safe. Do not take over unrelated existing agents.

## Discover before launching

1. Read the installed `herdr` skill and follow its safety and lifecycle rules. Check `HERDR_ENV=1` before any Herdr control command. If outside Herdr, report that limitation; do not control a different session or silently use another transport.
2. Inspect `herdr --help`, `herdr agent`, and relevant pane commands for current syntax. Never guess flags or IDs.
3. Inspect `omp --help` and `omp models --json` (or `omp models find flash`). Resolve an exact Google-provider Gemini Flash model from the installed catalog. Prefer the current stable, non-Lite Flash model; avoid preview variants if a stable option exists. Catalog presence does not prove authentication: inspect actual startup errors without reading or printing credentials.
4. If several Flash versions are available, choose the newest stable version compatible with the requested effort. If no appropriate Google Flash model is available or access fails, report the concrete blocker. Ask before switching provider/model or changing auth/config.
5. Use the discovered `herdr agent start` syntax with kind `omp`; pass OMP native options after `--`, using `--model <exact-provider/model>` and `--thinking <level>`. Do not change persistent OMP configuration or enable auto-approval as a convenience.

## Effort selection

- `low`: mechanical, well-specified transformations or straightforward collection.
- `medium`: default implementation with bounded behavior and clear acceptance criteria.
- `high`: subtle debugging, concurrency, security-sensitive changes, or difficult edge cases.
- Use only thinking levels supported by the selected runtime/model. If the level is rejected, inspect support and choose a supported level; do not claim an effort setting that was not applied.
- Keep architecture decisions, ambiguous requirements, cross-slice conflicts, and final review with the captain. A worker repeatedly failing is a reason to narrow the assignment or take it over, not endlessly retry it or silently upgrade models.

## Dispatch contract

Discover enough of the repository inline to identify independent slices and shared contracts before assigning work. Assign one owner per edited file; keep shared-file integration with the captain. Do not create worktrees, tabs, or workspaces unless requested. Follow Herdr's default sibling-pane geometry, preserve cwd, and use `--no-focus`.

Each worker prompt must contain:

- Goal and relevant user constraints; workers do not inherit this conversation.
- Exact owned files/surface, required shared interfaces, and explicit non-goals.
- Acceptance criteria and important edge cases.
- Applicable repository instructions and skills to read.
- Instruction not to overwrite others' edits, commit, push, or spawn further workers.
- Instruction to skip build/test/lint/format during concurrent editing; captain runs the appropriate consolidated verification after integration.
- Required final report: changed files, behavior implemented, unresolved risks/blockers, and checks actually run. Never fabricate verification.

Launch independent assignments together when the available tools permit it. Continue useful captain work while they run; avoid busy polling. Use Herdr agent lifecycle commands to wait/read results, not raw pane input for recognized agents. A settled agent state is not proof of task completion: read the worker's report and inspect its actual changes.

## Integrate and finish

- Resolve shared-file changes and cross-slice contracts yourself. Preserve unrelated user changes.
- Run the narrowest meaningful verification covering the final behavior, plus repository-mandated gates. For UI changes, verify the actual surface when available. Do not claim unrun tests passed.
- Fix reachable failures; escalate only genuine missing access, requirements, or permissions. Ask before destructive actions or unrequested model/provider changes.
- Update relevant documentation/skills when behavior changes and repository rules require it.
- Stop temporary processes you started. Close only your own worker panes when safe; never close user panes or kill the Herdr server. Do not interrupt an active worker merely to tidy the layout.
- Final response: result, concrete verification, and remaining blockers if any. Keep orchestration chatter minimal; mention model/effort decisions only when material or requested.

## Invocation examples

- `Pakai captain: implementasikan fitur export CSV.`
- `Captain, cari penyebab bug login dan perbaiki.`
- `Pakai captain, maksimal 3 worker, effort high: refactor modul billing.`

These invocations authorize this workflow for the stated task, not unrelated work, persistent configuration changes, paid plan changes, or bypassing approvals.
