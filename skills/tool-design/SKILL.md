---
name: tool-design
description: This skill should be used for the tool-interface layer of an agent system — writing tool descriptions agents can route on, designing tool schemas and response formats, naming conventions, actionable error recovery messages, MCP server design, tool-set consolidation, and deciding when to add or remove an individual tool. Route project-shape and pipeline architecture decisions to project-development; route deciding whether to introduce sub-agents to multi-agent-patterns.
---

# Tool Design for Agents

Design every tool as a contract between a deterministic system and a non-deterministic agent. Unlike human-facing APIs, agent-facing tools must make the contract unambiguous through the description alone: agents infer intent from descriptions and generate calls that must match expected formats. Every ambiguity becomes a potential failure mode that no amount of prompt engineering can fix.

The unit of work for this skill is a single tool or a tool catalog. Project-shape, pipeline architecture, task-model-fit, and cost-at-the-project-level decisions belong to `project-development`. Deciding whether to introduce sub-agents belongs to `multi-agent-patterns`.

## When to Activate

Activate this skill when the unit of work is a tool:
- Writing a new tool description, schema, or response format.
- Debugging cases where the agent picked the wrong tool or generated malformed calls.
- Consolidating an overlapping tool catalog.
- Designing actionable error messages so the agent can self-correct.
- Naming tools and parameters consistently across a catalog (MCP namespacing, verb-noun naming).
- Evaluating a third-party tool against the consolidation principle before adding it.

Do not activate this skill for adjacent work owned by other skills:
- Deciding whether the project should use LLMs at all, or what the pipeline stages should be: `project-development`.
- Deciding whether to split work across sub-agents or run a single agent with more tools: `multi-agent-patterns`.
- Reducing the token weight of tool outputs at the trajectory level: `context-optimization`.

## Core Concepts

Design tools around the consolidation principle: if a human engineer cannot definitively say which tool should be used in a given situation, an agent cannot be expected to do better. Reduce the tool set until each tool has one unambiguous purpose.

Treat every tool description as prompt engineering that shapes agent behavior. The description is not documentation for humans — it is injected into the agent's context and directly steers reasoning.

## Detailed Topics

### The Tool-Agent Interface

**Tools as Contracts**
Design each tool as a self-contained contract. Agents must infer the entire contract from a single description block. Include format examples, expected patterns, and explicit constraints.

**Tool Description as Prompt**
Write tool descriptions knowing they load directly into agent context. A vague description like "Search the database" forces the agent to guess. Instead, include usage context, parameter format examples, and sensible defaults.

**Namespacing and Organization**
Namespace tools under common prefixes as the collection grows: `db_query`, `db_insert`, `web_fetch`, `web_search`. Without namespacing, agents evaluate every tool in a flat list, degrading selection accuracy.

### The Consolidation Principle

**Single Comprehensive Tools**
Build single comprehensive tools instead of multiple narrow tools that overlap. Rather than `list_users`, `list_events`, `create_event`, implement `schedule_event` that handles the full workflow.

**When Not to Consolidate**
Keep tools separate when they have fundamentally different behaviors, serve different contexts, or must be callable independently. Over-consolidation creates tools with too many parameters and modes.

### Architectural Reduction

Push consolidation to its logical extreme: remove most specialized tools in favor of primitive, general-purpose capabilities.

**The File System Agent Pattern**
Provide direct file system access through a single command execution tool. The agent uses standard Unix utilities (`grep`, `cat`, `find`, `ls`) to explore and operate. This works because file systems are a proven abstraction that models understand deeply.

**When Reduction Outperforms Complexity**
Choose reduction when the data layer is well-documented and consistently structured, the model has sufficient reasoning capability, and specialized tools were constraining rather than enabling.

### Error Design

**Actionable Error Messages**
Return error messages that tell the agent what went wrong and what to try next:

```python
# Bad: opaque error
{"error": "Invalid parameter"}

# Good: actionable error
{"error": "Parameter 'date' must be ISO 8601 format (YYYY-MM-DD). Received: '12/25/2024'. Try: '2024-12-25'"}
```

**Error Recovery Patterns**
Design tools to support self-correction: include valid alternatives in error responses, suggest parameter fixes, and provide example correct calls.

### MCP Server Design

When building MCP (Model Context Protocol) servers:
- Group related tools under a single server with clear namespacing
- Implement resource endpoints for discovery (`list_resources`)
- Provide schema validation on input parameters
- Return structured responses that agents can parse reliably

## Gotchas

- **Description-schema mismatch**: When the tool description promises something the schema doesn't support, agents generate calls that match the description, not the schema. Keep them synchronized.
- **Tool schema token inflation**: JSON-serialized tool schemas inflate 2-3x compared to plain text. Monitor total tool token cost — 20 tools can consume 10-15K tokens.
- **Error swallowing**: Tools that return empty results on error (instead of error messages) leave agents unable to self-correct. Always return structured error information.
- **Overly flexible parameters**: Optional parameters with complex defaults create ambiguity. Prefer required parameters with clear types over optional parameters with implicit behavior.

## Integration

- `context-fundamentals` explains the attention mechanics that tool descriptions must respect.
- `context-optimization` covers reducing tool output token cost at the trajectory level.
- `multi-agent-patterns` covers when to split tools across agents vs. consolidate.
- `project-development` covers project-level decisions about tool architecture.
