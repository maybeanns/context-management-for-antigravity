---
name: latent-briefing
description: This skill should be used when sharing orchestrator trajectory state with workers via task-guided KV cache compaction — applicable when the worker runtime is controllable and the models share compatible architectures. Route multi-agent coordination patterns to multi-agent-patterns, general context optimization to context-optimization, and compression strategies to context-compression.
---

# Latent Briefing via KV Cache Compaction

Latent briefing shares task-relevant orchestrator state with workers by compacting the orchestrator's KV cache into a prefix that workers can reuse. This eliminates the information loss inherent in text-based summarization while preserving the context isolation benefits of multi-agent patterns. It requires a controllable runtime where the orchestrator and workers share compatible model architectures.

## When to Activate

Activate this skill when:
- Orchestrator and workers share the same model architecture and runtime
- Text-based context passing loses too much information
- Worker startup latency from re-processing shared context is a bottleneck
- Building systems where orchestrator trajectory must inform worker behavior precisely

Do not activate this skill for adjacent work owned by other skills:
- General multi-agent coordination without shared KV cache: `multi-agent-patterns`.
- Text-based compression and handoff summaries: `context-compression`.
- Token-level optimization within a single context: `context-optimization`.
- Foundational attention mechanics: `context-fundamentals`.

## Core Concepts

Traditional multi-agent systems pass context between agents as text — the orchestrator summarizes its state, serializes it, and the worker re-processes it from scratch. This introduces two costs: information loss (summarization is lossy) and latency (the worker re-processes tokens the orchestrator already computed).

Latent briefing eliminates both costs by sharing the orchestrator's computed KV cache entries directly with the worker. The worker starts with the orchestrator's "understanding" already loaded, without re-processing the text or losing information to summarization.

The technique requires:
1. **Compatible architectures** — Orchestrator and worker must use the same model (or compatible variants) so KV cache formats are interchangeable.
2. **Controllable runtime** — The serving infrastructure must support KV cache extraction, transfer, and injection.
3. **Task-guided compaction** — Not all of the orchestrator's KV cache is relevant to the worker's task. Compact the cache to retain only task-relevant entries.

## Detailed Topics

### KV Cache Compaction

The orchestrator's full KV cache contains attention states for its entire trajectory — system prompt, tool calls, reasoning, results. Most of this is irrelevant to any single worker task. Compaction selects the subset of KV entries that are relevant to the worker's assignment.

```python
class KVCacheCompactor:
    def compact(self, full_cache, task_description: str, relevance_threshold: float = 0.7):
        """Select KV cache entries relevant to the worker task."""
        task_embedding = self.encode(task_description)
        relevant_entries = []
        for entry in full_cache:
            relevance = self.score_relevance(entry, task_embedding)
            if relevance > relevance_threshold:
                relevant_entries.append(entry)
        return self.build_prefix(relevant_entries)
```

### When to Use Latent Briefing

| Criterion | Text Passing | Latent Briefing |
|-----------|-------------|-----------------|
| Runtime control | No requirement | Must control serving |
| Model compatibility | Any models | Same architecture |
| Information fidelity | Lossy (summarization) | Near-lossless |
| Worker startup latency | Full re-processing | Instant (cache loaded) |
| Implementation complexity | Low | High |
| Debugging transparency | High (readable text) | Low (opaque cache) |

Prefer latent briefing when information fidelity and worker startup latency are critical. Prefer text passing when transparency, simplicity, or cross-model compatibility matters.

### Prefix Construction

Construct the worker's initial context by combining:
1. **Compacted KV cache** — Orchestrator state relevant to the worker's task
2. **Task-specific system prompt** — Worker's role, tools, and constraints
3. **Explicit task instruction** — What the worker should do with the shared state

The compacted cache acts as "background knowledge" — the worker behaves as if it had already processed the relevant portions of the orchestrator's conversation.

## Gotchas

- **Cache format coupling**: Tight coupling to specific model versions and serving frameworks makes latent briefing fragile to infrastructure changes. Abstract the cache interface.
- **Debugging opacity**: Unlike text-based context passing, KV caches are not human-readable. Maintain parallel text summaries for debugging even when using latent briefing.
- **Relevance scoring errors**: Poor compaction can include irrelevant cache entries (diluting worker attention) or exclude critical entries (losing necessary context). Validate compaction quality.
- **Runtime constraints**: Most commercial API providers don't expose KV cache manipulation. Latent briefing currently requires self-hosted or custom serving infrastructure.

## Integration

- `multi-agent-patterns` provides the coordination framework within which latent briefing operates.
- `context-optimization` provides complementary token-efficiency techniques for the text portions.
- `context-compression` provides the text-based alternative when latent briefing isn't feasible.
- `context-fundamentals` explains the attention mechanics that latent briefing optimizes.
