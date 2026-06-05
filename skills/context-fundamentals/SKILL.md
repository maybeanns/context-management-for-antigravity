---
name: context-fundamentals
description: This skill should be used to explain or reason about the foundational concepts of context engineering — what context is, the anatomy of a context window, how attention mechanics work, the U-shaped attention curve, why context quality matters more than quantity, and the mental models needed to interpret every other context-engineering decision. Use this for conceptual explanation, onboarding, and background reading. Route operational work to the specialized skills — debugging attention failures goes to context-degradation, token-efficiency work goes to context-optimization, conversation summarization goes to context-compression, and project-shape decisions go to project-development.
---

# Context Engineering Fundamentals

Context is the complete state available to a language model at inference time: system instructions, tool definitions, retrieved documents, message history, and tool outputs. Context engineering is the discipline of curating the smallest high-signal token set that maximizes the likelihood of desired outcomes.

This skill is the conceptual foundation that every other skill in the collection builds on. It explains what context is, how attention mechanics work, why context quality matters more than quantity, and the mental models needed to interpret every other context-engineering decision. It does not own operational work: debugging attention failures belongs to `context-degradation`, token-efficiency tactics belong to `context-optimization`, conversation summarization belongs to `context-compression`, file-based offloading belongs to `filesystem-context`, and project-shape decisions belong to `project-development`.

## When to Activate

Activate this skill when the work is conceptual:

- Explaining what context is and how attention mechanics constrain agent behavior.
- Onboarding new contributors who need the mental models before diving into operational skills.
- Reasoning about a context-related design decision from first principles (what does this constraint mean, why does this trade-off exist) before picking a specific tactic.
- Writing or reviewing documentation that needs to ground operational guidance in the underlying mechanics.

Do not activate this skill for operational work. The specialized skills handle the doing:

- Diagnosing lost-in-middle, context poisoning, or attention failures: `context-degradation`.
- Reducing token cost via masking, partitioning, prefix caching, budgets: `context-optimization`.
- Compressing a long session into a handoff summary: `context-compression`.
- Offloading large tool outputs or maintaining a durable scratchpad: `filesystem-context`.
- Deciding the shape of an LLM project or pipeline: `project-development`.

## Core Concepts

Treat context as a finite attention budget, not a storage bin. Every token added competes for the model's attention and depletes a budget that cannot be refilled mid-inference. The engineering problem is maximizing utility per token against three constraints: the hard token limit, the softer effective-capacity ceiling, and the U-shaped attention curve that penalizes information placed in the middle of context.

Apply four principles when assembling context:

1. **Informativity over exhaustiveness** — include only what matters for the current decision; design systems that can retrieve additional information on demand.
2. **Position-aware placement** — place critical constraints at the beginning and end of context because long-context evaluations show middle-position information is less reliably recovered than edge-position information.
3. **Progressive disclosure** — load skill names and summaries at startup; load full content only when a skill activates for a specific task.
4. **Iterative curation** — context engineering is not a one-time prompt-writing exercise but an ongoing discipline applied every time content is passed to the model.

## Detailed Topics

### The Anatomy of Context

**System Prompts**
Organize system prompts into distinct sections using XML tags or Markdown headers (background, instructions, tool guidance, output format). System prompts persist throughout the conversation, so place the most critical constraints at the beginning and end where attention is strongest.

Calibrate instruction altitude to balance two failure modes. Too-low altitude hardcodes brittle logic that breaks when conditions shift. Too-high altitude provides vague guidance that fails to give concrete signals for desired behavior. Aim for heuristic-driven instructions: specific enough to guide behavior, flexible enough to generalize — for example, numbered steps with room for judgment at each step.

Start minimal, then add instructions reactively based on observed failure modes rather than preemptively stuffing edge cases. Curate diverse, canonical few-shot examples that portray expected behavior instead of listing every possible scenario.

**Tool Definitions**
Write tool descriptions that answer three questions: what the tool does, when to use it, and what it returns. Include usage context, parameter defaults, and error cases — agents cannot disambiguate tools that a human engineer cannot disambiguate either.

Keep the tool set minimal. Consolidate overlapping tools because bloated tool sets create ambiguous decision points and consume disproportionate context after JSON serialization (tool schemas typically inflate 2-3x compared to equivalent plain-text descriptions).

**Retrieved Documents**
Maintain lightweight identifiers (file paths, stored queries, web links) and load data into context dynamically using just-in-time retrieval. This mirrors human cognition — maintain an index, not a copy. Strong identifiers (e.g., `customer_pricing_rates.json`) let agents locate relevant files even without search tools; weak identifiers (e.g., `data/file1.json`) force unnecessary loads.

When chunking large documents, split at natural semantic boundaries (section headers, paragraph breaks) rather than arbitrary character limits that sever mid-concept.

**Message History**
Message history serves as the agent's scratchpad memory for tracking progress, maintaining task state, and preserving reasoning across turns. For long-running tasks, it can grow to dominate context usage — monitor and apply compaction before it crowds out active instructions.

Cyclically refine history: once a tool has been called deep in the conversation, the raw result rarely needs to remain verbatim. Replace stale tool outputs with compact summaries or references to files where full results are stored.

### Attention Mechanics and the U-Curve

The U-shaped attention curve is not a model bug — it is a consequence of how transformer attention works. The first token (often BOS or system prompt start) acts as an "attention sink" absorbing disproportionate attention. Tokens at the end benefit from recency. Middle tokens compete with both edges for attention weight.

Practical implications:
- **First position**: System-level constraints, identity, and critical rules
- **Last position**: Current task instructions, the most recent user query
- **Middle position**: Reference material, history, retrieved documents (lowest priority)

The effective capacity of a context window is always less than the raw token limit. A 128K-token window does not mean 128K tokens of useful capacity — beyond a model-specific threshold, additional tokens dilute attention for earlier content.

### The Four Context Engineering Principles

**Principle 1: Informativity**
Every token must earn its place. Before adding information to context, ask: "Will the model's output measurably improve with this content present?" If the answer is uncertain, keep the information behind a tool call rather than pre-loading it.

**Principle 2: Position-Aware Placement**
Structure context like a newspaper: headline (critical constraints) at the top, conclusion (current task) at the bottom, supporting details in the middle. This aligns with the U-shaped attention curve and ensures the most important information receives the most attention.

**Principle 3: Progressive Disclosure**
Design context systems that load information on demand rather than all at once. Skills load names first, then full content when activated. Tool outputs are summarized unless the full result is needed. Retrieved documents are loaded only when the current task requires them.

**Principle 4: Iterative Curation**
Context engineering is a continuous process, not a one-time setup. Monitor agent performance, identify failure modes, and adjust context composition accordingly. Every prompt iteration, every tool call response, every retrieved document is an opportunity to improve signal-to-noise ratio.

## Gotchas

- **The "more is better" fallacy**: Adding more context does not make agents smarter. Beyond the effective capacity threshold, additional tokens actively harm performance by diluting attention for critical content.
- **Tool schema bloat**: JSON-serialized tool schemas inflate 2-3x compared to equivalent plain-text descriptions. A catalog of 20 tools can consume 10-15K tokens before any user content is loaded.
- **Instruction drift**: As system prompts grow through iterative additions, early instructions lose effectiveness. Periodically audit and consolidate instructions rather than only appending.
- **Phantom context**: Agents may behave as if information is present that was actually in a previous turn but has since been compacted. Always verify that critical context is explicitly present, not assumed.

## Integration

- `context-degradation` builds on these fundamentals to diagnose specific failure patterns.
- `context-optimization` applies tactical techniques informed by these principles.
- `context-compression` implements compression strategies grounded in the attention budget model.
- `tool-design` applies the tool definition principles outlined here to specific tool authoring.
- `project-development` uses task-model fit analysis that depends on understanding context constraints.

## References

- `references/attention-mechanics.md` — Deep-dive on transformer attention patterns, the attention sink phenomenon, and experimental evidence for the U-curve.
