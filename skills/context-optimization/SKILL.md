---
name: context-optimization
description: This skill should be used for token-level efficiency tactics — observation masking, prefix caching, context partitioning, budget allocation, retrieval precision, format optimization, and trajectory-level token reduction. Route foundational concepts to context-fundamentals, failure diagnosis to context-degradation, compression strategies to context-compression, and filesystem offloading to filesystem-context.
---

# Context Optimization Techniques

Apply tactical techniques to maximize useful information per token within the context window. Context optimization operates at the token level — it is the operational counterpart to the conceptual foundation in `context-fundamentals` and the failure diagnosis in `context-degradation`. Every technique trades implementation complexity for token savings.

## When to Activate

Activate this skill when:
- Reducing token usage in production agent systems
- Implementing prefix caching for repeated context patterns
- Designing observation masking for tool outputs
- Partitioning context between static and dynamic sections
- Allocating token budgets across context components
- Optimizing retrieval precision to minimize irrelevant content

Do not activate this skill for adjacent work owned by other skills:
- Explaining why token efficiency matters: `context-fundamentals`.
- Diagnosing specific failure patterns: `context-degradation`.
- Designing compression strategies for long sessions: `context-compression`.
- Offloading content to filesystem: `filesystem-context`.

## Core Concepts

Partition context into static and dynamic regions. Static content (system prompt, tool definitions, persistent instructions) benefits from prefix caching — it is computed once and reused across turns. Dynamic content (user messages, tool outputs, retrieved documents) changes every turn and cannot be cached.

Apply observation masking to tool outputs: after processing, replace verbose outputs with compact summaries. The full output served its purpose during the processing turn; subsequent turns need only the conclusions.

Budget tokens explicitly across components. A 128K context window might allocate: 10K for system prompt, 5K for tool schemas, 20K for retrieved documents, 50K for conversation history, and 43K headroom. Monitor actual usage against budget and trigger compaction when any component exceeds its allocation.

## Detailed Topics

### Observation Masking

After a tool call is processed, replace the full output with a summary:

```python
def mask_observation(tool_name: str, raw_output: str, summary: str) -> str:
    """Replace verbose tool output with compact summary for subsequent turns."""
    return f"[{tool_name} output — {len(raw_output)} chars, summarized]\n{summary}"
```

Apply masking selectively: mask search results after relevant items are extracted, mask file contents after key sections are identified, but preserve raw output when the model needs to reference exact content.

### Prefix Caching

Structure context so static content appears first:

```
[CACHED PREFIX — computed once]
System prompt + Tool definitions + Persistent instructions

[DYNAMIC SUFFIX — computed every turn]
Conversation history + Retrieved documents + Current task
```

Benefits compound with conversation length: a 10K cached prefix saves re-computation on every turn after the first. Design system prompts with this in mind — avoid placing dynamic content before static content.

### Context Partitioning

Separate context into logical partitions with independent management:

| Partition | Content | Strategy |
|-----------|---------|----------|
| Identity | System prompt, persona | Static, cached |
| Tools | Tool schemas, descriptions | Static, cached |
| Knowledge | Retrieved documents | Dynamic, filtered |
| History | Conversation turns | Dynamic, compacted |
| Task | Current instructions | Dynamic, always present |

Each partition has its own token budget and compaction trigger. This prevents one partition (e.g., history) from crowding out another (e.g., knowledge).

### Budget Allocation

```python
class TokenBudget:
    def __init__(self, total: int):
        self.allocations = {
            "system": int(total * 0.08),     # 8% for system prompt
            "tools": int(total * 0.04),       # 4% for tool schemas
            "knowledge": int(total * 0.15),   # 15% for retrieved docs
            "history": int(total * 0.40),     # 40% for conversation
            "task": int(total * 0.10),        # 10% for current task
            "headroom": int(total * 0.23),    # 23% safety margin
        }

    def check(self, partition: str, current_tokens: int) -> bool:
        """Return True if partition is within budget."""
        return current_tokens <= self.allocations[partition]
```

### Format Optimization

Choose response formats that minimize token waste:

- **JSON vs. Markdown**: JSON uses structural tokens (braces, quotes, commas) that add 20-40% overhead. Use markdown for human-readable output, JSON only when structured parsing is required.
- **Verbose vs. terse**: "The file `main.py` was successfully created with 45 lines" vs. "Created `main.py` (45 lines)." The terse version uses 60% fewer tokens.
- **Inline vs. referenced**: Include small results inline; reference large results by file path.

## Gotchas

- **Premature masking**: Masking observations before the model has fully processed them loses information that may be needed in the same turn. Only mask after the turn that uses the output.
- **Cache invalidation**: Any change to the static prefix invalidates the entire cache. Avoid placing frequently-changing content in cached regions.
- **Budget rigidity**: Hard token budgets can prevent the model from loading critical information. Implement soft budgets with overflow alerts rather than hard cutoffs.
- **Format optimization backfire**: Extremely terse responses can confuse agents that expect verbose confirmation. Calibrate terseness to the model's expectations.

## Integration

- `context-fundamentals` provides the theoretical basis for optimization decisions.
- `context-degradation` identifies failure patterns that optimization prevents.
- `context-compression` provides complementary session-level strategies.
- `filesystem-context` provides offloading as an alternative to in-context optimization.
