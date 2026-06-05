# Memory Architecture Reference

## Architecture Decision Matrix

| Factor | Scratchpad | Vector Store | Knowledge Graph | Filesystem |
|--------|-----------|-------------|-----------------|-----------|
| Setup time | Minutes | Hours | Days | Minutes |
| Query flexibility | Low | High (semantic) | High (structural) | Medium (exact) |
| Relationship tracking | None | Implicit | Explicit | Manual |
| Scale limit | Context window | Millions of vectors | Millions of nodes | Disk space |
| Maintenance cost | None | Embedding updates | Schema evolution | File organization |
| Cross-agent sharing | Via context | Via API | Via API | Native filesystem |

## Implementation Patterns

### Tiered Memory Architecture
```
Working Memory (context window)
    ↕ promotion/demotion
Short-Term Memory (session files)
    ↕ consolidation/retrieval
Long-Term Memory (vector store + knowledge graph)
```

### Memory Lifecycle
1. **Acquisition**: New information enters working memory
2. **Evaluation**: Assess importance and relevance
3. **Storage**: Persist to appropriate tier
4. **Consolidation**: Periodically merge and deduplicate
5. **Retrieval**: Load relevant memories into working memory
6. **Expiry**: Remove outdated or invalidated memories
