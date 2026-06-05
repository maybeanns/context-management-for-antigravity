# LLM-as-a-Judge Evaluation Pipeline

This example demonstrates how to apply the `evaluation` and `advanced-evaluation` skills to build an automated, bias-aware evaluation pipeline.

## Overview

The judge system evaluates model outputs using:
1. **Direct Scoring**: Score outputs against explicit criteria on a 0-10 scale.
2. **Pairwise Comparison**: Compares two outputs directly.
3. **Position-Bias Mitigation**: Swaps candidate order (A vs B and B vs A) to ensure the evaluator doesn't consistently favor the first option.

## Installation

Ensure you have Node.js (version >= 18) installed, then:

```bash
npm install
```

## Running Tests

To run the Vitest suite validating the evaluator logic:

```bash
npm test
```
