# BDI Ontology Reference

## Core BDI Components

### Belief Structure
```python
@dataclass
class Belief:
    content: str          # What is believed
    source: str           # Where the belief came from
    confidence: float     # 0.0 to 1.0
    timestamp: datetime   # When the belief was formed
    invalidated: bool     # Whether the belief has been contradicted
```

### Desire Structure
```python
@dataclass
class Desire:
    description: str      # What the agent wants to achieve
    type: str             # goal, constraint, preference
    priority: int         # Higher = more important
    feasible: bool        # Whether achievable given current beliefs
    deadline: datetime    # Optional deadline
```

### Intention Structure
```python
@dataclass
class Intention:
    desire: Desire        # The desire this intention serves
    plan: Plan            # The plan being followed
    status: str           # active, suspended, completed, failed
    started: datetime     # When the intention was formed
    progress: float       # 0.0 to 1.0
```

## BDI Reasoning Cycle

```
1. PERCEIVE  → Update beliefs from observations
2. DELIBERATE → Select desires to pursue (based on beliefs)
3. PLAN      → Find/generate plans for selected desires
4. EXECUTE   → Carry out next plan step
5. MONITOR   → Check if intentions are still feasible
6. REVISE    → Drop infeasible intentions, reconsider desires
7. REPEAT    → Return to step 1
```

## RDF-to-BDI Mapping

| RDF Element | BDI Component | Mapping Rule |
|------------|--------------|-------------|
| Subject-Predicate-Object | Belief | Each triple becomes a belief with confidence from source |
| rdf:type assertions | Belief (categorization) | Entity type beliefs |
| owl:sameAs | Belief (identity) | Entity resolution beliefs |
| Reasoning goals | Desire | Extracted from task description |
| Planned actions | Intention | Generated from plan library |
