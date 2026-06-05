---
name: evaluation
description: This skill should be used for building deterministic evaluation frameworks for agent systems — assertion-based checks, regression testing, pass/fail criteria, metric design, and structured evaluation pipelines. Route LLM-as-judge techniques, rubric generation, and evaluator bias mitigation to advanced-evaluation. Route agent harness design to harness-engineering.
---

# Evaluation Frameworks for Agent Systems

Build evaluation systems that catch regressions before deployment and measure agent performance objectively. Agent evaluation differs from traditional software testing because outputs are non-deterministic — the same input can produce different valid outputs. The solution is layered evaluation: deterministic checks for structure and constraints, statistical checks for behavior, and LLM-based checks for subjective quality.

## When to Activate

Activate this skill when:
- Designing evaluation pipelines for agent systems
- Building regression tests for agent behavior
- Defining pass/fail criteria for agent outputs
- Choosing between evaluation approaches (deterministic vs. statistical vs. LLM-based)
- Measuring agent performance across versions or configurations

Do not activate this skill for adjacent work owned by other skills:
- LLM-as-judge scoring, pairwise comparison, and rubric generation: `advanced-evaluation`.
- Designing agent operating loops with evaluation gates: `harness-engineering`.
- Choosing project pipeline architecture: `project-development`.

## Core Concepts

Stack evaluation in three layers, each catching different failure classes:

1. **Deterministic checks** (fastest, most reliable) — Format validation, schema compliance, constraint satisfaction, required field presence, output length bounds. These are binary pass/fail with zero ambiguity.

2. **Statistical checks** (medium speed, medium reliability) — Aggregate metrics over multiple runs: success rate, average quality score, latency distribution, token usage patterns. Require sample sizes large enough for statistical significance.

3. **LLM-based checks** (slowest, most nuanced) — Semantic quality assessment, coherence evaluation, instruction following, factual accuracy. See `advanced-evaluation` for implementation details.

Run deterministic checks on every output. Run statistical checks on representative samples. Run LLM-based checks on a subset or during periodic quality audits.

## Detailed Topics

### Deterministic Evaluation

Build assertion-based checks that run on every agent output:

```python
class DeterministicEvaluator:
    def evaluate(self, output: dict, criteria: dict) -> dict:
        results = {}
        if "format" in criteria:
            results["format"] = self.check_format(output, criteria["format"])
        if "required_fields" in criteria:
            results["required_fields"] = self.check_fields(output, criteria["required_fields"])
        if "constraints" in criteria:
            results["constraints"] = self.check_constraints(output, criteria["constraints"])
        if "length_bounds" in criteria:
            results["length"] = self.check_length(output, criteria["length_bounds"])
        results["pass"] = all(r.get("pass", False) for r in results.values())
        return results

    def check_format(self, output, expected_format):
        """Validate output matches expected format (JSON, markdown, etc.)."""
        try:
            if expected_format == "json":
                json.loads(output["content"])
                return {"pass": True}
            elif expected_format == "markdown":
                return {"pass": output["content"].startswith("#")}
        except Exception as e:
            return {"pass": False, "error": str(e)}
```

### Regression Testing

Maintain a test suite of known-good input-output pairs:

```python
class RegressionSuite:
    def __init__(self, fixtures_path: str):
        self.fixtures = self.load_fixtures(fixtures_path)

    def run(self, agent_fn) -> dict:
        results = {"passed": 0, "failed": 0, "errors": []}
        for fixture in self.fixtures:
            output = agent_fn(fixture["input"])
            checks = self.evaluate(output, fixture["expected"])
            if checks["pass"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "fixture": fixture["id"],
                    "expected": fixture["expected"],
                    "actual": output,
                    "checks": checks
                })
        return results
```

### Metric Design

Design metrics that align with actual quality dimensions:

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| Task completion rate | Binary success/failure | All tasks |
| Constraint compliance | % of constraints satisfied | Constrained outputs |
| Output consistency | Agreement across runs | Non-deterministic tasks |
| Tool selection accuracy | Correct tool for task | Tool-using agents |
| Token efficiency | Useful tokens / total tokens | Cost optimization |
| Latency to completion | Time from input to output | Latency-sensitive tasks |

### Evaluation Pipeline Architecture

```
Input Cases -> Agent Under Test -> Raw Outputs
                                       |
                                       v
                              Deterministic Checks ──> Hard Failures (block)
                                       |
                                       v
                              Statistical Checks ──> Quality Alerts (warn)
                                       |
                                       v
                              LLM-Based Checks ──> Quality Report (review)
                                       |
                                       v
                              Aggregate Report -> Pass/Fail Decision
```

## Gotchas

- **Testing non-determinism as determinism**: Agent outputs vary between runs. Don't assert exact string matches — assert structural properties, constraint compliance, and semantic equivalence.
- **Evaluation set overfitting**: Optimizing for a fixed evaluation set may not improve real-world performance. Regularly refresh evaluation cases from production data.
- **Missing negative tests**: Testing that agents produce correct outputs is necessary but insufficient. Also test that agents don't produce harmful, incorrect, or constraint-violating outputs.
- **Metric gaming**: Agents (and humans optimizing agents) may game metrics without improving real quality. Use multiple complementary metrics and rotate evaluation sets.

## Integration

- `advanced-evaluation` extends this skill with LLM-as-judge techniques.
- `harness-engineering` uses evaluation gates within autonomous agent loops.
- `project-development` covers evaluation as part of the project lifecycle.
- `context-fundamentals` explains the attention mechanics that evaluation must account for.
