# How Skills Built This

This project demonstrates concrete applications of three skills:

## 1. `harness-engineering`
- **Locked Metrics**: Implemented in `harness.py` via `HarnessSession` tracking `token_budget` and `max_turns`.
- **Durable Logs**: Every action and observation is appended to `session.log` in JSONL format, preserving the full execution trajectory.
- **Novelty Gates**: Track the edit history and rollback file changes if the agent enters an infinite retry loop or generates the same error twice.

## 2. `tool-design`
- **Consolidation**: Instead of separate tools for `read_file`, `write_file`, and `patch_file`, the harness exposes a minimal, consolidated `file_editor` tool with explicit schema.
- **Namespacing & Clean Descriptions**: Tool definitions are structured for unambiguous selection.

## 3. `context-optimization`
- **Prefix Caching**: The system instructions and core tool definitions are kept static at the start of the prompt.
- **Observation Masking**: Old tool outputs (e.g. from previous compiler runs) are masked with `[Output of previous compilation omitted]` to save context window tokens.
