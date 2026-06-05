# Harness Pattern Reference

## Harness Component Checklist

- [ ] **Execution controller**: Start/pause/resume/terminate
- [ ] **Time limits**: Maximum wall-clock time per session
- [ ] **Token budgets**: Maximum tokens per session/turn
- [ ] **Action limits**: Maximum tool calls per session
- [ ] **Evaluation gates**: Deterministic checks on every output
- [ ] **Safety boundaries**: Human approval for destructive actions
- [ ] **Novelty detection**: Prevent repetitive loops
- [ ] **State checkpoints**: Periodic state snapshots for rollback
- [ ] **Durable logging**: All actions logged for post-hoc analysis
- [ ] **Failure recovery**: Graceful degradation on errors

## Approval Boundary Framework

```
Risk Level 1 (Auto-approve): Read-only operations
Risk Level 2 (Log + approve): Write operations within project scope
Risk Level 3 (Review + approve): Operations affecting external systems
Risk Level 4 (Human approval required): Destructive or irreversible operations
Risk Level 5 (Block): Operations outside defined scope
```

## Logging Schema
```json
{
  "session_id": "uuid",
  "turn": 42,
  "timestamp": "ISO-8601",
  "action_type": "tool_call | decision | checkpoint | error",
  "action": {"tool": "search_files", "params": {"query": "auth"}},
  "result": {"status": "success", "output_tokens": 150},
  "evaluation": {"deterministic_pass": true, "quality_score": 0.85},
  "state_hash": "sha256-of-current-state"
}
```
