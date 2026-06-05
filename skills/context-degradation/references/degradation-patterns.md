# Degradation Pattern Reference

## Pattern Taxonomy

| Pattern | Root Cause | Detection Signal | Recovery Strategy |
|---------|-----------|-----------------|-------------------|
| Lost-in-Middle | Attention U-curve | Correct info ignored | Reposition to edges |
| Poisoning | Error propagation | Quality degradation | Truncate + restart |
| Distraction | Irrelevant content | Attention dilution | Filter before loading |
| Confusion | Task mixing | Wrong-context actions | Isolate task contexts |
| Clash | Contradictory sources | Inconsistent outputs | Priority rules |

## Detailed Detection Checklists

### Lost-in-Middle Checklist
- [ ] Does the correct answer exist in context?
- [ ] Is it positioned in the middle 50% of context?
- [ ] Does moving it to the end fix the issue?
- [ ] Is the total context over 4K tokens?

### Poisoning Checklist
- [ ] Did output quality degrade on previously-working tasks?
- [ ] Can you identify a specific turn where quality dropped?
- [ ] Does the model repeat incorrect claims introduced earlier?
- [ ] Does restarting with clean context fix the issue?

### Distraction Checklist
- [ ] Are there documents in context not relevant to the current task?
- [ ] Does removing irrelevant documents improve performance?
- [ ] Is the model attending to the wrong sections?

### Confusion Checklist
- [ ] Does context contain multiple task types?
- [ ] Is the model applying constraints from a different task?
- [ ] Does isolating to a single task fix the issue?

### Clash Checklist
- [ ] Are there contradictory facts from different sources?
- [ ] Is the model inconsistently choosing between contradictory facts?
- [ ] Does establishing explicit source priority fix the issue?
