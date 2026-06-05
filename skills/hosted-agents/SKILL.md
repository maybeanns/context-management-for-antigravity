---
name: hosted-agents
description: This skill should be used when building background coding agents that run in remote sandboxed environments — pre-built images, warm sandbox pools, filesystem snapshots, multiplayer support, multi-client interfaces, and self-spawning patterns. Route multi-agent coordination patterns to multi-agent-patterns, individual tool design to tool-design, and filesystem offloading patterns to filesystem-context.
---

# Hosted Agent Infrastructure

Background coding agents run in remote sandboxed environments rather than on local machines. This separation enables persistent sessions, parallel execution, shared environments, and security isolation. The infrastructure challenge is minimizing latency (time to first useful action) while maximizing safety (preventing uncontrolled resource usage or data exfiltration).

## When to Activate

Activate this skill when:
- Designing infrastructure for background coding agents
- Building sandboxed execution environments for agent tasks
- Implementing session persistence and snapshot mechanisms
- Designing warm pool strategies for fast agent startup
- Building multiplayer agent environments (human + multiple agents)
- Planning self-spawning patterns for parallel task execution

Do not activate this skill for adjacent work owned by other skills:
- Designing multi-agent coordination protocols: `multi-agent-patterns`.
- Writing tool descriptions and schemas for agent tools: `tool-design`.
- Implementing filesystem-based context patterns within sandboxes: `filesystem-context`.
- Compressing session state for handoffs: `context-compression`.

## Core Concepts

Optimize for time-to-first-action. Pre-built environment images with dependencies pre-installed eliminate cold-start delays. Warm sandbox pools provide instant session starts by maintaining ready-to-use environments. Predictive warming (triggered when users start typing) further reduces perceived latency.

Design for persistence through filesystem snapshots. Agent sessions produce valuable state — modified files, test results, build artifacts — that must survive session boundaries. Snapshot mechanisms capture this state; restore mechanisms rebuild it in new sessions.

Enable multiplayer support for collaborative agent sessions. Multiple agents and humans may need to work in the same environment simultaneously, requiring file locking, change notification, and conflict resolution.

## Detailed Topics

### Pre-Built Environment Images

Build environment images on a regular cadence (daily or per-commit) that include:
- Language runtimes and package managers
- Project dependencies pre-installed
- Common tools (linters, formatters, test runners)
- Cached build artifacts

```python
class EnvironmentImage:
    def build(self, project_config: dict) -> str:
        """Build a pre-configured environment image."""
        return {
            "base_image": project_config["runtime"],
            "dependencies": self.resolve_dependencies(project_config),
            "tools": ["git", "grep", "find", "jq"],
            "cache": self.warm_caches(project_config),
            "built_at": datetime.utcnow().isoformat()
        }
```

### Warm Sandbox Pools

Maintain a pool of pre-warmed sandboxes at varying readiness levels:

| Level | Description | Startup Time |
|-------|-------------|-------------|
| Cold | Base OS image only | 30-60s |
| Warm | Runtime + deps installed | 5-10s |
| Hot | Project cloned + built | <2s |

Scale pool size based on usage patterns. Implement predictive warming: when a user opens a project, start warming a sandbox before they request an agent session.

### Session Persistence

Implement filesystem snapshots for session state:

1. **On pause**: Capture modified files, git state, environment variables
2. **On resume**: Restore from snapshot, validate state consistency
3. **On handoff**: Transfer snapshot to new agent with context summary

Allow file reads before git sync completes (block only writes) to minimize perceived latency during session restore.

### Self-Spawning Patterns

Enable agents to spawn additional agents for parallel subtasks:

```python
def spawn_worker(task: str, tools: list, context: dict) -> str:
    """Spawn a new agent instance for parallel work."""
    worker = create_sandbox(
        image=context["project_image"],
        tools=tools,
        system_prompt=build_worker_prompt(task, context),
        timeout=context.get("timeout", 300)
    )
    return worker.session_id
```

Guard self-spawning with resource limits: maximum concurrent agents, total compute budget, and time-to-live per spawned agent.

## Gotchas

- **Snapshot bloat**: Frequent snapshots of large repositories consume significant storage. Implement incremental snapshots (only changed files) and TTL-based cleanup.
- **Environment drift**: Pre-built images become stale as dependencies update. Implement staleness detection and force rebuilds when dependencies change.
- **Resource leaks**: Spawned sandboxes that aren't properly cleaned up consume resources indefinitely. Implement hard TTLs and periodic garbage collection.
- **Network isolation gaps**: Sandboxed agents may need network access for package installation but shouldn't have unrestricted internet access. Implement allowlist-based network policies.

## Integration

- `multi-agent-patterns` provides coordination protocols for multi-agent sessions.
- `tool-design` covers designing tools that work within sandbox constraints.
- `filesystem-context` provides patterns for file-based context within sandboxes.
- `harness-engineering` provides the operating loop that manages sandbox lifecycle.
