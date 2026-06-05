#!/usr/bin/env python3
"""
run_router_llm.py

Runs the router benchmark end-to-end against real LLMs using API keys provided in the environment.
Supports Google Gemini, OpenAI, and Anthropic providers.
"""

import os
import sys
import json
import re
import argparse

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

def load_skills_descriptions(base_dir):
    skills_desc = {}
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
        skills_desc[s_name] = description
    return skills_desc

def construct_prompt(query, skills_desc):
    skills_block = "\n".join([f"- **{name}**: {desc}" for name, desc in skills_desc.items()])
    
    prompt = f"""You are a skill routing system. Your task is to select the most appropriate context engineering skill for a given user query.

Available Skills:
{skills_block}

User Query: "{query}"

Respond strictly in JSON format containing a ranked list of skill names in order of relevance, with the primary matching skill at index 0. Do not include any markdown fences or conversational text outside the JSON.

Example Response:
{{
  "ranked_skills": ["context-fundamentals", "context-degradation"]
}}
"""
    return prompt

def call_gemini(prompt, model_name, api_key):
    try:
        import google.generativeai as genai
    except ImportError:
        print("[-] Error: 'google-generativeai' package is not installed. Run: pip install google-generativeai")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return response.text

def call_openai(prompt, model_name, api_key):
    try:
        from openai import OpenAI
    except ImportError:
        print("[-] Error: 'openai' package is not installed. Run: pip install openai")
        sys.exit(1)
        
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def call_anthropic(prompt, model_name, api_key):
    try:
        import anthropic
    except ImportError:
        print("[-] Error: 'anthropic' package is not installed. Run: pip install anthropic")
        sys.exit(1)
        
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model_name,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    parser = argparse.ArgumentParser(description="Run LLM routing benchmarks.")
    parser.add_argument("--provider", choices=["gemini", "openai", "anthropic"], required=True, help="LLM API provider")
    parser.add_argument("--model", required=True, help="Model name (e.g. gemini-1.5-flash, gpt-4o, claude-3-5-sonnet)")
    parser.add_argument("--api-key", help="API key (defaults to standard provider env variables)")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ac_file = os.path.join(base_dir, "researcher", "benchmarks", "activation-cases.jsonl")

    if not os.path.exists(ac_file):
        print(f"[-] Missing activation cases: {ac_file}")
        sys.exit(1)

    # Get API key from argument or environment
    api_key = args.api_key
    if not api_key:
        env_vars = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        api_key = os.environ.get(env_vars[args.provider])
        
    if not api_key:
        print(f"[-] Error: API key for provider '{args.provider}' not found. Please set the env var or pass --api-key.")
        sys.exit(1)

    skills_desc = load_skills_descriptions(base_dir)
    cases = []
    with open(ac_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))

    print(f"[+] Loaded {len(cases)} benchmark activation cases.")
    print(f"[+] Benchmarking model '{args.model}' via {args.provider.upper()}...")

    passed = 0
    total = 0

    for case in cases:
        query = case["query"]
        expected = case["expected_skill"]
        not_expected = case["not_skill"]
        case_id = case["id"]

        prompt = construct_prompt(query, skills_desc)
        
        try:
            if args.provider == "gemini":
                raw_response = call_gemini(prompt, args.model, api_key)
            elif args.provider == "openai":
                raw_response = call_openai(prompt, args.model, api_key)
            elif args.provider == "anthropic":
                raw_response = call_anthropic(prompt, args.model, api_key)
                
            # Clean response text if there are markdown code fences
            clean_json = raw_response.strip()
            if clean_json.startswith("```"):
                # Remove starting and ending markdown ticks
                clean_json = re.sub(r"^```[a-zA-Z]*\n", "", clean_json)
                clean_json = re.sub(r"\n```$", "", clean_json)
                
            res_data = json.loads(clean_json)
            ranked = res_data.get("ranked_skills", [])
            
            if not ranked:
                print(f"[-] Case {case_id}: Empty ranked list returned.")
                continue
                
            top_pred = ranked[0]
            total += 1
            
            # Verify if correct
            if top_pred == expected:
                print(f"[+] Case {case_id} [{query}]: PASSED (Routed to expected: {expected})")
                passed += 1
            else:
                print(f"[-] Case {case_id} [{query}]: FAILED. Expected: {expected}, Got: {top_pred}")
                
        except Exception as e:
            print(f"[-] Case {case_id}: Failed with exception: {e}")

    if total > 0:
        accuracy = passed / total
        print(f"\n==========================================")
        print(f"Benchmark Results for Model: {args.model}")
        print(f"Total Attempted: {total}")
        print(f"Total Correct: {passed}")
        print(f"Routing Accuracy: {accuracy * 100:.1f}%")
        print(f"==========================================")
    else:
        print("[-] No benchmark cases could be run successfully.")

if __name__ == "__main__":
    main()
