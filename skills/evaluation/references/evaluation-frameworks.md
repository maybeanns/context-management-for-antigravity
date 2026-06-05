# Evaluation Framework Reference

## Evaluation Layer Stack

```
Layer 3: LLM-Based (advanced-evaluation)
  └── Semantic quality, coherence, instruction-following
Layer 2: Statistical
  └── Success rates, score distributions, trend analysis
Layer 1: Deterministic
  └── Format validation, schema compliance, constraint checks
```

## Common Evaluation Pitfalls

1. **Testing happy paths only** — Always include adversarial and edge cases
2. **Exact-match assertions** — Use structural/semantic checks for non-deterministic outputs
3. **Single-metric optimization** — Use multiple complementary metrics
4. **Static test sets** — Refresh from production data regularly
5. **Ignoring latency** — Fast-but-wrong agents aren't useful

## Regression Test Fixture Format
```json
{
  "id": "test-001",
  "description": "Basic summarization task",
  "input": {"text": "...", "instruction": "Summarize in 2 sentences"},
  "expected": {
    "format": "text",
    "max_length": 200,
    "must_contain": ["key_concept_1"],
    "must_not_contain": ["irrelevant_topic"]
  },
  "tags": ["summarization", "regression", "v2.0"]
}
```
