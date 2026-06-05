#!/usr/bin/env python3
"""
run_benchmarks.py

Harness runner executing all validation and benchmark checks as a unified suite.
Runs validate_repo.py, skill_health.py, and check_activation_cases.py.
"""

import os
import sys
import subprocess

def run_script(script_path, args=[]):
    print(f"\n======================================================================")
    print(f"RUNNING: {os.path.basename(script_path)} {' '.join(args)}")
    print(f"======================================================================")
    
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print(f"[-] {os.path.basename(script_path)} FAILED with exit code {result.returncode}")
        return False
    else:
        print(f"[+] {os.path.basename(script_path)} PASSED")
        return True

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    
    validate_repo = os.path.join(scripts_dir, "validate_repo.py")
    skill_health = os.path.join(scripts_dir, "skill_health.py")
    check_activation = os.path.join(scripts_dir, "check_activation_cases.py")

    all_passed = True

    # 1. Run Repository Validation
    if not run_script(validate_repo, ["--strict"]):
        all_passed = False

    # 2. Run Skill Health Rubrics Check
    if not run_script(skill_health, ["--strict", "--no-history"]):
        all_passed = False

    # 3. Run Activation Boundaries Check
    if not run_script(check_activation):
        all_passed = False

    print("\n======================================================================")
    if all_passed:
        print("[+] ALL BENCHMARKS AND VALIDATION GATES PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("[-] ONE OR MORE VALIDATION GATES FAILED. SEE DETAILS ABOVE.")
        sys.exit(1)

if __name__ == "__main__":
    main()
