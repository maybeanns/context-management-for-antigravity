# Tool Contract Reference

## Tool Description Checklist
- [ ] What does the tool do? (action verb + object)
- [ ] When should it be used? (trigger conditions)
- [ ] What does it return? (output format + examples)
- [ ] What are the required parameters? (with types + constraints)
- [ ] What are sensible defaults for optional parameters?
- [ ] What errors can occur and how should the agent respond?

## Naming Convention Guide
- Use `verb_noun` format: `search_documents`, `create_file`, `analyze_data`
- Namespace related tools: `db_query`, `db_insert`, `db_delete`
- Avoid ambiguous verbs: `process`, `handle`, `manage` → use specific verbs
- Keep names under 30 characters

## Error Response Template
```json
{
  "error": true,
  "error_type": "validation_error | not_found | permission_denied | rate_limited",
  "message": "Human-readable description of what went wrong",
  "suggestion": "What the agent should try instead",
  "example": "Example of a correct call, if applicable"
}
```
