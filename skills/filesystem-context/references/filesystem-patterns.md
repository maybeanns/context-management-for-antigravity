# Filesystem Context Patterns Reference

## Pattern Catalog

### 1. Scratch Pad (Working Memory Extension)
**File**: `scratch.md` or `.scratch/current.md`
**Purpose**: Intermediate results, working notes, tool output summaries
**Lifecycle**: Created per-task, discarded on completion
**Access**: Read/write by active agent only

### 2. Plan File (Task Orchestration)
**File**: `plan.md` or `.plans/active.md`
**Purpose**: Task decomposition, progress tracking, decision log
**Lifecycle**: Created at task start, updated throughout, archived on completion
**Access**: Read/write by all agents in the session

### 3. Knowledge Directory (Structured Reference)
**Structure**: `knowledge/<category>/<topic>.md`
**Purpose**: Organized reference material discoverable via `ls` and `grep`
**Lifecycle**: Persistent across sessions
**Access**: Read by agents, write by designated knowledge agents

### 4. Tool Output Archive (Offloaded Results)
**Structure**: `tool_outputs/<tool_name>_<timestamp>.md`
**Purpose**: Full tool outputs too large for context
**Lifecycle**: Created per tool call, cleaned up periodically
**Access**: Read by agents, write by harness

### 5. Communication Channel (Agent-to-Agent)
**Structure**: `shared/<agent_name>_output.md`
**Purpose**: Results from sub-agents for coordinator consumption
**Lifecycle**: Created by worker, consumed by coordinator
**Access**: Write by source agent, read by target agent

## Discovery Primitives

| Operation | Command | Use Case |
|-----------|---------|----------|
| List structure | `ls -la directory/` | Discover available content |
| Find by name | `glob "**/*.md"` | Locate files by pattern |
| Search content | `grep -r "keyword" directory/` | Find relevant content |
| Read targeted | `read_file path/to/file.md` | Load specific content |
| Check existence | `test -f path/to/file` | Verify before reading |
