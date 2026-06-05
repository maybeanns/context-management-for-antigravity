---
name: project-development
description: This skill should be used for LLM project lifecycle decisions — task-model fit analysis, pipeline architecture design, structured output schemas, batch processing strategies, cost estimation, and deployment planning. Route individual tool design to tool-design, multi-agent topology decisions to multi-agent-patterns, and evaluation framework design to evaluation.
---

# LLM Project Development

Design and build LLM-powered projects from ideation through deployment. This skill covers the meta-level decisions that shape a project before any code is written: whether LLMs are appropriate for the task, how to structure the pipeline, what output formats to use, how to handle batch processing, and how to plan for cost and scale.

## When to Activate

Activate this skill when:
- Starting a new LLM-powered project from scratch
- Analyzing whether a task is a good fit for language models
- Designing pipeline architecture (single-pass, chain, DAG, agent loop)
- Choosing structured output schemas and validation strategies
- Planning batch processing for throughput optimization
- Estimating costs and planning resource allocation

Do not activate this skill for adjacent work owned by other skills:
- Designing individual tool schemas and descriptions: `tool-design`.
- Choosing multi-agent topology (supervisor vs. swarm): `multi-agent-patterns`.
- Building evaluation pipelines and metrics: `evaluation`.
- Designing agent operating loops: `harness-engineering`.

## Core Concepts

Start every project with task-model fit analysis. Not all tasks benefit from LLMs — some are better served by traditional software, rules engines, or simpler ML models. LLMs excel at tasks requiring language understanding, generation, reasoning across unstructured data, and flexible decision-making. They struggle with tasks requiring exact arithmetic, deterministic logic, real-time performance, or guaranteed correctness.

Design pipelines around the complexity of the task, not the sophistication of the technology:

| Pipeline Type | When to Use | Complexity |
|--------------|-------------|-----------|
| Single-pass | Task has one clear input → output | Lowest |
| Chain | Task decomposes into sequential steps | Low |
| DAG | Steps have conditional branches or parallel paths | Medium |
| Agent loop | Task requires exploration, tool use, or self-correction | Highest |

Choose the simplest pipeline that solves the problem. Over-engineering adds cost, latency, and debugging difficulty without proportional quality gains.

## Detailed Topics

### Task-Model Fit Analysis

Evaluate fitness across five dimensions:

1. **Input structure** — How structured is the input? Unstructured text is ideal for LLMs. Highly structured data (tables, forms) may be better served by traditional processing.
2. **Output determinism** — How much variation is acceptable? Tasks requiring exact answers need heavy validation. Tasks with creative latitude are more forgiving.
3. **Reasoning depth** — How many steps of reasoning are required? Single-step tasks are reliable. Multi-step chains accumulate error.
4. **Domain specificity** — How specialized is the knowledge? General knowledge works well. Niche domains may need fine-tuning or RAG.
5. **Error tolerance** — What is the cost of a wrong answer? High-stakes tasks need robust evaluation and human oversight.

### Pipeline Architecture

**Single-Pass Pipeline**
```
Input -> LLM -> Validate -> Output
```
Use for: classification, summarization, extraction, translation. Maximum simplicity, lowest latency.

**Chain Pipeline**
```
Input -> LLM (Extract) -> LLM (Analyze) -> LLM (Format) -> Output
```
Use for: multi-step processing where each step builds on the previous. Each step has a clear contract.

**DAG Pipeline**
```
Input -> [LLM (Path A), LLM (Path B)] -> Merge -> LLM (Synthesize) -> Output
```
Use for: tasks with conditional logic or parallel subtasks. More complex to orchestrate but enables specialization.

**Agent Loop Pipeline**
```
Input -> Agent[tools, memory, evaluation] -> (loop until done) -> Output
```
Use for: open-ended tasks requiring exploration, tool use, and self-correction. Highest capability but hardest to control.

### Structured Output Design

Design output schemas that enable reliable downstream parsing:

```python
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    """Structured output for document analysis."""
    summary: str = Field(description="2-3 sentence summary of key findings")
    sentiment: str = Field(description="positive, negative, or neutral")
    key_entities: list[str] = Field(description="Named entities mentioned")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    reasoning: str = Field(description="Step-by-step reasoning for the analysis")
```

Use schema validation on every LLM output. Retry with explicit error messages when validation fails. Design schemas that are specific enough to be useful but flexible enough to accommodate valid variation.

### Batch Processing

Optimize throughput and cost through batching:

- **Request batching** — Combine multiple inputs into a single prompt when tasks are independent and context allows.
- **Async processing** — Process batches asynchronously to maximize throughput.
- **Priority queuing** — Route urgent requests to real-time processing, bulk requests to batch queues.
- **Cost optimization** — Batch processing APIs often offer significant discounts (50%+) compared to real-time pricing.

### Cost Estimation

```python
def estimate_cost(task_config: dict) -> dict:
    input_tokens = task_config["avg_input_tokens"] * task_config["volume"]
    output_tokens = task_config["avg_output_tokens"] * task_config["volume"]
    retries = task_config["volume"] * task_config["retry_rate"]
    total_input = input_tokens + (retries * task_config["avg_input_tokens"])
    total_output = output_tokens + (retries * task_config["avg_output_tokens"])
    return {
        "input_cost": total_input * task_config["input_price_per_token"],
        "output_cost": total_output * task_config["output_price_per_token"],
        "total_daily": (total_input * task_config["input_price_per_token"] +
                       total_output * task_config["output_price_per_token"]),
    }
```

## Gotchas

- **Over-engineering the first version**: Start with the simplest pipeline that works. Add complexity only when evaluation data shows it's needed.
- **Ignoring cost at design time**: A pipeline that costs $0.10 per request at $1000/day volume needs different architecture than one at $10/day.
- **Schema rigidity**: Over-specified schemas reject valid outputs. Under-specified schemas produce unparseable outputs. Iterate schema design alongside prompt design.
- **Batch-processing ordering effects**: Some LLMs are sensitive to the order of items in a batch. Randomize order and verify consistency.

## Integration

- `tool-design` covers designing the tools used within pipelines.
- `multi-agent-patterns` covers when to escalate from pipelines to multi-agent systems.
- `evaluation` covers building evaluation for pipeline outputs.
- `context-optimization` covers reducing per-request token costs.
