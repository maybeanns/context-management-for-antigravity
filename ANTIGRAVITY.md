# ANTIGRAVITY.md

This file provides guidance to Google Antigravity IDE agents when working with code in this repository.

## Project Overview

Agent Skills for Context Engineering: an open collection of 15 Agent Skills teaching context engineering and harness engineering principles for production AI agent systems. Skills are platform-agnostic (Google Antigravity IDE, Claude Code, Cursor, GitHub Copilot, any Open Plugins-conformant tool). v2.3.0 ships a file-based researcher operating system with deterministic gates and a continuous improvement loop.

Context engineering is the discipline of curating everything that enters a model's context window (system prompts, tool definitions, retrieved documents, message history, tool outputs) to maximize signal within limited attention budget.

## Repository Structure

- `skills/` — 15 skill directories, each containing a `SKILL.md` with YAML frontmatter (`name`, `description`) and optional `references/` and `scripts/` subdirectories
- `examples/` — 5 complete demonstration projects applying skills in practice
- `researcher/` — File-based research-to-skill operating system: rubrics, mechanism registry, claim provenance, corpus index, benchmarks, and validation scripts
- `template/SKILL.md` — Canonical skill template (use when creating new skills)
- `SKILL.md` (root) — Collection-level metadata and skill map
- `.antigravity/marketplace.json` — Antigravity IDE marketplace manifest (single bundled plugin, v2.3.0)
- `.plugin/plugin.json` — Open Plugins format manifest (v2.3.0)

## Build & Test Commands

No top-level build system. Repo-level gates and per-project tooling below.

### Top-level deterministic gates (run on every PR)

```bash
python3 researcher/scripts/validate_repo.py --strict       # corpus structure, manifests, rubric math, mechanism registry, claims, corpus index, activation cases, benchmark scenarios
python3 researcher/scripts/skill_health.py --strict --no-history  # deterministic skill-body quality gate
python3 researcher/scripts/run_benchmarks.py               # adversarial benchmark harness + repo + activation gates
python3 researcher/scripts/check_activation_cases.py       # skill-boundary regression fixtures
```

### Example projects

#### examples/llm-as-judge-skills (TypeScript, Node >= 18)
```bash
cd examples/llm-as-judge-skills
npm install
npm run build        # tsc
npm test             # vitest
```

#### examples/code-generation-harness (Python >= 3.10)
```bash
cd examples/code-generation-harness
pip install -e ".[dev]"
pytest
```

## Skill Authoring Rules

When creating or modifying skills in `skills/`:

1. **Use the template**: Start from `template/SKILL.md`. Every skill must have YAML frontmatter with `name` and `description`.

2. **500-line budget**: Keep SKILL.md under 500 lines. Move detailed content to `references/` subdirectory.

3. **Ownership boundaries**: Every skill must state what it owns and what adjacent skills own. The `description` field and `When to Activate` section must include explicit "Do not activate" blocks.

4. **Third-person descriptions**: Write in third person. Descriptions are injected into system prompts — first-person creates inconsistencies.

5. **Token consciousness**: Challenge every paragraph: "Does this justify its token cost?" Prefer behavior-changing mechanisms over general background.

6. **Cross-references**: Use backtick-quoted skill names for cross-references: `context-fundamentals`, `tool-design`, etc.

7. **Claim system**: Use `claim-<skill-name>-<topic>` identifiers for volatile facts that may change. Track claims in `researcher/claims/index.jsonl`.

8. **Mechanism registry**: If a concept is reusable across skills, add it to `researcher/mechanisms/registry.jsonl`.

9. **Activation cases**: Add boundary test cases to `researcher/benchmarks/activation-cases.jsonl` for every new skill.

10. **Validation**: Run all four deterministic gates before committing changes.

## Key Design Decisions

- **Platform agnosticism**: Never vendor-lock. Abstract to principles that transfer across platforms.
- **Progressive disclosure**: Agents load only skill names initially; full content loads on activation.
- **Gotchas first**: Experience-derived failures are the highest-signal content in any skill.
- **Explicit boundaries**: Overlapping skills create confusion. Every skill must define its edges.
- **Deterministic gates**: Every PR must pass `validate_repo.py --strict` and `skill_health.py --strict`.
