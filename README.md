# Agent Skills for Context Engineering

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: 15](https://img.shields.io/badge/Skills-15-brightgreen.svg)](#skills-overview)
[![Platform: Antigravity IDE](https://img.shields.io/badge/Platform-Antigravity%20IDE-blueviolet.svg)](https://github.com/maybeanns/antigravity-agent-skills)

A comprehensive, open collection of Agent Skills focused on context engineering and harness engineering principles for building production-grade AI agent systems. These skills teach the art and science of curating context, designing agent operating loops, and evaluating agent behavior across any agent platform — optimized for Google Antigravity IDE.

## What is Context Engineering?

Context engineering is the discipline of managing the language model's context window. Unlike prompt engineering, which focuses on crafting effective instructions, context engineering addresses the holistic curation of **all information** that enters the model's limited attention budget: system prompts, tool definitions, retrieved documents, message history, and tool outputs.

The fundamental challenge is that context windows are constrained not by raw token capacity but by **attention mechanics**. As context length increases, models exhibit predictable degradation patterns: the "lost-in-the-middle" phenomenon, U-shaped attention curves, and attention scarcity. Effective context engineering means finding the **smallest possible set of high-signal tokens** that maximize the likelihood of desired outcomes.

## Skills Overview

### Foundational Skills

These skills establish the foundational understanding required for all subsequent context engineering work.

| Skill | Description |
|-------|-------------|
| [context-fundamentals](skills/context-fundamentals/) | Understand what context is, why it matters, and the anatomy of context in agent systems |
| [context-degradation](skills/context-degradation/) | Recognize patterns of context failure: lost-in-middle, poisoning, distraction, and clash |
| [context-compression](skills/context-compression/) | Design and evaluate compression strategies for long-running sessions |

### Architectural Skills

These skills cover the patterns and structures for building effective agent systems.

| Skill | Description |
|-------|-------------|
| [multi-agent-patterns](skills/multi-agent-patterns/) | Master orchestrator, peer-to-peer, and hierarchical multi-agent architectures |
| [memory-systems](skills/memory-systems/) | Design short-term, long-term, and graph-based memory architectures |
| [tool-design](skills/tool-design/) | Build tools that agents can use effectively |
| [filesystem-context](skills/filesystem-context/) | Use filesystems for dynamic context discovery, tool output offloading, and plan persistence |
| [hosted-agents](skills/hosted-agents/) | Build background coding agents with sandboxed VMs, pre-built images, and multiplayer support |

### Operational Skills

These skills address the ongoing operation and optimization of agent systems.

| Skill | Description |
|-------|-------------|
| [context-optimization](skills/context-optimization/) | Apply compaction, masking, and caching strategies |
| [latent-briefing](skills/latent-briefing/) | Share task-relevant orchestrator state with workers via task-guided KV cache compaction |
| [evaluation](skills/evaluation/) | Build evaluation frameworks for agent systems |
| [advanced-evaluation](skills/advanced-evaluation/) | Master LLM-as-a-Judge techniques: direct scoring, pairwise comparison, rubric generation, and bias mitigation |
| [harness-engineering](skills/harness-engineering/) | Design autonomous agent harnesses with locked metrics, durable logs, novelty gates, rollback, and human approval boundaries |

### Development Methodology

These skills cover the meta-level practices for building LLM-powered projects.

| Skill | Description |
|-------|-------------|
| [project-development](skills/project-development/) | Design and build LLM projects from ideation through deployment, including task-model fit analysis, pipeline architecture, and structured output design |

### Cognitive Architecture Skills

These skills cover formal cognitive modeling for rational agent systems.

| Skill | Description |
|-------|-------------|
| [bdi-mental-states](skills/bdi-mental-states/) | Transform external RDF context into agent mental states (beliefs, desires, intentions) using formal BDI ontology patterns for deliberative reasoning and explainability |

## Design Philosophy

### Progressive Disclosure

Each skill is structured for efficient context use. At startup, agents load only skill names and descriptions. Full content loads only when a skill is activated for relevant tasks. This mirrors human cognition — maintain an index, not a copy.

### Platform Agnosticism

These skills focus on transferable principles rather than vendor-specific implementations. The patterns work across Google Antigravity IDE, Claude Code, Cursor, GitHub Copilot, and any agent platform that supports skills or allows custom instructions.

### Conceptual Foundation with Practical Examples

Scripts and examples demonstrate concepts using Python pseudocode that works across environments without requiring specific dependency installations. The goal is understanding, not copy-paste.

### Token Consciousness

Every SKILL.md is kept under 500 lines. Detailed reference material lives in `references/` subdirectories, loaded only when needed. This ensures skills don't bloat the agent's context window during discovery.

## Installation & Setup

You can install this skills collection using one of three methods:

### Option 1: CLI Installer / NPM Dependency (Recommended)

To install the package as a local dependency in your project:

```bash
npm i context-management-for-antigravity
```

Alternatively, you can run the installer instantly without installing it as a dependency using Node's package runner (`npx`). This command pulls the package directly from the registry and runs the binary to install the skills based on your environment:

* **Antigravity 2.0 Global Agents:**
  Installs the skills collection to `~/.agents/skills` (the default global discovery path):
  ```bash
  npx context-management-for-antigravity
  ```

* **Antigravity CLI Slash Commands:**
  Installs each skill to `~/.gemini/antigravity-cli/skills/<skill>/SKILL.md` so they can be triggered as slash commands inside the CLI:
  ```bash
  npx context-management-for-antigravity --agy
  ```

* **Custom Directory:**
  Installs the skills recursively into a directory of your choice:
  ```bash
  npx context-management-for-antigravity --path ./my-skills-folder
  ```

---

### Option 2: Direct Git Clone
Clone the repository directly into your local workspace or global skills directory:

```bash
git clone https://github.com/maybeanns/context-management-for-antigravity.git
```
*After cloning, configure your Antigravity IDE configuration to point to the cloned directory.*

---

### Option 3: Plugin Marketplace
If your Antigravity IDE workspace is configured for external marketplace resolution, register and install the plugin using slash commands:

```
/plugin marketplace add maybeanns/context-management-for-antigravity
/plugin install context-management@antigravity-marketplace
```

---

## Skill Activation & Detailed Use Cases

This collection consists of 15 specialized skills. The table below outlines exactly when each skill should be activated (the activation trigger) and its primary practical use cases.

| Skill | Activate When (Trigger Scenario) | Primary Use Cases |
| :--- | :--- | :--- |
| **`context-fundamentals`** | Establishing base context models, designing system prompts, or when analyzing how context structures affect LLM reasoning. | • Setting up startup agent profiles<br>• Designing token-conscious system prompts<br>• Decoupling code instructions from workspace files. |
| **`context-degradation`** | Diagnosing degraded agent performance, "lost-in-middle" attention drops, repeating actions, or context distraction in long sessions. | • Debugging multi-turn session fatigue<br>• Preventing hallucinated tool loops<br>• Restructuring bloated conversation logs. |
| **`context-compression`** | Compressing conversation history or tool trajectories to free up space under strict token limits without losing critical state. | • Compacting long chat histories<br>• Defining token budgets for sub-agents<br>• Generating structured session summaries. |
| **`context-optimization`** | Applying systematic token-saving strategies (masking, partitioning, prefix caching optimization) to make the workspace highly efficient. | • Minimizing overhead of large payload tokens<br>• Restructuring prompts for Prefix Cache hits<br>• Setting up compartmentalized context pools. |
| **`latent-briefing`** | Coordinating worker/sub-agent execution states when the runner runtime can be customized (e.g. KV cache compaction). | • Compacting intermediate state for worker VMs<br>• Fast-loading state for cold-started sub-agents<br>• Transferring task-guided KV contexts. |
| **`multi-agent-patterns`** | Designing orchestration systems, determining if a task warrants parallel agents, or designing sub-agent communications. | • Building orchestrator-worker swarms<br>• Isolating context between specialist sub-agents<br>• Defining handoff protocols between CLI agents. |
| **`memory-systems`** | Designing short-term, long-term, or graph-based memory structures to persist information across multiple sessions. | • Setting up cross-session knowledge bases<br>• Designing hybrid Vector RAG + Knowledge Graph memory<br>• Minimizing context bloating via filesystem paging. |
| **`tool-design`** | Creating new tools (e.g., custom MCP servers), refining tool descriptions, or diagnosing tool selection/argument generation failures. | • Writing precise OpenAPI/JSON tool schemas<br>• Describing tools as steering prompts<br>• Returning rich contextual help in tool errors. |
| **`filesystem-context`** | Offloading verbose outputs to file systems, persisting long-term plans, or managing sub-agent communication files. | • Offloading grep/git output to scratch files<br>• Creating persistent plan-tracking checklists<br>• Using file read/write for dynamic skill loading. |
| **`hosted-agents`** | Designing background agent sandbox pools, pre-built runtime images, session persistence, or multiplayer collab environments. | • Scaffold VM environments for remote execution<br>• Managing warm pool caches for instant CLI runs<br>• Rebuilding sandbox filesystem snapshots. |
| **`evaluation`** | Designing deterministic regression tests, verification frameworks, and pass/fail metrics for agent task execution. | • Asserting file changes match expected specs<br>• Testing tool sequence execution correctness<br>• Automated repo-health checks. |
| **`advanced-evaluation`** | Implementing LLM-as-a-Judge systems, rubric-based grading, pairwise comparisons, or neutralizing evaluator bias. | • Grading non-deterministic code changes<br>• Conducting automated A/B test analysis<br>• Designing double-blind grading prompts. |
| **`harness-engineering`** | Constructing end-to-end agent harnesses with locked targets, durable history tracking, and rollback capabilities. | • Building automated benchmark systems<br>• Managing loop security policies and permissions<br>• Handling human-in-the-loop approvals. |
| **`project-development`** | Starting new AI-native projects, conducting task-model fit audits, or choosing pipeline architectures. | • Auditing complexity of codebase tasks<br>• Designing structured JSON schema outputs<br>• Deciding between RAG vs. fine-tuning approach. |
| **`bdi-mental-states`** | Modeling rational agent deliberative states (beliefs, desires, intentions) for explainable reasoning loops. | • Exporting agent logic as queryable RDF graphs<br>• Resolving plan conflicts using logic solvers<br>• Auditing agent intent history for safety. |

## Examples

See the [examples/](examples/) directory for complete demonstration projects that apply these skills in practice:

| Example | Skills Applied |
|---------|---------------|
| [digital-brain-skill](examples/digital-brain-skill/) | context-fundamentals, memory-systems, filesystem-context |
| [llm-as-judge-skills](examples/llm-as-judge-skills/) | evaluation, advanced-evaluation |
| [code-generation-harness](examples/code-generation-harness/) | harness-engineering, tool-design, context-optimization |
| [research-pipeline](examples/research-pipeline/) | multi-agent-patterns, filesystem-context, context-compression |
| [multi-agent-coordination](examples/multi-agent-coordination/) | multi-agent-patterns, memory-systems, latent-briefing |

## Researcher Operating System

The `researcher/` directory contains a file-based research operating system for continuous skill improvement:

- **source-registry.md** — Research priorities and source tracking
- **mechanisms/** — Behavior-changing mechanism registry (JSONL)
- **claims/** — Volatile claim provenance tracking
- **corpus/** — Machine-readable skill-to-mechanism map
- **rubrics/** — Deterministic quality rubrics
- **scripts/** — Validation and benchmarking scripts
- **benchmarks/** — Activation case fixtures

### Validation Gates

```bash
python3 researcher/scripts/validate_repo.py --strict
python3 researcher/scripts/skill_health.py --strict --no-history
python3 researcher/scripts/run_benchmarks.py
python3 researcher/scripts/check_activation_cases.py
```

#### Per-Skill Routing Accuracy

| Skill | Baseline Top-1 | After Rewrite | Delta |
|-------|----------------|---------------|-------|
| `context-fundamentals` | 0.255 | 0.489 | +23.4pp |
| `project-development` | 0.750 | 1.000 | +25.0pp (perfect) |
| `tool-design` | 0.729 | 0.807 | +7.8pp |

#### Per-Model Accuracy Leaderboard (Post-Corpus Hardening)

| Model | Top-1 | Top-3 |
|-------|-------|-------|
| `gemini-3.1-pro` | 0.920 | 0.933 |
| `composer-2` | 0.913 | 0.947 |
| `gpt-5.5` | 0.913 | 0.973 |
| `claude-opus-4-7` | 0.840 | 0.933 |

### Context Window Savings (Measured)

> **These are real measurements**, not theoretical estimates. Each benchmark processes realistic test fixtures — 41-row database query results, 20-turn agent conversations with tool outputs, 5-tool JSON schemas, all 15 skill files — and reports actual token counts before and after applying each technique.

Run the benchmark yourself:

```bash
python researcher/benchmarks/context-savings/benchmark_context_savings.py
python researcher/benchmarks/context-savings/benchmark_context_savings.py --markdown
python researcher/benchmarks/context-savings/benchmark_context_savings.py --json
```

#### Per-Technique Token Savings

| Technique | Before (tokens) | After (tokens) | Saved | Savings % | Skill |
|-----------|----------------:|---------------:|------:|----------:|-------|
| Observation Masking | 2,222 | 95 | 2,127 | 95.7% | `context-optimization` |
| Hierarchical Summarization | 3,777 | 428 | 3,349 | 88.7% | `context-compression` |
| Tool Schema Optimization | 1,571 | 292 | 1,279 | 81.4% | `tool-design` |
| Progressive Disclosure | 35,803 | 1,789 | 34,014 | 95.0% | `context-fundamentals` |
| Format Optimization | 493 | 136 | 357 | 72.4% | `context-optimization` |
| Filesystem Offloading | 1,250 | 203 | 1,047 | 83.8% | `filesystem-context` |
| Context Partitioning + Budget | 3,682 | 435 | 3,247 | 88.2% | `context-optimization` |
| Handoff Summary | 3,777 | 255 | 3,522 | 93.2% | `context-compression` |
| Selective Retention | 904 | 145 | 759 | 84.0% | `context-compression` |
| Combined Pipeline | 2,936 | 234 | 2,702 | 92.0% | `all context skills` |
| **TOTAL** | **56,415** | **4,012** | **52,403** | **92.9%** | — |

**Key findings:**
- **Progressive Disclosure** delivers the single largest saving (34K tokens) — loading 15 skill descriptions at startup costs 1,789 tokens vs. 35,803 for loading all skill bodies + references
- **Observation Masking** achieves the highest per-item efficiency (95.7%) — a 41-row database query compresses from 2,222 to 95 tokens
- **Tool Schema Optimization** confirms the skill's documented 2-3x inflation claim — actual measurement shows **5.4x inflation** from JSON serialization
- **Combined Pipeline** (all techniques together) achieves 92.0% savings on a full agent session

#### Skill Quality Validation

| Metric | Result | Details |
|--------|--------|---------|
| Activation Boundary Completeness | 100.0% | 15/15 skills have both "When to Activate" and "Do not activate" |
| Cross-Reference Density | 132 refs | Explicit routing to sibling skills for disambiguation |
| Token Budget Compliance (500-line) | 15/15 | All SKILL.md files under 500 lines |
| Routing Signal Quality | 4.0/5.0 | 5-point rubric: activation phrase, scope, disambiguation, detail, cross-refs |

Full results: [context-savings-2026-06-05.json](researcher/benchmarks/context-savings/results/context-savings-2026-06-05.json)

## Contributing

1. Use `template/SKILL.md` as the starting point for new skills
2. Keep SKILL.md under 500 lines; move details to `references/`
3. Include YAML frontmatter with `name` and `description`
4. Define ownership boundaries in "When to Activate" with "Do not activate" blocks
5. Run all validation gates before submitting

## Recognition

This repository is cited in academic research as foundational work on static skill architecture:

> "While static skills are well-recognized [Anthropic, 2025b; Muratcan Koylan, 2025], MCE is among the first to dynamically evolve them, bridging manual skill engineering and autonomous self-improvement."
>
> — *Meta Context Engineering via Agentic Skill Evolution*, Peking University State Key Laboratory of General Artificial Intelligence (2025)

* *Agent Harness Engineering: A Survey*, CMU, Yale, JHU, NEU, Tulane, UAB, OSU, Virginia Tech, and Amazon (2026)

## Credits & Inspiration

This project is built upon the original reference implementation:
* **Original Repository:** [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) by Muratcan Koylan.
* **Google Antigravity IDE Adaptation:** Modified and hardened with structured activation boundaries ("Do not activate" blocks), automatic validation scripts, and custom manifests to optimize tool routing, prefix reuse, and context management specifically within the Antigravity ecosystem.

## License

[MIT](LICENSE) — © 2025 maybeanns
