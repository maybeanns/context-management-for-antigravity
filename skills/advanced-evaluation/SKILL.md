---
name: advanced-evaluation
description: This skill should be used for LLM-as-a-Judge evaluation techniques — direct scoring, pairwise comparison, rubric generation, reference-based grading, bias mitigation, calibration, and evaluator reliability measurement. Route deterministic evaluation checks and pipeline design to evaluation. Route agent harness design to harness-engineering.
---

# Advanced Evaluation: LLM-as-a-Judge Techniques

Master the use of language models as evaluators for subjective quality dimensions that deterministic checks cannot capture. LLM-as-judge evaluation complements assertion-based testing by assessing coherence, helpfulness, safety, instruction-following, and other qualities that require semantic understanding. The core challenge is that evaluators are themselves non-deterministic — they exhibit systematic biases that must be detected and mitigated.

## When to Activate

Activate this skill when:
- Implementing LLM-based scoring for agent outputs
- Designing pairwise comparison evaluations
- Building rubrics for subjective quality assessment
- Mitigating evaluator biases (position, verbosity, self-preference)
- Calibrating evaluator models against human judgments
- Measuring inter-evaluator reliability

Do not activate this skill for adjacent work owned by other skills:
- Deterministic checks, regression testing, or metric design: `evaluation`.
- Designing autonomous agent loops with evaluation gates: `harness-engineering`.
- Choosing evaluation strategy at the project level: `project-development`.

## Core Concepts

LLM-as-judge evaluation uses a language model to score or compare outputs against quality criteria. Three evaluation modes serve different purposes:

1. **Direct scoring** — A single evaluator rates an output on a scale (1-5, 1-10). Simple but susceptible to calibration drift.
2. **Pairwise comparison** — An evaluator chooses between two outputs. More reliable than direct scoring because relative judgments are easier than absolute ones.
3. **Reference-based grading** — An evaluator compares output against a gold-standard reference. Most reliable but requires reference answers.

All three modes are subject to systematic biases: position bias (preferring the first or last option), verbosity bias (preferring longer responses), self-preference bias (preferring outputs from the same model family), and anchoring bias (being influenced by the scoring scale presentation).

## Detailed Topics

### Direct Scoring

```python
class DirectScorer:
    def score(self, output: str, criteria: str, scale: tuple = (1, 5)) -> dict:
        prompt = f"""Rate the following output on a scale of {scale[0]} to {scale[1]}.

Criteria: {criteria}

Output to evaluate:
{output}

Provide your rating as a JSON object: {{"score": N, "rationale": "..."}}"""
        response = self.evaluator_model(prompt)
        return json.loads(response)
```

**Calibration**: Run the scorer on known-quality outputs to establish baseline scores. Monitor for drift — if average scores change over time without quality changes, the evaluator needs recalibration.

### Pairwise Comparison

```python
class PairwiseComparator:
    def compare(self, output_a: str, output_b: str, criteria: str) -> dict:
        # Randomize order to mitigate position bias
        if random.random() > 0.5:
            first, second, order = output_a, output_b, "original"
        else:
            first, second, order = output_b, output_a, "swapped"

        prompt = f"""Compare the following two outputs.

Criteria: {criteria}

Output 1:
{first}

Output 2:
{second}

Which output is better? Respond: {{"winner": 1 or 2, "rationale": "..."}}"""
        result = json.loads(self.evaluator_model(prompt))
        # Correct for order swapping
        if order == "swapped":
            result["winner"] = 3 - result["winner"]
        return result
```

### Bias Mitigation

**Position Bias**
Run every comparison twice with swapped order. Only count results where both orderings agree. Disagreements indicate position bias is dominating the judgment.

**Verbosity Bias**
Normalize output lengths before comparison, or explicitly instruct evaluators to judge quality independent of length. Monitor correlation between output length and scores.

**Self-Preference Bias**
Use evaluator models from a different family than the generation model. If evaluating GPT-4 outputs, use Claude as the evaluator, and vice versa.

**Anchoring Bias**
Vary scoring scales across evaluation runs to detect scale-dependent behavior. If changing from 1-5 to 1-10 produces non-linearly different distributions, anchoring is affecting results.

### Rubric Generation

Generate evaluation rubrics that make quality criteria explicit and measurable:

```python
def generate_rubric(task_description: str, quality_dimensions: list) -> dict:
    rubric = {}
    for dimension in quality_dimensions:
        rubric[dimension] = {
            "5_excellent": f"Description of excellent performance on {dimension}",
            "4_good": f"Description of good performance on {dimension}",
            "3_adequate": f"Description of adequate performance on {dimension}",
            "2_poor": f"Description of poor performance on {dimension}",
            "1_failing": f"Description of failing performance on {dimension}",
        }
    return rubric
```

### Evaluator Reliability

Measure evaluator consistency using:

- **Intra-rater reliability**: Same evaluator, same inputs, different runs. Should produce consistent scores.
- **Inter-rater reliability**: Different evaluator models, same inputs. Agreement indicates robust quality signal.
- **Human correlation**: Evaluator scores vs. human expert scores. The gold standard for validation.

## Gotchas

- **Evaluator as oracle fallacy**: LLM evaluators are not ground truth. They exhibit systematic biases and can be confidently wrong. Always validate against human judgments.
- **Rubric vagueness**: Vague rubric criteria ("good quality") produce inconsistent scores. Make every rubric level concrete and distinguishable.
- **Scale collapse**: Evaluators often cluster scores in a narrow range (e.g., 3-4 on a 1-5 scale). Use pairwise comparison when differentiation matters.
- **Evaluation cost**: LLM-based evaluation can be expensive at scale. Reserve for periodic audits, not every output.

## Integration

- `evaluation` provides the deterministic foundation that this skill extends.
- `harness-engineering` uses evaluation gates within autonomous agent loops.
- `project-development` covers evaluation planning at the project level.
