---
name: multi-agent-patterns
description: This skill should be used when designing multi-agent systems that need context isolation, supervisor or swarm coordination, explicit handoffs, parallel execution, or a decision on whether multiple agents are justified. Route project-level pipeline decisions to project-development, hosted sandbox infrastructure to hosted-agents, KV-cache state sharing to latent-briefing, and individual tool design to tool-design.
---

# Multi-Agent Architecture Patterns

Multi-agent architectures distribute work across multiple language model instances, each with its own context window. When designed well, this distribution enables capabilities beyond single-agent limits. When designed poorly, it introduces coordination overhead that negates benefits. The critical insight is that sub-agents exist primarily to isolate context, not to anthropomorphize role division.

## When to Activate

Activate this skill when:
- Single-agent context limits constrain task complexity
- Tasks decompose naturally into parallel subtasks
- Different subtasks require different tool sets or system prompts
- Building systems that must handle multiple domains simultaneously
- Scaling agent capabilities beyond single-context limits
- Designing production agent systems with multiple specialized components

Do not activate this skill for adjacent work owned by other skills:
- Deciding task-model fit, pipeline shape, or project-level cost before topology is known: `project-development`.
- Designing hosted sandboxes, warm pools, remote sessions, or background runtime infrastructure: `hosted-agents`.
- Sharing orchestrator state through KV-cache compaction in controlled runtimes: `latent-briefing`.
- Designing the tools each agent exposes: `tool-design`.

## Core Concepts

Use multi-agent patterns when a single agent's context window cannot hold all task-relevant information. Context isolation is the primary benefit — each agent operates in a clean context without accumulated noise from other subtasks, preventing the telephone game problem where information degrades through repeated summarization.

Choose among three dominant patterns based on coordination needs, not organizational metaphor:

- **Supervisor/orchestrator** — Use for centralized control when tasks have clear decomposition and human oversight matters. A single coordinator delegates to specialists and synthesizes results.
- **Peer-to-peer/swarm** — Use for flexible exploration when rigid planning is counterproductive. Any agent can transfer control to any other through explicit handoff mechanisms.
- **Hierarchical** — Use for large-scale projects with layered abstraction (strategy, planning, execution). Each layer operates at a different level of detail with its own context structure.

Design every multi-agent system around explicit coordination protocols, consensus mechanisms that resist sycophancy, and failure handling that prevents error propagation cascades.

## Detailed Topics

### Why Multi-Agent Architectures

**The Context Bottleneck**
Reach for multi-agent architectures when a single agent's context fills with accumulated history, retrieved documents, and tool outputs to the point where performance degrades. Recognize three degradation signals: the lost-in-middle effect, attention scarcity, and context poisoning.

Partition work across multiple context windows so each agent operates in a clean context focused on its subtask. Aggregate results at a coordination layer without any single context bearing the full burden.

**The Token Economics Reality**
Budget for substantially higher token costs. Production data shows multi-agent systems cost far more tokens than single-agent chat:

| Architecture | Token Multiplier | Use Case |
|--------------|------------------|----------|
| Single agent chat | Baseline | Simple queries |
| Single agent with tools | 2-5x baseline | Tool-using tasks |
| Multi-agent system | 10-50x baseline | Complex research/coordination |

Prioritize model selection alongside architecture design — upgrading to better models often provides larger performance gains than doubling token budgets.

**The Parallelization Argument**
Assign parallelizable subtasks to dedicated agents with fresh contexts rather than processing them sequentially. Total real-world time approaches the duration of the longest subtask rather than the sum of all subtasks.

**The Specialization Argument**
Configure each agent with only the system prompt, tools, and context it needs. Specialized agents carry only what they need, operating with lean context optimized for their domain.

### Architectural Patterns

**Pattern 1: Supervisor/Orchestrator**
```
User Query -> Supervisor -> [Specialist A, Specialist B, Specialist C] -> Aggregation -> Final Output
```

Choose this pattern when: tasks have clear decomposition, coordination across domains is needed, or human oversight is important.

Trade-offs: strict workflow control and easier human-in-the-loop interventions, but the supervisor context becomes a bottleneck, supervisor failures cascade to all workers, and the "telephone game" problem emerges.

**The Telephone Game Problem and Solution**
Supervisors paraphrase sub-agent responses, losing fidelity with each pass. Fix by implementing a `forward_message` tool that allows sub-agents to pass responses directly to users:

```python
def forward_message(message: str, to_user: bool = True):
    """Forward sub-agent response directly without supervisor synthesis.
    Use when sub-agent response is final, complete, and format-sensitive."""
    if to_user:
        return {"type": "direct_response", "content": message}
    return {"type": "supervisor_input", "content": message}
```

**Pattern 2: Peer-to-Peer/Swarm**
```
Agent A <-> Agent B <-> Agent C  (any-to-any handoffs)
```

Choose this pattern when: tasks require flexible exploration, rigid planning is counterproductive, or the problem space is poorly understood.

Trade-offs: maximum flexibility and no single point of failure, but coordination overhead grows quadratically, consensus is harder to achieve, and debugging emergent behavior is difficult.

**Pattern 3: Hierarchical**
```
Strategy Layer -> Planning Layer -> Execution Layer -> [Worker, Worker, Worker]
```

Choose this pattern when: projects have layered abstraction needs, different granularity levels require different context, or the system must scale to many concurrent tasks.

### Coordination Protocols

**Explicit Handoffs**
Every agent transition must include: what task is being handed off, what context the receiving agent needs, what the expected output format is, and what happens if the receiving agent fails.

**Consensus Mechanisms**
When multiple agents provide input on the same decision, implement structured disagreement resolution. Simple majority voting produces sycophantic agreement. Better: require agents to independently propose solutions, then have a separate evaluator agent score proposals against explicit criteria.

**Failure Handling**
Design for partial failure. When one agent in a multi-agent system fails, the system must: detect the failure, decide whether to retry, fail gracefully for that subtask, or escalate. Never let a single agent failure crash the entire system.

## Gotchas

- **Anthropomorphic role design**: Naming agents "researcher," "editor," "critic" creates organizational metaphors that waste tokens on persona maintenance. Name agents by function: `search_agent`, `format_agent`, `validate_agent`.
- **Context leakage between agents**: Shared state (databases, files, APIs) can create implicit context sharing that undermines isolation. Audit all shared state for unintended coupling.
- **Sycophantic consensus**: Agents shown other agents' outputs tend to agree rather than independently evaluate. Present problems independently, then compare solutions.
- **Coordination token overhead**: The coordination layer (supervisor prompts, handoff messages, aggregation) can consume more tokens than the actual work. Monitor coordination-to-work ratio.

## Integration

- `context-fundamentals` explains the attention mechanics that motivate context isolation.
- `context-degradation` identifies the failure patterns that multi-agent patterns prevent.
- `tool-design` covers designing the tools each agent exposes.
- `hosted-agents` covers the runtime infrastructure for hosted multi-agent systems.
- `latent-briefing` provides an alternative to explicit context passing via KV-cache compaction.
