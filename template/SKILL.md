---
name: skill-template
description: Template for creating new Agent Skills for context engineering. Use this template when adding new skills to the collection.
---

# Skill Name

Provide a clear, concise description of what this skill covers and when to use it. This description appears in skill discovery and should help agents (and humans) determine when this skill is relevant.

**Important**: Keep the total SKILL.md body under 500 lines for optimal performance. Move detailed reference material to separate files in the `references/` directory.

Every skill body must make its ownership boundary explicit. The description and `When to Activate` section should say what the skill owns and which adjacent skills own nearby work. This prevents broad skills from stealing activation from narrower skills.

## When to Activate

Describe specific situations, tasks, or contexts where this skill should be activated. Include both direct triggers (specific keywords or task types) and indirect signals (broader patterns that indicate skill relevance).

Write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems.

- Good: "Processes Excel files and generates reports"
- Avoid: "I can help you process Excel files"

Include a short "Do not activate" block for adjacent skills. Example:

Do not activate this skill for adjacent work owned by other skills:

- Do not activate for project-level pipeline shape: `project-development`.
- Do not activate for individual tool schema design: `tool-design`.

## Core Concepts

Explain the fundamental concepts covered by this skill. These are the mental models, principles, or frameworks that the skill teaches.

Default assumption: the agent is already very smart. Only add context the agent does not already have. Challenge each piece of information:
- "Does the agent really need this explanation?"
- "Can I assume the agent knows this?"
- "Does this paragraph justify its token cost?"

Prefer behavior-changing mechanisms over general background. If a concept should be reusable across the corpus, add or update a record in `researcher/mechanisms/registry.jsonl`.

## Detailed Topics

### Topic 1

Provide detailed explanation of the first major topic. Include specific techniques, patterns, or approaches. Use examples to illustrate concepts.

### Topic 2

Provide detailed explanation of the second major topic.

## Gotchas

List experience-derived failure modes and counterintuitive behaviors. Gotchas are the highest-signal content in any skill — they encode hard-won knowledge that prevents agents from repeating known mistakes.

- **Gotcha name**: Description of the failure mode and how to avoid it.

## Integration

Describe how this skill connects to other skills in the collection. Use explicit cross-references:

- `context-fundamentals` provides the foundational mental models this skill builds on.
- `context-optimization` provides the operational tactics this skill's concepts inform.

## References

List any external references, papers, or documentation that informed this skill. Use the claim system for volatile facts:

- `claim-<skill-name>-<topic>`: Description of the claim and its source.

Move detailed reference material to the `references/` directory:

- `references/topic-name.md` — Deep-dive on specific topics that exceed the 500-line budget.
