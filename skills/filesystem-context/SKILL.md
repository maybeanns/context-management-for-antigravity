---
name: filesystem-context
description: This skill should be used for filesystem-based context management — scratch pads, plan persistence, tool output offloading, sub-agent communication via shared files, dynamic skill loading, and just-in-time context discovery using standard file operations. Route memory architecture decisions to memory-systems, compression strategies to context-compression, and hosted runtime infrastructure to hosted-agents.
---

# Filesystem-Based Context Management

The filesystem provides a single interface for storing, retrieving, and updating effectively unlimited context outside the model's context window. Unlike in-context memory, filesystem storage has zero token cost until content is actively read, supports random access, persists across sessions, and is accessible by multiple agents simultaneously.

## When to Activate

Activate this skill when:
- Offloading large tool outputs to avoid context bloat
- Persisting plans and progress across long-horizon tasks
- Enabling sub-agent communication via shared files
- Implementing just-in-time context loading from structured files
- Designing scratch pad patterns for working memory extension
- Building discovery mechanisms using standard file operations

Do not activate this skill for adjacent work owned by other skills:
- Designing memory architecture (vector RAG, knowledge graphs): `memory-systems`.
- Compressing conversation history into summaries: `context-compression`.
- Building hosted sandbox environments: `hosted-agents`.
- Diagnosing context degradation in loaded content: `context-degradation`.

## Core Concepts

Use the filesystem as an attention-budget multiplier. Instead of loading entire documents into context, maintain lightweight references (file paths, content summaries) and load data just-in-time when the current task requires it. This mirrors human cognition: maintain an index, retrieve on demand.

Agents navigate filesystems effectively using four primitives: `ls` for structure discovery, `glob` for pattern matching, `grep` for content search, and `read_file` for targeted loading. These often outperform semantic search for structural queries because they provide deterministic, exact-match results.

## Detailed Topics

### Scratch Pad Pattern

Maintain a running scratch file for intermediate results, working notes, and tool output summaries:

```markdown
# scratch.md — Working State

## Current Task
Implementing user authentication flow

## Key Findings
- Database schema uses `users` table with `email` as unique key
- OAuth provider configured in `config/auth.yml`
- Rate limiting set to 100 requests/minute per IP

## Pending Questions
- [ ] Confirm session duration (currently 24h)
- [ ] Check if MFA is required for admin users
```

Write to scratch after processing tool outputs. Read from scratch when resuming work. This pattern reduces reliance on message history for state tracking.

### Plan Persistence

Persist task decomposition and progress in structured plan files:

```markdown
# plan.md — Task Plan

## Objective
Refactor authentication module to support OAuth2

## Steps
- [x] Audit current auth implementation
- [x] Design OAuth2 flow diagram
- [/] Implement token exchange endpoint
- [ ] Add refresh token rotation
- [ ] Update integration tests
- [ ] Update API documentation

## Decisions
- Using PKCE flow for public clients (Turn 5)
- Storing refresh tokens in encrypted database column (Turn 8)
```

Plans survive context resets, session restarts, and agent handoffs. They provide continuity that message history cannot guarantee.

### Tool Output Offloading

Redirect verbose tool outputs to files instead of loading them into context:

```python
def handle_large_output(tool_name: str, output: str, threshold: int = 2000):
    """Offload large outputs to filesystem, return summary in context."""
    if len(output) > threshold:
        filepath = f"tool_outputs/{tool_name}_{timestamp()}.md"
        write_file(filepath, output)
        return f"Full output saved to {filepath}. Summary: {summarize(output)}"
    return output
```

This preserves the information without consuming context tokens. Agents can read specific sections of the file when needed.

### Sub-Agent Communication

Share context between agents through files rather than passing through coordinator context:

```
shared/
├── task_assignment.md     # Coordinator writes, workers read
├── worker_a_results.md    # Worker A writes, coordinator reads
├── worker_b_results.md    # Worker B writes, coordinator reads
└── shared_state.json      # All agents read/write with locking
```

File-based communication avoids the telephone game problem (coordinator paraphrasing worker results) and provides an audit trail.

### Dynamic Context Discovery

Build structured knowledge directories that agents can explore:

```
project_knowledge/
├── architecture/
│   ├── overview.md
│   ├── data_model.md
│   └── api_contracts.md
├── decisions/
│   ├── 001_auth_provider.md
│   └── 002_database_choice.md
└── runbooks/
    ├── deployment.md
    └── incident_response.md
```

Agents use `ls` to discover available knowledge, `grep` to find relevant content, and `read_file` to load specific sections. This is more efficient than pre-loading all documentation into context.

## Gotchas

- **Stale file references**: Agents may reference files that have been moved, renamed, or deleted. Validate file existence before citing content from files.
- **Write conflicts**: Multiple agents writing to the same file simultaneously can cause data loss. Implement simple locking or use append-only patterns for shared files.
- **Path assumptions**: Agents may assume file paths based on common conventions that don't match the actual project structure. Always discover paths rather than guessing.
- **Over-offloading**: Offloading everything to files forces excessive read operations. Keep actively-needed context in the window; offload only reference material and verbose outputs.

## Integration

- `context-fundamentals` explains the attention budget that filesystem offloading preserves.
- `memory-systems` provides higher-level memory architecture that filesystem patterns implement.
- `context-compression` provides alternatives when filesystem access is limited.
- `multi-agent-patterns` uses filesystem communication for agent coordination.
- `hosted-agents` provides the runtime environment where filesystem patterns operate.
