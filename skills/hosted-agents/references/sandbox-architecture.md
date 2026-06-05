# Sandbox Architecture Reference

## Sandbox Lifecycle States

```
COLD → WARMING → WARM → HOT → ACTIVE → PAUSED → SNAPSHOT → TERMINATED
```

| State | Description | Transition Trigger |
|-------|-------------|-------------------|
| COLD | Base image only | Pool request |
| WARMING | Installing deps | Pool manager |
| WARM | Deps ready | Project assignment |
| HOT | Project cloned + built | User request |
| ACTIVE | Agent session running | Session start |
| PAUSED | Session suspended | Idle timeout |
| SNAPSHOT | State captured | Pause or handoff |
| TERMINATED | Resources freed | Session end or TTL |

## Resource Limits Template

```yaml
sandbox_limits:
  cpu: 2 cores
  memory: 4GB
  disk: 10GB
  network: allowlist_only
  max_processes: 50
  max_file_size: 100MB
  session_ttl: 3600  # seconds
  idle_timeout: 300   # seconds
```

## Security Considerations

- **Network isolation**: Default deny, allowlist for package registries
- **Filesystem isolation**: Agent cannot access host filesystem
- **Process isolation**: Agent processes sandboxed via containers or VMs
- **Resource caps**: Hard limits on CPU, memory, disk to prevent abuse
- **Credential management**: Secrets injected via environment, never persisted to disk
