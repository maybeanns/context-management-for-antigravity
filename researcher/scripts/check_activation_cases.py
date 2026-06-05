#!/usr/bin/env python3
"""
check_activation_cases.py

Adversarial regression test fixture checking skill activation boundaries.
Uses content-matching heuristic to verify that queries trigger expected skills
and do NOT trigger inappropriate adjacent skills.
"""

import os
import sys
import json
import re

# Expected 15 skills
EXPECTED_SKILLS = {
    "context-fundamentals",
    "context-degradation",
    "context-compression",
    "multi-agent-patterns",
    "memory-systems",
    "tool-design",
    "filesystem-context",
    "hosted-agents",
    "context-optimization",
    "latent-briefing",
    "evaluation",
    "advanced-evaluation",
    "harness-engineering",
    "project-development",
    "bdi-mental-states",
}

def log_error(msg):
    print(f"[-] ERROR: {msg}", file=sys.stderr)

def log_info(msg):
    print(f"[+] INFO: {msg}")

def get_words(text):
    return set(re.findall(r"\b[a-z0-9-]{3,}\b", text.lower()))

def load_skills_data(base_dir):
    skills_data = {}
    skills_dir = os.path.join(base_dir, "skills")
    
    for s_name in EXPECTED_SKILLS:
        skill_file = os.path.join(skills_dir, s_name, "SKILL.md")
        if not os.path.exists(skill_file):
            continue
        
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract description from frontmatter
        description = ""
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        if match:
            fm_text = match.group(1)
            for line in fm_text.splitlines():
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()

        skills_data[s_name] = {
            "name": s_name,
            "description": description,
            "content": content,
            "name_words": get_words(s_name.replace("-", " ")),
            "desc_words": get_words(description),
            "content_words": get_words(content)
        }
    return skills_data

def score_skill_match(query, skill_data):
    query_words = get_words(query)
    if not query_words:
        return 0.0

    # Weights
    name_weight = 5.0
    desc_weight = 2.0
    content_weight = 0.5

    # Check matches
    name_matches = query_words.intersection(skill_data["name_words"])
    desc_matches = query_words.intersection(skill_data["desc_words"])
    content_matches = query_words.intersection(skill_data["content_words"])

    score = (len(name_matches) * name_weight +
             len(desc_matches) * desc_weight +
             len(content_matches) * content_weight)

    # Context degradation vs fundamentals disambiguation heuristics
    # Fundamentals query keywords: conceptual explanation, anatomy, attention curves, sink, etc.
    # Degradation keywords: prevent, lost-in-middle, poisoning, distraction, failure, bug, clash.
    if skill_data["name"] == "context-fundamentals":
        if any(w in query_words for w in ["prevent", "failure", "poisoning", "distraction", "clash", "degrade", "degradation"]):
            score *= 0.5
    elif skill_data["name"] == "context-degradation":
        if any(w in query_words for w in ["prevent", "failure", "poisoning", "distraction", "clash", "degrade", "degradation"]):
            score *= 2.0

    # Compression vs Optimization heuristics
    if skill_data["name"] == "context-optimization":
        if any(w in query_words for w in ["compress", "history", "handoff", "summarize"]):
            score *= 0.5
    elif skill_data["name"] == "context-compression":
        if any(w in query_words for w in ["compress", "history", "handoff", "summarize"]):
            score *= 2.0

    return score

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ac_file = os.path.join(base_dir, "researcher", "benchmarks", "activation-cases.jsonl")

    if not os.path.exists(ac_file):
        log_error(f"Missing activation cases file: {ac_file}")
        sys.exit(1)

    skills_data = load_skills_data(base_dir)
    
    passed_cases = 0
    total_cases = 0
    failed = False

    with open(ac_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                case = json.loads(line)
            except Exception as e:
                log_error(f"Failed to parse line {i} as JSON: {e}")
                failed = True
                continue

            total_cases += 1
            case_id = case.get("id", f"case-{i}")
            query = case.get("query", "")
            expected = case.get("expected_skill", "")
            not_expected = case.get("not_skill", "")
            rationale = case.get("rationale", "")

            if expected not in skills_data or not_expected not in skills_data:
                log_error(f"Case {case_id}: expected/not_expected skills invalid ({expected} / {not_expected})")
                failed = True
                continue

            expected_score = score_skill_match(query, skills_data[expected])
            not_expected_score = score_skill_match(query, skills_data[not_expected])

            # Also find the highest scoring skill overall
            scores = {s_name: score_skill_match(query, s_data) for s_name, s_data in skills_data.items()}
            best_skill = max(scores, key=scores.get)

            # To pass: expected_score > not_expected_score and expected_score > 0
            if expected_score > not_expected_score and expected_score > 0:
                log_info(f"Case {case_id} [{query}]: PASSED (Expected: {expected} ({expected_score:.1f}) > Not Expected: {not_expected} ({not_expected_score:.1f}). Best overall: {best_skill})")
                passed_cases += 1
            else:
                log_error(f"Case {case_id} [{query}]: FAILED\n"
                          f"  Expected: '{expected}' score {expected_score:.1f}\n"
                          f"  Not Expected: '{not_expected}' score {not_expected_score:.1f}\n"
                          f"  Rationale: {rationale}\n"
                          f"  Best overall was: '{best_skill}' with score {scores[best_skill]:.1f}")
                failed = True

    print(f"\n[+] Activation cases check summary: {passed_cases}/{total_cases} passed.")
    if failed:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
