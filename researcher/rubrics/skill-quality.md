# Skill Quality Rubric

## Purpose
Deterministic quality gate for every SKILL.md in the collection. Each criterion is binary pass/fail with no subjective interpretation.

## Rubric Criteria

### Structure (must all pass)

| ID | Criterion | Check |
|----|-----------|-------|
| S1 | Has YAML frontmatter with `name` field | `grep -c "^name:" SKILL.md` |
| S2 | Has YAML frontmatter with `description` field | `grep -c "^description:" SKILL.md` |
| S3 | Has "When to Activate" section | `grep -c "## When to Activate" SKILL.md` |
| S4 | Has "Do not activate" boundary block | `grep -c "Do not activate" SKILL.md` |
| S5 | Under 500 lines | `wc -l SKILL.md` |
| S6 | Has at least one cross-reference to another skill | grep for backtick-quoted skill names |

### Content Quality (must all pass)

| ID | Criterion | Check |
|----|-----------|-------|
| C1 | Description is third-person | No "I can", "you should" in description |
| C2 | Has "Core Concepts" or equivalent section | Section header present |
| C3 | Has "Gotchas" section | `grep -c "## Gotchas" SKILL.md` |
| C4 | Has "Integration" section | `grep -c "## Integration" SKILL.md` |
| C5 | No duplicate content with adjacent skills | Manual review + grep for shared paragraphs |

### Provenance (should pass)

| ID | Criterion | Check |
|----|-----------|-------|
| P1 | All volatile claims have claim IDs | Claims reference `claim-<skill>-<topic>` |
| P2 | Referenced mechanisms exist in registry | Cross-check with `mechanisms/registry.jsonl` |
| P3 | References directory exists if referenced | Directory presence check |

## Scoring

- **Pass**: All S* and C* criteria pass, P* criteria advisory
- **Fail**: Any S* or C* criterion fails
- **Score**: Count of passing criteria / total criteria × 100%

## Minimum Thresholds

- New skills: Must pass 100% of S* and C* criteria
- Existing skills: Must pass 100% of S* criteria, 80% of C* criteria
- All skills: P* criteria are tracked but not blocking
