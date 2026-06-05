# Attention Mechanics Deep Dive

## The Attention Sink Phenomenon

The first token in a sequence (typically BOS — beginning of sequence) absorbs disproportionate attention weight regardless of its semantic content. This was first documented in the "StreamingLLM" research and has been replicated across model families.

### Why It Matters
The attention sink means that the first position in context is not just "important" — it is fundamentally different from all other positions. Content placed immediately after the BOS token receives residual attention benefits from its proximity to the sink.

### Practical Implications
- **First-position privilege**: System-level identity and critical rules placed in the first position receive the strongest attention.
- **Sink-adjacent positioning**: Instructions placed in positions 2-10 benefit from proximity to the sink.
- **Middle-position penalty**: As content grows, middle positions lose attention budget to both the sink and the recency effect.

## The U-Shaped Attention Curve

Experimental evidence across multiple model families shows a consistent U-shaped attention curve:

```
Attention
   ^
   |  *                                           *
   |   *                                         *
   |    *                                       *
   |     *                                     *
   |      *                                   *
   |       *         *  *  *  *  *           *
   |        *      *                  *     *
   |         *   *                      * *
   |          * *                        *
   +---------------------------------------------> Position
   0         25%        50%         75%       100%
```

Key findings:
- **Primacy effect**: First 10-15% of context receives strong attention
- **Recency effect**: Last 10-15% of context receives strong attention
- **Middle trough**: Central 50-70% receives significantly reduced attention
- **Trough depth**: Middle-position recall accuracy drops 10-40% compared to edge positions

## Effective vs. Raw Context Capacity

A model with a 128K-token context window does not have 128K tokens of useful capacity. Effective capacity is the point beyond which adding more tokens provides diminishing returns and may actively harm performance.

### Factors Reducing Effective Capacity
1. **Attention dilution**: Each added token dilutes attention for existing tokens
2. **Computational limits**: Self-attention is O(n²) in theory; optimized implementations are still sensitive to length
3. **Memory contention**: Longer contexts increase KV cache requirements
4. **Quality degradation**: As context grows beyond effective capacity, output quality degrades measurably

### Estimated Effective Capacities
These are rough guidelines — actual effective capacity depends on model, task, and content:

| Model Context | Estimated Effective | Ratio |
|--------------|-------------------|-------|
| 4K tokens | ~3K | 75% |
| 32K tokens | ~20K | 62% |
| 128K tokens | ~60-80K | 50-62% |
| 1M+ tokens | Highly task-dependent | <50% |

## Experimental Evidence

### Multi-Needle-in-a-Haystack Tests
Place multiple target facts at known positions within a large context. Ask the model to retrieve all targets. Results consistently show:
- Targets at beginning: 90-95% recall
- Targets at end: 85-92% recall
- Targets in middle: 55-80% recall (depending on context length)

### The Ruler Benchmark
The RULER benchmark extends basic needle tests with multi-hop reasoning, variable tracking, and aggregation tasks. Results show that degradation is not just about recall — it affects reasoning quality, not just retrieval accuracy.

### Cross-Model Consistency
The U-shaped curve appears across GPT-4, Claude, Gemini, Llama, and Mistral model families. The specific parameters differ, but the qualitative pattern is universal.
