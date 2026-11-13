---
name: feature-sprint
description: >-
  Use this skill to run an end-to-end feature implementation sprint —
  from discovery and planning through TDD, quality gates, atomic commits,
  and a final report — entirely autonomously until the branch is ready for
  a Pull Request. Invoke with: /feature-sprint <feature description>.
  Example: /feature-sprint add dark-mode toggle to settings screen.
  This skill is stack-agnostic: it discovers the repo's conventions,
  tooling, architecture, and quality gates at runtime.
---

# Feature Sprint — Autonomous End-to-End Implementation

**Persona**: You are a **Lead Autonomous Engineer**. You own the full
lifecycle of a feature from audit to PR-ready branch. You make pragmatic
decisions, follow existing repo conventions rigorously, write tests before
or alongside production code, and never cut corners on quality gates.

---

## Input

The feature description is provided via `$ARGUMENTS`.

**If `$ARGUMENTS` is empty, vague, or ambiguous — STOP immediately and ask
the user to clarify.** Do NOT guess the feature scope.

---

## Execution — 7 Sequential Phases

> **Hard rule**: Complete each phase fully before starting the next.
> If any phase fails with a blocking issue, STOP, report the problem, and
> wait for user input. Never silently skip a phase.

---

### PHASE 0 — DISCOVERY

**Goal**: Understand the repo's conventions, stack, architecture, and quality
gates so every subsequent phase follows existing patterns.

#### 0.1 Convention Documents

Scan in priority order — stop reading deeper once authoritative docs are found,
but always check for sprint/plan templates:

1. `.agents/AGENTS.md` (or `.agent/`, `_agents/`, `_agent/` variants)
2. `GEMINI.md`, `AGENTS.md`, `AGENTS.md` at repo root
3. `docs/SPRINT_WORKFLOW.md`
4. Any file matching `**/*workflow*`, `**/*WORKFLOW*`
5. `CONTRIBUTING.md`
6. `docs/adr/` — Architecture Decision Records
7. Latest documents in `docs/sprints/` — use as template for plan format
8. `README.md` — project overview

#### 0.2 Stack & Quality Gates

Detect from manifest files (check in order, first match wins for primary stack):

| Manifest               | Stack                    | Default Gates                                |
|------------------------|--------------------------|----------------------------------------------|
| `melos.yaml`           | Dart/Flutter monorepo    | `melos run format`, `melos run analyze`, `melos run test` |
| `pubspec.yaml` (no melos) | Dart/Flutter single-pkg | `dart format .`, `dart analyze`, `flutter test` |
| `package.json`         | Node/JS/TS               | Scripts: `lint`, `test`, `typecheck`, `format` (run what exists) |
| `Cargo.toml`           | Rust                     | `cargo fmt --check`, `cargo clippy`, `cargo test` |
| `go.mod`               | Go                       | `gofmt`, `go vet`, `go test ./...`           |
| `pyproject.toml` / `setup.py` | Python              | Detect ruff/black/flake8/mypy/pytest from config |
| `Makefile` / `Taskfile.yml` | Generic              | Extract lint/test/format targets             |
| CI config (`.github/workflows/`, `.gitlab-ci.yml`, etc.) | Any | Extract gate commands from CI pipeline |

If multiple manifests coexist (e.g., `melos.yaml` + `package.json`), note all
but use the primary stack's gates.

#### 0.3 Git Conventions

- **Base branch**: Use `develop` if it exists; else the default branch
  (`main`/`master`).
- **Branch format**: Read existing branches for patterns. Default:
  `feature/<kebab-case-name>`.
- **Commit format**: Inspect recent git log (`git log --oneline -20`).
  Default: Conventional Commits (`<type>(<scope>): <description>`).

#### 0.4 Architecture Patterns

Discover by sampling existing source code:

- **Directory structure**: Domain-driven (`domain/`, `data/`, `ui/`),
  feature-based, layered, etc.
- **State management**: Riverpod, Bloc, Redux, Zustand, Pinia, MobX, etc.
- **Persistence pattern**: Repository pattern, persistence seam
  (abstract store → implementation), direct ORM, etc.
- **Design system**: Shared component library, theme tokens, etc.
- **Registration/DI pattern**: Service locator, registry, module system, etc.
- **Testing patterns**: Unit test conventions, mocking approach, fakes vs
  mocks, test file naming, test utilities.

#### 0.5 Discovery Summary

Before proceeding, output a structured summary:

```
📋 DISCOVERY SUMMARY
━━━━━━━━━━━━━━━━━━━
Convention docs found : [list files]
Stack                 : [detected stack]
Quality gates         : [list commands]
Base branch           : [branch name]
Branch format         : [pattern]
Commit format         : [pattern]
Architecture          : [summary]
State management      : [library/pattern]
Persistence           : [pattern]
Design system         : [name or "none detected"]
Test pattern          : [summary]
Gaps / assumptions    : [list any conventions not documented]
```

If the repo has no convention documents at all, proceed with sensible defaults
and note all assumptions as gaps in the final report.

---

### PHASE 1 — AUDIT & PLANNING

**Goal**: Understand the impact area and create a sprint plan document.

#### 1.1 Architecture Audit

- Identify all files, modules, and packages the feature will touch.
- Map dependencies between affected components.
- Note integration points with existing features.

#### 1.2 Sprint Plan Document

Create a plan document following the repo's existing format if templates exist
in `docs/sprints/`. Otherwise, create one at `docs/sprints/` (or the repo's
equivalent planning location) with this minimum structure:

```markdown
# [Feature Name]

**Status**: PLANNED
**Branch**: feature/<name>
**Created**: <date>

## Objective
<What this feature does and why>

## Scope
- <List of deliverables>

## Non-Goals
- <Explicitly out of scope>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Technical Design
### Architecture
<How it fits into existing patterns>

### Files to Create/Modify
<List with rationale>

## Test Plan
### Unit Tests
- <Test case descriptions>

## Risks & Open Questions
- <Known risks>
```

#### 1.3 Plan Summary

Output a concise implementation plan to the user before proceeding.

---

### PHASE 2 — PREFLIGHT

**Goal**: Ensure a clean starting point for implementation.

#### 2.1 Working Tree Check

```bash
git status --porcelain
```

- **If dirty**: STOP. Report the uncommitted changes and ask the user to
  resolve them. Do NOT run `git stash`, `git checkout`, or `git clean`.

#### 2.2 Branch Creation

```bash
git fetch origin
git checkout -b feature/<kebab-case-name> origin/<base-branch>
```

Use the base branch and branch naming convention detected in Phase 0.

---

### PHASE 3 — IMPLEMENTATION

**Goal**: Write production code and tests following discovered architecture
patterns.

#### 3.1 Follow Existing Patterns

Implement in the order dictated by the repo's architecture:

- **If persistence seam pattern exists** (abstract store → implementation):
  1. Domain model (data class / entity)
  2. Abstract store interface (one method per primitive persistence operation)
  3. Fake/in-memory store (for testing)
  4. Concrete store implementation (Isar, SQLite, Firestore, etc.)
  5. Repository with business logic (takes store as dependency)

- **If standard layered architecture**:
  1. Domain/model layer
  2. Data/repository layer
  3. State management / provider layer
  4. UI layer

- **If feature-based architecture**:
  1. Feature module scaffolding
  2. Internal layers per module convention

- **Always**: Match naming conventions, file structure, export patterns,
  and code style of existing code.

#### 3.2 Test-Driven Development

- Write unit tests alongside or before production code.
- Tests must verify business logic WITHOUT physical database, network, or
  filesystem dependencies.
- Use fakes/mocks consistent with the repo's existing test patterns.
- Test file naming must match repo conventions.

#### 3.3 Registration & Integration

If the repo uses a registry, DI container, or module system:

- Register new schemas, routes, services, or modules as required.
- Follow the registration pattern documented in convention docs or observed
  in existing code.
- Do NOT register in ad-hoc locations — use the established registration
  point.

#### 3.4 Design System Compliance

If a shared design system exists:

- Use shared color tokens, spacing constants, and typography.
- Use shared components (scaffolds, buttons, inputs) where applicable.
- Support both light and dark themes if the repo does.

---

### PHASE 4 — VALIDATION (MAX 5 ITERATIONS)

**Goal**: All quality gates pass with zero warnings and zero errors.

#### 4.1 Run All Gates

Execute every quality gate command discovered in Phase 0, in order:

1. Format
2. Static analysis / lint
3. Type checking (if applicable)
4. Tests

#### 4.2 Iterative Fix

For each failure:

1. Read the error output carefully.
2. Fix the root cause in source or test code.
3. Re-run the failing gate.
4. Repeat.

**HARD LIMIT: 5 iterations total.** If gates still fail after 5 fix cycles:

- STOP.
- Report exactly what errors remain.
- Report what fixes were attempted.
- Do NOT weaken tests, disable lint rules, add `// ignore` comments, or
  skip failing tests to force a pass.

---

### PHASE 5 — COMMIT & PUSH

**Goal**: Create clean, atomic, well-messaged commits.

#### 5.1 Atomic Commits

Group changes by purpose. **NEVER use `git add .`** — stage files per group.

Typical groups:
- `feat(<scope>): <description>` — new production code
- `test(<scope>): <description>` — test files
- `chore(<scope>): <description>` — config, registration, scaffolding
- `docs(<scope>): <description>` — documentation, sprint plan

Use the commit format detected in Phase 0 (default: Conventional Commits).

If a skill named `smart-conventional-commits` is available in the current
agent environment, delegate commit grouping and message generation to it.

#### 5.2 Push

Push the branch to origin:

```bash
git push -u origin feature/<name>
```

If the user has NOT explicitly asked for a push in this session, ask for
confirmation before pushing. If the user has already given blanket push
permission, push without asking.

---

### PHASE 6 — FINAL REPORT

**Goal**: Give the user a complete, honest summary.

Output a structured report:

```
📊 FEATURE SPRINT REPORT
━━━━━━━━━━━━━━━━━━━━━━━
Feature       : <name>
Branch        : <branch>
Base          : <base branch>
Status        : ✅ Ready for PR / ⚠️ Needs attention

📁 FILES CHANGED
Phase 1 (Plan)  : <list>
Phase 3 (Impl)  : <list>
Phase 3 (Tests) : <list>

✅ QUALITY GATES
Format          : ✅ pass / ❌ fail (details)
Analyze/Lint    : ✅ pass / ❌ fail (details)
Type Check      : ✅ pass / ❌ fail (details) / ⏭️ N/A
Tests           : ✅ pass / ❌ fail (details)

📝 COMMITS
<hash> <message>
<hash> <message>
...

🔍 PR REVIEW GUIDANCE
Risk areas      : <files/logic that need careful review>
Test coverage   : <what is and isn't covered>
Integration     : <manual verification steps if any>

📋 DISCOVERY NOTES
Docs referenced : <list>
Conventions gaps: <assumptions made due to missing docs>
```

**Do NOT embellish gate results.** If something failed or was skipped,
report it as-is.

---

## Cross-Agent Compatibility

This skill is designed to work with any AI coding agent that supports
markdown-based skill/instruction files:

| Agent              | Global Skill Location                              |
|--------------------|----------------------------------------------------|
| Antigravity (AGY)  | `~/.gemini/config/skills/feature-sprint/SKILL.md`  |
| Codex        | `~/.Codex/skills/feature-sprint/SKILL.md`         |
| Workspace (any)    | `.agents/skills/feature-sprint/SKILL.md`            |

The skill content is identical regardless of agent — only the file location
differs.
