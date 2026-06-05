---
name: bdi-mental-states
description: This skill should be used for modeling agent cognitive states using formal Belief-Desire-Intention (BDI) ontology — transforming external RDF context into explicit mental states, designing deliberative reasoning pipelines, enabling explainable agent decisions, and implementing plan libraries. Route multi-agent coordination to multi-agent-patterns, memory architecture to memory-systems, and evaluation of agent reasoning to evaluation.
---

# BDI Mental State Modeling

Transform unstructured context into explicit mental states using the Belief-Desire-Intention (BDI) framework. BDI provides a formal ontology for modeling what an agent believes about the world, what it wants to achieve, and what it has committed to doing. This framework enables deliberative reasoning (choosing actions based on beliefs and goals) and explainable decision-making (every action traces to explicit beliefs, desires, and intentions).

## When to Activate

Activate this skill when:
- Modeling agent reasoning with formal cognitive structures
- Transforming RDF or structured external context into agent mental states
- Designing plan libraries for deliberative agent architectures
- Implementing explainable decision-making in agent systems
- Building agents that must reason about their own beliefs and goals
- Analyzing the gap between agent beliefs and ground truth

Do not activate this skill for adjacent work owned by other skills:
- Multi-agent coordination and handoff protocols: `multi-agent-patterns`.
- Designing memory persistence and retrieval: `memory-systems`.
- Evaluating agent output quality: `evaluation`.
- Understanding general context mechanics: `context-fundamentals`.

## Core Concepts

The BDI framework decomposes agent cognition into three components:

**Beliefs** — The agent's model of the world. What it thinks is true based on observations, tool outputs, and prior knowledge. Beliefs can be incorrect, outdated, or incomplete. The gap between beliefs and reality is a critical failure vector.

**Desires** — The agent's objectives. What it wants to achieve, ordered by priority. Desires can be conflicting — the BDI framework provides mechanisms for resolving conflicts through priority ordering and feasibility analysis.

**Intentions** — The agent's commitments. What it has decided to do and the plan it will follow. Intentions persist across reasoning cycles until the goal is achieved, the goal becomes impossible, or a higher-priority goal supersedes it.

## Detailed Topics

### From Context to Mental States

Transform raw context into BDI structures:

```python
class BDIAgent:
    def __init__(self):
        self.beliefs = BeliefBase()
        self.desires = DesireSet()
        self.intentions = IntentionStack()

    def perceive(self, observations: list):
        """Update beliefs from new observations."""
        for obs in observations:
            belief = self.interpret(obs)
            self.beliefs.update(belief)

    def deliberate(self):
        """Select desires to pursue based on current beliefs."""
        feasible_desires = [d for d in self.desires if self.is_feasible(d, self.beliefs)]
        prioritized = sorted(feasible_desires, key=lambda d: d.priority, reverse=True)
        return prioritized[0] if prioritized else None

    def plan(self, desire):
        """Generate or retrieve a plan to achieve the selected desire."""
        applicable_plans = self.plan_library.match(desire, self.beliefs)
        selected = self.select_plan(applicable_plans, self.beliefs)
        self.intentions.push(Intention(desire=desire, plan=selected))

    def execute(self):
        """Execute the current intention's next action."""
        if self.intentions.empty():
            return None
        current = self.intentions.peek()
        action = current.plan.next_step()
        result = self.perform(action)
        self.perceive([result])
        if current.plan.is_complete():
            self.intentions.pop()
        return result
```

### RDF Context Integration

Transform RDF triples into beliefs:

```python
def rdf_to_beliefs(rdf_graph) -> list:
    """Convert RDF triples to BDI belief structures."""
    beliefs = []
    for subject, predicate, obj in rdf_graph:
        belief = Belief(
            content=f"{subject} {predicate} {obj}",
            source="rdf_context",
            confidence=0.9,  # External knowledge
            timestamp=datetime.utcnow()
        )
        beliefs.append(belief)
    return beliefs
```

### Plan Libraries

Maintain a library of reusable plans indexed by the desires they satisfy:

```python
class PlanLibrary:
    def __init__(self):
        self.plans = {}

    def register(self, plan_id: str, applicable_desire: str,
                 preconditions: dict, steps: list):
        self.plans[plan_id] = {
            "desire": applicable_desire,
            "preconditions": preconditions,
            "steps": steps
        }

    def match(self, desire, beliefs) -> list:
        """Find plans that satisfy the desire given current beliefs."""
        candidates = [p for p in self.plans.values()
                     if p["desire"] == desire.type]
        return [p for p in candidates
               if self.preconditions_met(p["preconditions"], beliefs)]
```

### Explainable Decision Traces

Every agent action should trace back to explicit beliefs, desires, and intentions:

```python
class DecisionTrace:
    def record(self, action, beliefs_used, desire, intention, plan_step):
        return {
            "action": action,
            "because_I_believe": [b.content for b in beliefs_used],
            "to_achieve": desire.description,
            "as_part_of": intention.plan.name,
            "step": plan_step.description,
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Gotchas

- **Belief-reality gap**: Agents may act on beliefs that are no longer true. Implement belief revision mechanisms that update or invalidate beliefs when contradicting evidence appears.
- **Intention persistence trap**: Agents may continue pursuing intentions that are no longer feasible. Implement periodic intention review that checks feasibility against current beliefs.
- **Over-formalization**: Not every agent needs full BDI modeling. Simple task-completion agents work fine without formal cognitive architecture. Use BDI when explainability or complex goal management is required.
- **Plan library completeness**: Agents with incomplete plan libraries fail silently when no applicable plan exists. Implement fallback strategies for unplanned situations.

## Integration

- `context-fundamentals` explains how beliefs and desires map to context components.
- `multi-agent-patterns` covers coordination between BDI agents.
- `memory-systems` provides persistence for beliefs and plan libraries.
- `evaluation` covers testing agent reasoning quality.
- `harness-engineering` provides the operating loop that manages BDI agent execution.
