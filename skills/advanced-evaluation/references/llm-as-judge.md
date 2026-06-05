# LLM-as-Judge Reference

## Evaluator Bias Taxonomy

| Bias | Description | Mitigation |
|------|-------------|-----------|
| Position | Preferring first or last option | Swap order, require agreement |
| Verbosity | Preferring longer responses | Normalize length, instruct to ignore |
| Self-preference | Preferring same-family outputs | Use cross-family evaluators |
| Anchoring | Influenced by scale presentation | Vary scales, use pairwise |
| Sycophancy | Agreeing with provided labels | Hide labels during evaluation |
| Recency | Overweighting recent examples | Randomize presentation order |

## Rubric Design Template

```yaml
dimension: "instruction_following"
levels:
  5: "All instructions followed precisely, including edge cases"
  4: "Most instructions followed, minor omissions"
  3: "Core instructions followed, some deviations"
  2: "Partial instruction following, significant gaps"
  1: "Instructions largely ignored or misinterpreted"
examples:
  5: "When asked for JSON output with 3 fields, returns valid JSON with all 3 fields"
  3: "Returns JSON but missing one required field"
  1: "Returns plain text instead of JSON"
```

## Reliability Measurement

- **Cohen's Kappa** for inter-rater agreement (>0.6 is good, >0.8 is excellent)
- **Cronbach's Alpha** for internal consistency of multi-dimension rubrics
- **Spearman correlation** with human expert scores (>0.7 is acceptable)
