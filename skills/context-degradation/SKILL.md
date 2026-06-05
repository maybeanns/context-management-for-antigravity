---
name: context-degradation
description: This skill should be used for diagnosing and mitigating context degradation — lost-in-middle failures, context poisoning, context clash, context confusion, attention-pattern issues, and agent performance degradation caused by accumulated or conflicting context. Route foundational conceptual work to context-fundamentals, token-efficiency tactics to context-optimization, and compression strategy design to context-compression.
---

# Context Degradation Patterns

Diagnose and fix context failures before they cascade. Context degradation is not binary — it is a continuum that manifests through five distinct, predictable patterns: lost-in-middle, poisoning, distraction, confusion, and clash. Each pattern has specific detection signals and mitigation strategies. Treat degradation as an engineering problem with measurable thresholds, not an unpredictable failure mode.

## When to Activate

Activate this skill when:
- Agent performance degrades unexpectedly during long conversations
- Debugging cases where agents produce incorrect or irrelevant outputs
- Designing systems that must handle large contexts reliably
- Evaluating context engineering choices for production systems
- Investigating "lost in middle" phenomena in agent outputs
- Analyzing context-related failures in agent behavior

Do not activate this skill for adjacent work owned by other skills:
- Explaining foundational context mechanics without an active failure: `context-fundamentals`.
- Applying token-efficiency tactics after the failure pattern is known: `context-optimization`.
- Designing a compression or handoff summary strategy: `context-compression`.
- Persisting large outputs, logs, or scratch state outside the prompt: `filesystem-context`.

## Core Concepts

Structure context placement around the attention U-curve: beginning and end positions receive reliable attention, while middle positions suffer materially reduced recall accuracy in long-context experiments. This is not a model bug but a consequence of attention mechanics — the first token acts as an "attention sink" that absorbs disproportionate attention budget, leaving middle tokens under-attended as context grows.

Treat context poisoning as a circuit breaker problem. Once a hallucination, tool error, or incorrect retrieved fact enters context, it compounds through repeated self-reference. A poisoned goals section causes every downstream decision to reinforce incorrect assumptions. Detection requires tracking claim provenance; recovery requires truncating to before the poisoning point or restarting with verified-only context.

Filter aggressively before loading context — even a single irrelevant document measurably degrades performance on relevant tasks. Models cannot "skip" irrelevant context; they must attend to everything provided, creating attention competition between relevant and irrelevant content. Move information that might be needed but is not immediately relevant behind tool calls instead of pre-loading it.

Isolate task contexts to prevent confusion. When context contains multiple task types or switches between objectives, models incorporate constraints from the wrong task, call tools appropriate for a different context, or blend requirements from multiple sources. Explicit task segmentation with separate context windows eliminates cross-contamination.

Resolve context clash through priority rules, not accumulation. When multiple correct-but-contradictory sources appear in context, models cannot determine which applies. Mark contradictions explicitly, establish source precedence, and filter outdated versions before they enter context.

## Detailed Topics

### Lost-in-Middle: Detection and Placement Strategy

Place critical information at the beginning and end of context, never in the middle. The U-shaped attention curve means middle-positioned information suffers 10-40% reduced recall accuracy. For contexts over 4K tokens, this effect becomes significant.

Use summary structures that surface key findings at attention-favored positions. Add explicit section headers and structural markers — these help models navigate long contexts by creating attention anchors. When a document must be included in full, prepend a summary of its key points and append the critical conclusions.

Monitor for lost-in-middle symptoms: correct information exists in context but the model ignores it, responses contradict provided data, or the model "forgets" instructions given earlier in a long prompt.

### Context Poisoning: Prevention and Recovery

Validate all external inputs before they enter context. Tool outputs, retrieved documents, and model-generated summaries are the three primary poisoning vectors. Each introduces unverified claims that subsequent reasoning treats as ground truth.

Detect poisoning through these signals: degraded output quality on previously-successful tasks, tool misalignment (wrong tools or parameters), and hallucinations that persist despite explicit correction. When these cluster, suspect poisoning rather than model capability issues.

Recover by removing poisoned content, not by adding corrections on top. Truncate to before the poisoning point, restart with clean context preserving only verified information, or explicitly mark the poisoned section and request re-evaluation from scratch. Layering corrections over poisoned context rarely works — the original errors retain attention weight.

### Context Distraction: Curation Over Accumulation

Curate what enters context rather than relying on models to ignore irrelevant content. Research shows even a single distractor document triggers measurable performance degradation — the effect follows a step function, not a linear curve. Multiple distractors compound the problem.

Apply relevance filtering before loading retrieved documents. Use namespacing and structural organization to make section boundaries clear. Prefer tool-call-based access over pre-loading: store reference material behind retrieval tools so it enters context only when directly relevant to the current reasoning step.

### Context Confusion: Task Isolation

Segment different tasks into separate context windows. Context confusion is distinct from distraction — it concerns the model applying wrong-context constraints to the current task, not just attention dilution. Signs include responses addressing the wrong aspect of a query, tool calls appropriate for a different task, and outputs mixing requirements from multiple sources.

Implement clear transitions between task contexts. Use state management that isolates objectives, constraints, and tool definitions per task. When task-switching within a single session is unavoidable, use explicit "context reset" markers that signal which constraints apply to the current segment.

### Context Clash: Conflict Resolution Protocols

Establish source priority rules before conflicts arise. Context clash differs from poisoning — multiple pieces of information are individually correct but mutually contradictory (version conflicts, perspective differences, multi-source retrieval with divergent facts).

Implement version filtering to exclude outdated information before it enters context. When contradictions are unavoidable, mark them explicitly with structured conflict annotations: state what conflicts, which source each claim comes from, and which source has priority. Without explicit priority, models arbitrarily choose between contradictory facts.

## Gotchas

- **Correction stacking fails**: Adding "Actually, ignore the above and do X instead" rarely overrides poisoned context. The model attends to both the poison and the correction, blending them unpredictably.
- **Distraction is a step function**: Performance doesn't degrade linearly with irrelevant content. Even one distractor document causes a measurable drop; additional distractors compound but don't linearly increase the damage.
- **Confusion mimics capability failure**: When agents produce incorrect outputs due to context confusion, it looks like the model isn't smart enough. Always check for mixed task contexts before concluding the model lacks capability.
- **Clash is invisible without tracking**: Contradictory facts from different sources look identical once loaded into context. Without explicit source annotations, there is no way to detect which fact the model chose or why.

## Integration

- `context-fundamentals` provides the attention mechanics theory this skill operationalizes.
- `context-optimization` applies tactical fixes once this skill has identified the degradation pattern.
- `context-compression` prevents degradation by reducing context volume proactively.
- `filesystem-context` provides offloading patterns that mitigate distraction and poisoning.
