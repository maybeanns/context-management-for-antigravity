# Digital Brain Skill Example

A demonstration of a personal knowledge OS applying context-fundamentals and memory-systems principles.

## Overview
This project represents a conceptual "Digital Brain" or personal knowledge base that runs on top of the filesystem. It dynamically loads note contexts and constructs memory graphs.

## Core Design
- **Memory Nodes**: Formed by Markdown files with structured YAML frontmatter.
- **Dynamic Retrieval**: Instead of loading the entire knowledge base, the agent uses semantic tag queries to selectively retrieve relevant nodes.
