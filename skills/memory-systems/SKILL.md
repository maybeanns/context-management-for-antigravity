---
name: memory-systems
description: This skill should be used when designing agent memory architectures — short-term scratchpads, long-term persistence, entity tracking, vector RAG, knowledge graphs, and the file-system-as-memory pattern. Route filesystem-specific offloading patterns to filesystem-context, cross-session handoff summaries to context-compression, and multi-agent state sharing to multi-agent-patterns.
---

# Memory System Design

Memory architectures determine how agents retain, retrieve, and update information across turns and sessions. The right memory design depends on the retention horizon (within-session vs. cross-session), the query pattern (keyword vs. semantic vs. structural), and the fidelity requirement (exact recall vs. gist). No single memory system dominates all use cases — production systems typically layer multiple strategies.

## When to Activate

Activate this skill when:
- Designing cross-session knowledge persistence
- Choosing between vector RAG and knowledge graph approaches
- Building entity tracking systems for long-running agents
- Implementing scratchpad patterns for within-session state
- Evaluating memory system trade-offs for production deployment

Do not activate this skill for adjacent work owned by other skills:
- Filesystem-specific offloading and discovery patterns: `filesystem-context`.
- Compressing conversation history into handoff summaries: `context-compression`.
- Sharing state between agents in multi-agent systems: `multi-agent-patterns`.
- Designing hosted runtime environments for persistent agents: `hosted-agents`.

## Core Concepts

Design memory around three horizons:

1. **Working memory** (within-turn) — The context window itself. Information the model can directly attend to during inference. Limited by token capacity and attention mechanics.
2. **Short-term memory** (within-session) — Scratchpads, plan files, accumulated tool outputs. Persists across turns but not across sessions. Implemented via message history or filesystem.
3. **Long-term memory** (cross-session) — Knowledge bases, entity stores, learned preferences. Persists indefinitely. Implemented via databases, vector stores, or structured files.

The file-system-as-memory pattern bridges all three horizons: scratch files serve as working memory extensions, session files provide short-term persistence, and structured knowledge files provide long-term storage — all accessible through the same filesystem interface.

## Detailed Topics

### Vector RAG Memory

Store embeddings of past interactions, documents, and decisions. Retrieve semantically similar content at query time.

**Strengths**: Scales to large corpora, handles fuzzy/semantic queries, requires minimal schema design.

**Weaknesses**: Loses relationship information (who said what, in what order, in response to what), embedding quality varies by model and domain, retrieval relevance is probabilistic not deterministic.

**Design pattern**:
```python
class VectorMemory:
    def store(self, content: str, metadata: dict):
        """Store content with metadata for filtered retrieval."""
        embedding = self.embed(content)
        self.index.add(embedding, metadata=metadata)

    def recall(self, query: str, filters: dict = None, top_k: int = 5):
        """Retrieve semantically similar content, optionally filtered."""
        query_embedding = self.embed(query)
        results = self.index.search(query_embedding, top_k=top_k, filters=filters)
        return [r.content for r in results if r.score > self.threshold]
```

### Knowledge Graph Memory

Store entities and relationships as structured graphs. Query by traversing relationships.

**Strengths**: Preserves relationship information, enables reasoning over connections, supports precise structural queries.

**Weaknesses**: Requires explicit schema design, entity extraction is error-prone, scales poorly to unstructured content.

**Design pattern**:
```python
class GraphMemory:
    def store_entity(self, entity: str, entity_type: str, attributes: dict):
        """Store or update an entity with typed attributes."""
        self.graph.upsert_node(entity, type=entity_type, **attributes)

    def store_relationship(self, source: str, target: str, relation: str):
        """Store a directed relationship between entities."""
        self.graph.add_edge(source, target, relation=relation)

    def recall(self, entity: str, depth: int = 2):
        """Retrieve entity and its neighborhood up to given depth."""
        return self.graph.subgraph(entity, max_depth=depth)
```

### File-System-as-Memory Pattern

Use the filesystem as a universal memory layer. Files provide durable, structured, randomly-accessible storage that agents can read and write using standard tools.

**Key patterns**:
- **Scratch pad**: `scratch.md` — running notes, intermediate results, working state
- **Plan file**: `plan.md` — task decomposition, progress tracking, next steps
- **Knowledge base**: `knowledge/` — structured facts, entity records, learned preferences
- **Session log**: `session.md` — chronological record of actions and decisions

**Advantages over in-context memory**: No token cost for stored content, unlimited capacity, persistence across sessions, accessible by multiple agents, human-readable for debugging.

### Entity Tracking

Track entities (people, files, concepts) across interactions:

```python
class EntityTracker:
    def update(self, entity_id: str, facts: dict, source_turn: int):
        """Update entity with new facts, preserving provenance."""
        entry = self.entities.get(entity_id, {"facts": {}, "history": []})
        for key, value in facts.items():
            entry["history"].append({
                "key": key, "old": entry["facts"].get(key),
                "new": value, "turn": source_turn
            })
            entry["facts"][key] = value
        self.entities[entity_id] = entry

    def recall(self, entity_id: str):
        """Retrieve current facts about an entity."""
        return self.entities.get(entity_id, {}).get("facts", {})
```

### Memory Selection Guide

| Criterion | Vector RAG | Knowledge Graph | Filesystem |
|-----------|-----------|----------------|-----------|
| Query type | Semantic/fuzzy | Structural/relational | Path/grep/exact |
| Setup cost | Medium | High | Low |
| Scale | Large corpora | Medium graphs | Medium files |
| Relationship preservation | Poor | Excellent | Manual |
| Cross-agent access | Via API | Via API | Native |
| Human readability | Low | Medium | High |

## Gotchas

- **Embedding drift**: Changing embedding models invalidates stored vectors. Version your embedding model alongside your vector store.
- **Over-retrieval**: Returning too many memories floods context and triggers degradation. Set strict top-k limits and relevance thresholds.
- **Entity resolution**: The same entity referred to differently ("the main file," "app.py," "the application entry point") creates duplicate entries. Implement entity normalization.
- **Stale memories**: Old memories that are no longer accurate can poison current context. Implement TTL (time-to-live) or explicit invalidation for factual memories.

## Integration

- `context-fundamentals` explains the attention budget that memory systems must respect.
- `filesystem-context` provides the filesystem patterns that implement file-based memory.
- `context-compression` provides strategies for compressing memories before storage.
- `multi-agent-patterns` covers sharing memory state across multiple agents.
