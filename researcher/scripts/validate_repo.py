#!/usr/bin/env python3
"""
validate_repo.py

Strict validation script for the Agent Skills for Context Engineering repository.
Validates directory structure, manifest integrity, corpus index mapping, and registry completeness.
"""

import os
import sys
import json
import argparse

# List of expected core files
CORE_FILES = [
    "README.md",
    "SKILL.md",
    "ANTIGRAVITY.md",
    "LICENSE",
    ".gitignore",
    "template/SKILL.md",
]

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

VALID_CATEGORIES = {"foundational", "architectural", "operational", "methodology", "cognitive"}

def log_error(msg, strict=True):
    print(f"[-] ERROR: {msg}", file=sys.stderr)
    if strict:
        sys.exit(1)

def log_warn(msg):
    print(f"[!] WARNING: {msg}", file=sys.stderr)

def log_info(msg):
    print(f"[+] INFO: {msg}")

def validate_structure(base_dir):
    log_info("Validating core files and directory structure...")
    for f in CORE_FILES:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            log_error(f"Missing core file: {f}")
        else:
            log_info(f"  Found core file: {f}")

    # Check skills/ directory
    skills_dir = os.path.join(base_dir, "skills")
    if not os.path.exists(skills_dir) or not os.path.isdir(skills_dir):
        log_error("Missing or invalid skills/ directory")
        return

    found_skills = set()
    for d in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, d)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, "SKILL.md")
            if not os.path.exists(skill_md):
                log_error(f"Missing SKILL.md in skills/{d}")
            found_skills.add(d)

    missing_skills = EXPECTED_SKILLS - found_skills
    extra_skills = found_skills - EXPECTED_SKILLS

    if missing_skills:
        log_error(f"Missing expected skills in skills/: {missing_skills}")
    if extra_skills:
        log_warn(f"Found unexpected skills in skills/: {extra_skills}")

    log_info("Repository structure looks good.")

def validate_manifests(base_dir):
    log_info("Validating manifests...")
    
    # 1. .antigravity/marketplace.json
    m_path = os.path.join(base_dir, ".antigravity", "marketplace.json")
    if not os.path.exists(m_path):
        log_error("Missing .antigravity/marketplace.json")
        return

    try:
        with open(m_path, "r", encoding="utf-8") as f:
            marketplace = json.load(f)
    except Exception as e:
        log_error(f"Failed to parse marketplace.json: {e}")
        return

    # Check basic fields
    required_fields = ["id", "name", "description", "version", "skills"]
    for field in required_fields:
        if field not in marketplace:
            log_error(f"marketplace.json missing field: {field}")

    m_skills = marketplace.get("skills", [])
    m_skill_ids = set()
    for s in m_skills:
        s_id = s.get("id")
        if not s_id:
            log_error("marketplace.json skill entry missing 'id'")
            continue
        m_skill_ids.add(s_id)
        
        path = s.get("path")
        if not path or not os.path.exists(os.path.join(base_dir, path)):
            log_error(f"marketplace.json skill '{s_id}' points to non-existent path: {path}")

        cat = s.get("category")
        if cat not in VALID_CATEGORIES:
            log_error(f"marketplace.json skill '{s_id}' has invalid category: {cat}")

    missing_m_skills = EXPECTED_SKILLS - m_skill_ids
    if missing_m_skills:
        log_error(f"marketplace.json missing expected skills: {missing_m_skills}")

    # 2. .plugin/plugin.json
    p_path = os.path.join(base_dir, ".plugin", "plugin.json")
    if not os.path.exists(p_path):
        log_error("Missing .plugin/plugin.json")
        return

    try:
        with open(p_path, "r", encoding="utf-8") as f:
            plugin = json.load(f)
    except Exception as e:
        log_error(f"Failed to parse plugin.json: {e}")
        return

    p_skills = set(plugin.get("skills", []))
    missing_p_skills = EXPECTED_SKILLS - p_skills
    if missing_p_skills:
        log_error(f"plugin.json missing expected skills: {missing_p_skills}")

    log_info("Manifest validation passed.")

def validate_registries(base_dir):
    log_info("Validating mechanisms registry, claims index, corpus index, and benchmarks...")

    # Load mechanisms
    mech_path = os.path.join(base_dir, "researcher", "mechanisms", "registry.jsonl")
    mechanisms = {}
    if not os.path.exists(mech_path):
        log_error("Missing researcher/mechanisms/registry.jsonl")
    else:
        with open(mech_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    m_id = data.get("id")
                    if not m_id or not m_id.startswith("mech-"):
                        log_error(f"registry.jsonl line {i}: invalid id '{m_id}'")
                    mechanisms[m_id] = data
                except Exception as e:
                    log_error(f"registry.jsonl line {i}: failed to parse JSON: {e}")

    # Load claims
    claim_path = os.path.join(base_dir, "researcher", "claims", "index.jsonl")
    claims = {}
    if not os.path.exists(claim_path):
        log_error("Missing researcher/claims/index.jsonl")
    else:
        with open(claim_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    c_id = data.get("id")
                    if not c_id or not c_id.startswith("claim-"):
                        log_error(f"claims index.jsonl line {i}: invalid id '{c_id}'")
                    claims[c_id] = data
                except Exception as e:
                    log_error(f"claims index.jsonl line {i}: failed to parse JSON: {e}")

    # Load activation cases
    ac_path = os.path.join(base_dir, "researcher", "benchmarks", "activation-cases.jsonl")
    if not os.path.exists(ac_path):
        log_error("Missing researcher/benchmarks/activation-cases.jsonl")
    else:
        with open(ac_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    expected = data.get("expected_skill")
                    not_expected = data.get("not_skill")
                    if expected not in EXPECTED_SKILLS:
                        log_error(f"activation-cases.jsonl line {i}: expected_skill '{expected}' is invalid")
                    if not_expected not in EXPECTED_SKILLS:
                        log_error(f"activation-cases.jsonl line {i}: not_skill '{not_expected}' is invalid")
                except Exception as e:
                    log_error(f"activation-cases.jsonl line {i}: failed to parse JSON: {e}")

    # Load corpus index
    corpus_path = os.path.join(base_dir, "researcher", "corpus", "index.json")
    if not os.path.exists(corpus_path):
        log_error("Missing researcher/corpus/index.json")
        return

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus = json.load(f)
    except Exception as e:
        log_error(f"Failed to parse corpus index.json: {e}")
        return

    corpus_skills = corpus.get("skills", {})
    for s_name, s_data in corpus_skills.items():
        if s_name not in EXPECTED_SKILLS:
            log_error(f"corpus index.json contains unexpected skill: {s_name}")
            continue

        # Check mechanisms
        for m in s_data.get("mechanisms", []):
            if m not in mechanisms:
                log_error(f"Skill '{s_name}' references unregistered mechanism '{m}' in corpus index")
            elif s_name not in mechanisms[m].get("skills", []):
                log_error(f"Mechanism '{m}' registry entry does not list skill '{s_name}'")

        # Check claims
        for c in s_data.get("claims", []):
            if c not in claims:
                log_error(f"Skill '{s_name}' references unregistered claim '{c}' in corpus index")
            elif s_name not in claims[c].get("skills", []):
                log_error(f"Claim '{c}' index entry does not list skill '{s_name}'")

        # Check references files exist
        for ref_path in s_data.get("references", []):
            full_ref_path = os.path.join(base_dir, ref_path)
            if not os.path.exists(full_ref_path):
                log_error(f"Skill '{s_name}' references non-existent reference file: {ref_path}")

    # Ensure all mechanisms are mapped to at least one skill in corpus
    for m_id, m_data in mechanisms.items():
        m_skills = m_data.get("skills", [])
        if not m_skills:
            log_warn(f"Mechanism '{m_id}' is registered but maps to no skills")
        for ms in m_skills:
            if ms not in corpus_skills:
                log_error(f"Mechanism '{m_id}' lists skill '{ms}' but skill is missing in corpus index")
            elif m_id not in corpus_skills[ms].get("mechanisms", []):
                log_error(f"Mechanism '{m_id}' lists skill '{ms}' but skill corpus index entry does not list mechanism")

    log_info("Registry validation passed.")

def main():
    parser = argparse.ArgumentParser(description="Validate repository structure and content maps.")
    parser.add_argument("--strict", action="store_true", help="Fail and exit with code 1 on errors.")
    args = parser.parse_args()

    # Base dir is the parent of researcher/scripts
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    try:
        validate_structure(base_dir)
        validate_manifests(base_dir)
        validate_registries(base_dir)
        log_info("All validation gates passed successfully.")
    except Exception as e:
        log_error(f"An unexpected error occurred during validation: {e}", strict=args.strict)
        sys.exit(1)

if __name__ == "__main__":
    main()
