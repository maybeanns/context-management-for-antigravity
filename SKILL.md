---
name: context-engineering-collection
description: A comprehensive collection of Agent Skills for context engineering, harness engineering, multi-agent architectures, and production agent systems. Use when building, optimizing, evaluating, or debugging agent systems that require effective context management and reliable operating loops.
version: 2.3.0
author: maybeanns
---

# Agent Skills for Context Engineering

This collection provides structured guidance for building production-grade AI agent systems through effective context engineering. It is optimized for Google Antigravity IDE but works with any agent platform that supports skills or custom instructions.

## When to Activate

Activate these skills when:
- Building new agent systems from scratch
- Optimizing existing agent performance
- Debugging context-related failures
- Designing multi-agent architectures
- Creating or evaluating tools for agents
- Implementing memory and persistence layers
- Designing autonomous research or evaluation harnesses
- Modeling agent cognitive states for explainable reasoning

## Skill Map

### Foundational Context Engineering

**Understanding Context Fundamentals**
Context is not just prompt text — it is the complete state available to the language model at inference time, including system instructions, tool definitions, retrieved documents, message history, and tool outputs. Effective context engineering means understanding what information truly matters for the task at hand and curating that information for maximum signal-to-noise ratio.

**Recognizing Context Degradation**
Language models exhibit predictable degradation patterns as context grows: the "lost-in-middle" phenomenon where information in the center of context receives less attention; U-shaped attention curves that prioritize beginning and end; context poisoning when errors compound; and context distraction when irrelevant information overwhelms relevant content.

**Compression Under Pressure**
Long-running agent sessions accumulate history that eventually exceeds useful capacity. Compression strategies — hierarchical summarization, selective retention, token budgeting — preserve task-critical state while shedding noise. The key insight is that compression is not lossless: every strategy trades some fidelity for capacity, and the engineering challenge is choosing what to lose.

### Architectural Patterns

**Multi-Agent Coordination**
Production multi-agent systems converge on three dominant patterns: supervisor/orchestrator architectures with centralized control, peer-to-peer swarm architectures for flexible handoffs, and hierarchical structures for complex task decomposition. The critical insight is that sub-agents exist primarily to isolate context rather than to simulate organizational roles.

**Memory System Design**
Memory architectures range from simple scratchpads to sophisticated temporal knowledge graphs. Vector RAG provides semantic retrieval but loses relationship information. Knowledge graphs preserve structure but require more engineering investment. The file-system-as-memory pattern enables just-in-time context loading without stuffing context windows.

**Tool Design Principles**
Tools are contracts between deterministic systems and non-deterministic agents. Effective tool design follows the consolidation principle (prefer single comprehensive tools over multiple narrow ones), returns contextual information in error messages, and treats descriptions as prompt engineering that directly steers agent behavior.

**Filesystem-Based Context**
The filesystem provides a single interface for storing, retrieving, and updating effectively unlimited context. Key patterns include scratch pads for tool output offloading, plan persistence for long-horizon tasks, sub-agent communication via shared files, and dynamic skill loading. Agents use `ls`, `glob`, `grep`, and `read_file` for targeted context discovery, often outperforming semantic search for structural queries.

**Hosted Agent Infrastructure**
Background coding agents run in remote sandboxed environments rather than on local machines. Key patterns include pre-built environment images refreshed on regular cadence, warm sandbox pools for instant session starts, filesystem snapshots for session persistence, and multiplayer support for collaborative agent sessions.

### Operational Excellence

**Context Optimization**
Token-level efficiency tactics: observation masking removes redundant tool outputs, prefix caching reuses shared context prefixes, partitioning separates static from dynamic content, and budget allocation ensures each context component earns its token cost.

**Latent Briefing**
When orchestrator and worker share the same model runtime, task-relevant trajectory state can be compressed into KV cache prefixes rather than serialized as text. This eliminates the information loss of summarization while preserving the context isolation benefits of multi-agent patterns.

**Evaluation Frameworks**
Deterministic evaluation gates catch regressions before deployment. Production evaluation stacks combine assertion-based checks (format, structure, constraint compliance) with statistical sampling and LLM-as-judge techniques for subjective quality dimensions.

**Harness Engineering**
Autonomous agent harnesses manage the operating loop: locked evaluation metrics prevent gaming, durable logs enable post-hoc analysis, novelty gates prevent repetitive exploration, rollback mechanisms recover from failures, and human approval boundaries enforce safety constraints.

### Development Methodology

**Project Development**
LLM project lifecycle from ideation through deployment. Task-model fit analysis determines whether LLMs are appropriate. Pipeline architecture designs the flow of information. Structured output design ensures reliable parsing. Batch processing optimizes throughput and cost.

### Cognitive Architecture

**BDI Mental States**
Formal belief-desire-intention modeling transforms unstructured context into explicit mental states. Beliefs represent the agent's model of the world. Desires encode objectives. Intentions commit to specific plans. This framework enables deliberative reasoning and explainable decision-making in complex agent systems.
