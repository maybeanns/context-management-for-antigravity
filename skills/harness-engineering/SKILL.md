---
name: harness-engineering
description: This skill should be used for designing autonomous agent harnesses — the operating loop that manages agent execution with locked evaluation metrics, durable logs, novelty gates, rollback mechanisms, human approval boundaries, and safety constraints. Route evaluation framework design to evaluation, LLM-as-judge techniques to advanced-evaluation, and multi-agent coordination to multi-agent-patterns.
---

# Harness Engineering for Autonomous Agents

Design the operating loop that wraps an autonomous agent — the harness that manages execution, evaluates outputs, enforces safety, and provides human oversight. A well-designed harness transforms an unreliable agent into a reliable system by adding deterministic guardrails around non-deterministic behavior. The harness is the engineering, the agent is the capability.

## When to Activate

Activate this skill when:
- Designing autonomous agent execution loops
- Implementing rollback and recovery mechanisms for agent failures
- Building novelty gates to prevent repetitive agent behavior
- Defining human approval boundaries for high-risk agent actions
- Designing durable logging for post-hoc analysis of agent behavior
- Locking evaluation metrics to prevent metric gaming

Do not activate this skill for adjacent work owned by other skills:
- Building evaluation checks and metrics: `evaluation`.
- Implementing LLM-as-judge scoring: `advanced-evaluation`.
- Designing multi-agent coordination protocols: `multi-agent-patterns`.
- Building hosted sandbox infrastructure: `hosted-agents`.

## Core Concepts

The harness is the deterministic wrapper around the non-deterministic agent. It manages five concerns:

1. **Execution control** — Start, pause, resume, and terminate agent sessions. Enforce time limits, token budgets, and action counts.
2. **Evaluation gates** — Check agent outputs against quality criteria before accepting them. Gate on deterministic checks (format, constraints) and statistical checks (quality scores).
3. **Safety boundaries** — Define actions that require human approval (destructive operations, external communications, resource-intensive tasks). Block unauthorized actions.
4. **State management** — Log all actions, tool calls, and decisions for debugging. Enable rollback to previous states when failures are detected.
5. **Novelty detection** — Detect and prevent repetitive behavior loops where agents retry the same failed approach.

## Detailed Topics

### The Operating Loop

```python
class AgentHarness:
    def run(self, task: str, max_iterations: int = 50):
        state = self.initialize(task)
        for iteration in range(max_iterations):
            # 1. Agent proposes action
            action = self.agent.propose(state)

            # 2. Safety check
            if self.requires_approval(action):
                if not self.get_human_approval(action):
                    state = self.handle_rejection(state, action)
                    continue

            # 3. Novelty check
            if self.is_repetitive(action, state.action_history):
                state = self.force_exploration(state)
                continue

            # 4. Execute action
            result = self.execute(action)
            state = self.update_state(state, action, result)

            # 5. Evaluation gate
            if self.is_complete(state):
                evaluation = self.evaluate(state)
                if evaluation["pass"]:
                    return self.finalize(state)
                else:
                    state = self.handle_failure(state, evaluation)

            # 6. Checkpoint
            self.checkpoint(state)

        return self.timeout_handler(state)
```

### Locked Metrics

Lock evaluation metrics before the agent starts to prevent gaming:

```python
class LockedMetrics:
    def __init__(self, metrics: dict):
        self._metrics = frozenset(metrics.items())
        self._hash = hashlib.sha256(str(self._metrics).encode()).hexdigest()

    def evaluate(self, output):
        """Evaluate against immutable metric definitions."""
        results = {}
        for name, config in self._metrics:
            results[name] = config["evaluator"](output)
        return results

    def verify_integrity(self):
        """Verify metrics haven't been tampered with."""
        current_hash = hashlib.sha256(str(self._metrics).encode()).hexdigest()
        return current_hash == self._hash
```

### Novelty Gates

Prevent agents from repeating failed approaches:

```python
class NoveltyGate:
    def __init__(self, similarity_threshold: float = 0.85):
        self.history = []
        self.threshold = similarity_threshold

    def is_novel(self, action: dict) -> bool:
        action_repr = self.encode(action)
        for past_action in self.history[-10:]:  # Check recent history
            if self.similarity(action_repr, past_action) > self.threshold:
                return False
        self.history.append(action_repr)
        return True

    def force_exploration(self, state) -> str:
        """Generate a prompt that forces the agent to try a different approach."""
        failed_approaches = self.summarize_failures(self.history)
        return f"Previous approaches failed: {failed_approaches}. Try a fundamentally different strategy."
```

### Rollback Mechanisms

Checkpoint state and roll back on failure:

```python
class StateManager:
    def checkpoint(self, state, label: str = None):
        """Save a recoverable checkpoint."""
        self.checkpoints.append({
            "state": deepcopy(state),
            "label": label or f"checkpoint_{len(self.checkpoints)}",
            "timestamp": datetime.utcnow()
        })

    def rollback(self, to_label: str = None):
        """Restore state from a checkpoint."""
        if to_label:
            target = next(c for c in self.checkpoints if c["label"] == to_label)
        else:
            target = self.checkpoints[-1]
        return deepcopy(target["state"])
```

### Human Approval Boundaries

Define which actions require human approval:

| Action Category | Approval Required | Rationale |
|----------------|-------------------|-----------|
| File read | No | Non-destructive |
| File write (existing) | Conditional | May overwrite work |
| File delete | Yes | Destructive |
| External API call | Conditional | Cost/privacy implications |
| Package install | Yes | Security implications |
| Deploy to production | Yes | Business impact |

## Gotchas

- **Harness overhead**: Over-engineered harnesses can slow agents significantly. Measure harness overhead as a percentage of total execution time and optimize hot paths.
- **False novelty triggers**: Superficially similar but meaningfully different actions may be blocked by overly aggressive novelty gates. Use semantic similarity, not string matching.
- **Checkpoint storage**: Frequent checkpointing of large states consumes significant memory/storage. Implement tiered checkpointing (frequent lightweight + periodic full).
- **Approval fatigue**: Too many approval requests cause humans to approve without reviewing. Set approval thresholds that are meaningful, not comprehensive.

## Integration

- `evaluation` provides the evaluation frameworks used within harness gates.
- `advanced-evaluation` provides LLM-based evaluation for subjective quality.
- `multi-agent-patterns` covers coordination when multiple agents operate within harnesses.
- `hosted-agents` provides the sandboxed runtime where harnesses operate.
