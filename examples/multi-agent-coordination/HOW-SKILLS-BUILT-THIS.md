# How Skills Built This

## 1. `multi-agent-patterns`
- **Topology choice**: Demonstrates both Supervisor and Peer-to-Peer modes based on task complexity.

## 2. `memory-systems`
- **Shared memory store**: Agents read and write to a common memory registry that maps variables and state objects, ensuring state consistency.

## 3. `latent-briefing`
- **KV cache sharing**: Sub-agents inherit prefix-cached state from the supervisor, bypassing long system prompts processing.
