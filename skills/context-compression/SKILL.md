---
name: context-compression
description: This skill should be used for designing and evaluating compression strategies for long-running agent sessions — hierarchical summarization, selective retention, compaction triggers, quality thresholds, and handoff summaries. Route foundational context concepts to context-fundamentals, failure diagnosis to context-degradation, and token-level efficiency tactics to context-optimization.
---

# Context Compression Strategies

Design compression strategies that preserve task-critical state while shedding accumulated noise. Compression is not lossless — every strategy trades fidelity for capacity. The engineering challenge is choosing what to lose, when to compress, and how to verify that compressed context retains sufficient signal for the task.

## When to Activate

Activate this skill when:
- Long-running sessions accumulate history that approaches context limits
- Designing handoff summaries for agent-to-agent or session-to-session transitions
- Choosing between compression strategies (summarization, truncation, selective retention)
- Evaluating compression quality — what was preserved, what was lost
- Building systems that must maintain coherence across many turns

Do not activate this skill for adjacent work owned by other skills:
- Explaining why context degrades without an active compression task: `context-fundamentals`.
- Diagnosing specific failure patterns in degraded contexts: `context-degradation`.
- Applying tactical token-efficiency techniques (masking, caching, partitioning): `context-optimization`.
- Offloading content to filesystem rather than compressing it: `filesystem-context`.

## Core Concepts

Compression operates on a fidelity-capacity trade-off curve. At one extreme, verbatim retention preserves all information but consumes maximum tokens. At the other extreme, aggressive summarization minimizes tokens but loses nuance, context, and recoverable detail. The optimal compression point depends on the task: creative tasks tolerate more information loss than debugging tasks.

Apply compression proactively, not reactively. By the time context is full, compression under pressure produces lower-quality summaries because the model's attention is already degraded. Set compression triggers at 60-70% of effective context capacity, leaving headroom for the compression operation itself and subsequent work.

Use hierarchical compression: compress oldest content most aggressively, recent content least aggressively, and never compress active task instructions or constraints. This mirrors human memory — distant events are recalled as summaries, recent events retain detail.

## Detailed Topics

### Hierarchical Summarization

Structure compression in tiers based on information age and relevance:

**Tier 1 — Active context (no compression)**
Current task instructions, active constraints, recent tool outputs needed for the current step. These must remain verbatim.

**Tier 2 — Recent history (light compression)**
Last 3-5 turns of conversation. Compress tool outputs to key findings, preserve reasoning steps, retain decision points. Replace verbose outputs with structured summaries.

**Tier 3 — Session history (moderate compression)**
Earlier conversation turns. Compress to a narrative summary: what was attempted, what succeeded, what failed, key decisions made and their rationale. Discard raw tool outputs entirely.

**Tier 4 — Cross-session memory (heavy compression)**
Information from previous sessions. Compress to factual assertions: established facts, user preferences, project state, key file locations. Discard process details entirely.

### Selective Retention Strategies

Not all information deserves equal compression treatment. Prioritize retention of:

1. **Decision rationale** — Why choices were made, not just what was chosen
2. **Error history** — What failed and why, to avoid repeating mistakes
3. **User preferences** — Stated requirements, style preferences, constraints
4. **State checkpoints** — Current progress markers, file locations, pending tasks
5. **Tool output summaries** — Key findings, not raw data

Aggressively discard:
- Verbose tool outputs that have been processed
- Exploratory reasoning that didn't lead to decisions
- Repeated information (same instruction given multiple times)
- Formatting and structural tokens that don't carry meaning

### Compaction Triggers

Set explicit triggers for compression operations:

```python
def should_compact(context_state):
    """Determine if compaction is needed based on context metrics."""
    triggers = {
        "capacity_threshold": context_state.token_count > context_state.max_tokens * 0.65,
        "turn_count": context_state.turn_count > 20,
        "tool_output_ratio": context_state.tool_output_tokens / context_state.total_tokens > 0.4,
        "stale_content": context_state.oldest_uncompressed_age > 10,  # turns
    }
    return any(triggers.values())
```

Trigger compaction before the model's attention degrades, not after. The compaction operation itself requires attention — performing it on already-degraded context produces worse summaries.

### Handoff Summaries

Design handoff summaries for agent-to-agent or session-to-session transitions:

**Structure:**
```markdown
## Task State
- Current objective: [what the agent is trying to accomplish]
- Progress: [what has been done, what remains]
- Blockers: [known issues or dependencies]

## Key Decisions
- [Decision]: [rationale] (turn N)

## Critical Context
- [Facts, constraints, or preferences that must be preserved]

## File State
- [Modified files and their current state]
- [Pending changes or uncommitted work]
```

Keep handoff summaries under 500 tokens. If more detail is needed, persist it to a file and include the file path in the summary.

### Compression Quality Verification

After compression, verify that the compressed context retains sufficient signal:

1. **Task continuity test** — Can the agent continue the current task with only the compressed context?
2. **Decision consistency test** — Would the agent make the same key decisions with compressed vs. full context?
3. **Information recovery test** — Can critical facts be extracted from the compressed context?
4. **Regression check** — Does the compressed context introduce contradictions or lose constraints?

## Gotchas

- **Premature compression loses rationale**: Compressing too early discards decision rationale that becomes critical when debugging later steps. Preserve "why" even when discarding "how."
- **Compression cascades**: Each compression pass loses information. After 3-4 rounds of compression, the remaining context may be too abstracted to be useful. Monitor compression depth.
- **Summary hallucination**: Models sometimes introduce facts during summarization that weren't in the original content. Verify compressed summaries against source material.
- **Loss of negative information**: Compression tends to preserve what was done, not what was explicitly avoided. Track "do not do X" constraints separately from positive decisions.

## Integration

- `context-fundamentals` provides the attention budget model that motivates compression.
- `context-degradation` identifies the failure patterns that compression prevents.
- `context-optimization` provides complementary token-efficiency tactics.
- `filesystem-context` provides offloading as an alternative to compression.
- `memory-systems` provides cross-session persistence that works alongside compression.
