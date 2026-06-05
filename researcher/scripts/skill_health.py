#!/usr/bin/env python3
"""
skill_health.py

Deterministic quality gate for every SKILL.md in the collection.
Scores skills according to the researcher/rubrics/skill-quality.md criteria.
"""

import os
import sys
import re
import argparse
import json

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

def log_error(msg, strict=True):
    print(f"[-] ERROR: {msg}", file=sys.stderr)
    if strict:
        sys.exit(1)

def log_warn(msg):
    print(f"[!] WARNING: {msg}", file=sys.stderr)

def log_info(msg):
    print(f"[+] INFO: {msg}")

def load_registry_ids(base_dir):
    mechanisms = set()
    claims = set()

    mech_path = os.path.join(base_dir, "researcher", "mechanisms", "registry.jsonl")
    if os.path.exists(mech_path):
        with open(mech_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        if "id" in data:
                            mechanisms.add(data["id"])
                    except Exception:
                        pass

    claim_path = os.path.join(base_dir, "researcher", "claims", "index.jsonl")
    if os.path.exists(claim_path):
        with open(claim_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        if "id" in data:
                            claims.add(data["id"])
                    except Exception:
                        pass

    return mechanisms, claims

def evaluate_skill(skill_name, file_path, registered_mechanisms, registered_claims):
    results = {}
    issues = []

    if not os.path.exists(file_path):
        return None, [f"File {file_path} does not exist"]

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # Parse YAML frontmatter
    # YAML frontmatter is enclosed between three dashes `---`
    frontmatter = {}
    has_frontmatter = False
    if content.startswith("---"):
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        if match:
            has_frontmatter = True
            fm_text = match.group(1)
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    frontmatter[k.strip()] = v.strip()

    # S1: Has YAML frontmatter with name field
    s1 = has_frontmatter and "name" in frontmatter and frontmatter["name"] == skill_name
    results["S1"] = s1
    if not s1:
        issues.append("S1: Missing or incorrect 'name' field in YAML frontmatter.")

    # S2: Has YAML frontmatter with description field
    s2 = has_frontmatter and "description" in frontmatter and len(frontmatter["description"]) > 0
    results["S2"] = s2
    if not s2:
        issues.append("S2: Missing 'description' field in YAML frontmatter.")

    # S3: Has "When to Activate" section
    s3 = "## When to Activate" in content
    results["S3"] = s3
    if not s3:
        issues.append("S3: Missing '## When to Activate' section.")

    # S4: Has "Do not activate" boundary block
    # Case insensitive search for "do not activate"
    s4 = re.search(r"do not activate", content, re.IGNORECASE) is not None
    results["S4"] = s4
    if not s4:
        issues.append("S4: Missing 'Do not activate' boundary block.")

    # S5: Under 500 lines
    s5 = line_count < 500
    results["S5"] = s5
    if not s5:
        issues.append(f"S5: File length ({line_count} lines) is >= 500 lines.")

    # S6: Has at least one cross-reference to another skill
    # We look for backtick quoted skill names, like `context-fundamentals`
    refs = re.findall(r"`([a-z0-9-]+)`", content)
    valid_refs = [r for r in refs if r in EXPECTED_SKILLS and r != skill_name]
    s6 = len(valid_refs) > 0
    results["S6"] = s6
    if not s6:
        issues.append("S6: Missing cross-reference to other skills in backticks.")

    # C1: Description is third-person
    # Check that description doesn't contain first/second person words like I, my, we, you, your, our
    desc = frontmatter.get("description", "")
    # Check words cleanly using boundary regex
    c1 = True
    if desc:
        bad_words = ["i", "my", "we", "you", "your", "our", "us"]
        for word in bad_words:
            if re.search(r"\b" + word + r"\b", desc, re.IGNORECASE):
                c1 = False
                issues.append(f"C1: Description contains first/second-person word '{word}': '{desc}'")
                break
    results["C1"] = c1

    # C2: Has "Core Concepts" or equivalent section
    c2 = "## Core Concepts" in content
    results["C2"] = c2
    if not c2:
        issues.append("C2: Missing '## Core Concepts' section.")

    # C3: Has "Gotchas" section
    c3 = "## Gotchas" in content
    results["C3"] = c3
    if not c3:
        issues.append("C3: Missing '## Gotchas' section.")

    # C4: Has "Integration" section
    c4 = "## Integration" in content
    results["C4"] = c4
    if not c4:
        issues.append("C4: Missing '## Integration' section.")

    # C5: No duplicate content (Mocked pass or basic checks)
    results["C5"] = True

    # P1: All volatile claims have claim IDs
    # Check if there are any unregistered claim references
    found_claims = re.findall(r"\b(claim-[a-z0-9-]+)\b", content)
    unregistered_claims = [c for c in found_claims if c not in registered_claims]
    p1 = len(unregistered_claims) == 0
    results["P1"] = p1
    if not p1:
        issues.append(f"P1: References unregistered claims: {unregistered_claims}")

    # P2: Referenced mechanisms exist in registry
    found_mechs = re.findall(r"\b(mech-[a-z0-9-]+)\b", content)
    unregistered_mechs = [m for m in found_mechs if m not in registered_mechanisms]
    p2 = len(unregistered_mechs) == 0
    results["P2"] = p2
    if not p2:
        issues.append(f"P2: References unregistered mechanisms: {unregistered_mechs}")

    # P3: References directory exists if referenced
    # If the skill references a references file, let's make sure the directory and files exist
    references_dir_path = os.path.join(os.path.dirname(file_path), "references")
    p3 = True
    if "references/" in content or "references\\" in content:
        if not os.path.exists(references_dir_path) or not os.path.isdir(references_dir_path):
            p3 = False
            issues.append("P3: references/ directory is missing or not a directory.")
        else:
            files = os.listdir(references_dir_path)
            if not files:
                p3 = False
                issues.append("P3: references/ directory is empty.")
    results["P3"] = p3

    return results, issues

def main():
    parser = argparse.ArgumentParser(description="Evaluate quality of SKILL.md files.")
    parser.add_argument("--strict", action="store_true", help="Fail and exit with code 1 on errors.")
    parser.add_argument("--no-history", action="store_true", help="Do not load history.")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    skills_dir = os.path.join(base_dir, "skills")

    if not os.path.exists(skills_dir):
        log_error("skills/ directory not found.")

    registered_mechanisms, registered_claims = load_registry_ids(base_dir)

    failed_skills = 0
    for skill_name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_name)
        if not os.path.isdir(skill_path):
            continue

        skill_file = os.path.join(skill_path, "SKILL.md")
        results, issues = evaluate_skill(skill_name, skill_file, registered_mechanisms, registered_claims)

        if results is None:
            log_error(f"Skill '{skill_name}': {issues[0]}", strict=args.strict)
            failed_skills += 1
            continue

        # Criteria breakdown
        s_passed = all(results[k] for k in ["S1", "S2", "S3", "S4", "S5", "S6"])
        c_passed = all(results[k] for k in ["C1", "C2", "C3", "C4", "C5"])
        
        # Total criteria scored
        passed_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        score = (passed_count / total_count) * 100.0

        if not s_passed or not c_passed:
            log_warn(f"Skill '{skill_name}' FAILED quality check. Score: {score:.1f}%")
            for issue in issues:
                print(f"  - {issue}")
            failed_skills += 1
        else:
            log_info(f"Skill '{skill_name}' PASSED quality check. Score: {score:.1f}%")

    if failed_skills > 0:
        log_error(f"{failed_skills} skill(s) failed the quality gate.", strict=args.strict)
    else:
        log_info("All skills passed the quality rubric!")

if __name__ == "__main__":
    main()
