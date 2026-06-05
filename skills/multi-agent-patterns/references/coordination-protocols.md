# Multi-Agent Coordination Protocols

## Pattern Selection Decision Tree

```
Is single-agent context sufficient?
├── Yes → Use single agent
└── No → Are subtasks independent?
    ├── Yes → Are they parallelizable?
    │   ├── Yes → Parallel workers with aggregator
    │   └── No → Sequential chain
    └── No → Is decomposition clear?
        ├── Yes → Supervisor/Orchestrator
        └── No → Is the problem space well-defined?
            ├── Yes → Hierarchical
            └── No → Peer-to-peer/Swarm
```

## Coordination Protocol Templates

### Supervisor Protocol
1. Supervisor receives user task
2. Supervisor decomposes into subtasks
3. Supervisor assigns subtasks to workers
4. Workers execute independently
5. Workers return results to supervisor
6. Supervisor aggregates and synthesizes
7. Supervisor delivers final output

### Swarm Protocol
1. Initial agent receives user task
2. Agent evaluates: can I handle this?
3. If yes: execute and return
4. If no: identify best-fit agent and handoff
5. Handoff includes: task, context summary, constraints
6. Receiving agent repeats from step 2

### Hierarchical Protocol
1. Strategy layer defines high-level plan
2. Planning layer decomposes into concrete steps
3. Execution layer assigns steps to workers
4. Workers execute and report results
5. Execution layer aggregates worker results
6. Planning layer evaluates progress
7. Strategy layer adjusts plan if needed

## Token Cost Benchmarks

| Pattern | Coordination Overhead | Typical Total Multiplier |
|---------|----------------------|-------------------------|
| Single agent | 0% | 1x |
| 2-agent chain | 15-25% | 2.2-2.5x |
| 3-worker supervisor | 30-50% | 4-6x |
| 5-worker swarm | 40-70% | 8-15x |
| 3-layer hierarchy | 50-80% | 10-25x |
