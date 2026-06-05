# How Skills Built This

This project demonstrates concrete applications of two skills:

## 1. `evaluation`
- **Deterministic scoring metrics**: Direct evaluation checks specific constraints (like character length and factual overlap) and maps them to a numeric score.

## 2. `advanced-evaluation`
- **Pairwise comparison**: A generic pairwise interface comparison is implemented.
- **Bias Mitigation**: The evaluator specifically runs the comparison in both orders (A/B and B/A) to cancel out position bias, which is a known vulnerability in LLM judges.
