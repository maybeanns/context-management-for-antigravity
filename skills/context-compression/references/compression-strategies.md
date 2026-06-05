# Compression Strategy Reference

## Strategy Comparison Matrix

| Strategy | Fidelity | Token Savings | Implementation Complexity | Best For |
|----------|----------|---------------|--------------------------|----------|
| Full verbatim | 100% | 0% | None | Active task context |
| Selective retention | 80-95% | 30-50% | Low | Recent history |
| Hierarchical summary | 60-80% | 50-70% | Medium | Session history |
| Key-fact extraction | 40-60% | 70-90% | Medium | Cross-session memory |
| Lossy truncation | Variable | Variable | Low | Emergency compaction |

## Compression Quality Metrics

- **Fact preservation rate**: % of original facts recoverable from compressed version
- **Decision reversibility**: Can key decisions be re-derived from compressed context?
- **Task continuity**: Can work continue without referencing the uncompressed original?
- **Contradiction rate**: Does compression introduce facts not in the original?

## Handoff Summary Templates

### Agent-to-Agent Handoff
```
HANDOFF: [source_agent] -> [target_agent]
TASK: [current objective]
PROGRESS: [completed steps / total steps]
CRITICAL CONTEXT: [must-preserve facts]
DECISIONS MADE: [key decisions + rationale]
PENDING: [next steps]
FILES: [modified file paths]
```

### Session-to-Session Handoff
```
SESSION SUMMARY: [date/time]
OBJECTIVE: [what was being worked on]
COMPLETED: [what was finished]
IN PROGRESS: [what was partially done]
BLOCKED: [what couldn't be done and why]
KEY FACTS: [established facts to preserve]
NEXT SESSION: [recommended starting point]
```
