# KV Cache Compaction Reference

## When Latent Briefing is Feasible

| Requirement | Detail |
|------------|--------|
| Same model architecture | Orchestrator and worker use identical or compatible models |
| Runtime access | Serving infrastructure exposes KV cache read/write APIs |
| Cache format compatibility | KV cache entries are transferable between instances |
| Compaction capability | Mechanism to select task-relevant cache entries |

## Compaction Quality Metrics

- **Relevance precision**: % of included cache entries actually relevant to worker task
- **Relevance recall**: % of relevant cache entries included (not dropped)
- **Worker performance delta**: Task accuracy with vs. without latent briefing
- **Startup latency delta**: Time savings from cache reuse vs. text re-processing

## Comparison with Text-Based Alternatives

| Dimension | Text Summary | Full Context Copy | Latent Briefing |
|-----------|-------------|-------------------|-----------------|
| Info fidelity | 40-70% | 100% | 85-95% |
| Token cost | Low | High | Zero (cache) |
| Startup latency | Fast (short text) | Slow (re-process) | Instant (cache load) |
| Debugging ease | High | High | Low |
| Infrastructure need | None | None | Custom serving |
