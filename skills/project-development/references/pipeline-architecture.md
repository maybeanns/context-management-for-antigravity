# Pipeline Architecture Reference

## Pipeline Selection Guide

| Task Characteristics | Recommended Pipeline | Rationale |
|---------------------|---------------------|-----------|
| Single input → single output | Single-pass | Minimal overhead |
| Sequential processing steps | Chain | Clear contracts between steps |
| Conditional branching | DAG | Handles complexity efficiently |
| Requires exploration/iteration | Agent loop | Self-correction capability |
| Multiple independent subtasks | Parallel fan-out | Latency optimization |

## Task-Model Fit Scorecard

Rate each dimension 1-5:

| Dimension | Score | Notes |
|-----------|-------|-------|
| Language understanding required | _/5 | Higher = better LLM fit |
| Output determinism required | _/5 | Higher = worse LLM fit |
| Reasoning depth required | _/5 | Higher = more expensive |
| Domain specificity | _/5 | Higher = needs RAG/fine-tuning |
| Error tolerance | _/5 | Higher = needs more evaluation |

**Interpretation**: Sum > 15 = good LLM fit. Sum < 10 = consider traditional approaches.

## Cost Estimation Formula

```
Daily cost = (avg_input_tokens × input_price + avg_output_tokens × output_price)
             × daily_volume × (1 + retry_rate) × pipeline_multiplier

Pipeline multipliers:
  Single-pass: 1.0
  Chain (3 steps): 2.5-3.5
  DAG (5 nodes): 3.0-5.0
  Agent loop (avg 8 turns): 6.0-12.0
```
