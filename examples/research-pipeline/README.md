# Research Pipeline Example

A pipeline for research automation demonstrating multi-agent coordination and filesystem-based context storage.

## Overview
This system orchestrates multiple sub-agents to gather, clean, and summarize academic papers.

## Core Design
- **Orchestrator Agent**: Breaks down the topic and spawns Search and Summary agents.
- **Shared Filesystem Context**: Sub-agents write their intermediate papers/results to the shared directory, passing simple file links rather than passing giant raw texts.
- **Handoff Compression**: Prior to reporting to the user, the orchestrator compresses the entire search history into a structured brief.
