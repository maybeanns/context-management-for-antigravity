# Code Generation Harness Example

This example demonstrates how to apply the `harness-engineering`, `tool-design`, and `context-optimization` skills to build a safe, reliable, autonomous code-generation agent loop.

## Overview

The harness wraps an agent loop with deterministic safety boundaries:
1. **Locked Metrics**: Track total tokens used, total execution time, and cumulative cost. Fails the run if thresholds are exceeded.
2. **Durable Logs**: Writes every turn (query, response, tool call, tool output) to a JSONL log file.
3. **Novelty Gates**: Track the state of code being edited. If the agent generates the same error twice, or edit attempts stall (no change in edit diff), the harness triggers a novelty gate and rolls back the file or intervenes.
4. **Human Approval Boundaries**: Requires explicit approval for file-system writes.

## Installation

```bash
pip install -e ".[dev]"
```

## Running Tests

To run the unit tests demonstrating the harness's boundary gates:

```bash
pytest
```
