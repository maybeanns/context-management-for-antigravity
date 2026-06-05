# How Skills Built This

## 1. `multi-agent-patterns`
- **Hierarchical structure**: A coordinator oversees worker agents. Worker output is passed via structured filesystem logs to minimize context telephone-game dilution.

## 2. `filesystem-context`
- **Output offloading**: Raw paper text is saved directly to disk. The agents only reference the file path inside the context.

## 3. `context-compression`
- **Session summary**: The final run outcome is summarized using a standardized research brief template.
