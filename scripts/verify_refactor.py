#!/usr/bin/env python3
"""
verify_refactor.py — Verify no tests lost during refactor.

Usage:
    python scripts/verify_refactor.py <module_dir> <old_commit>

Example:
    python scripts/verify_refactor.py tests/patient_outreach HEAD~1
"""

import sys
import subprocess


def get_test_names_from_git(commit, module_dir):
    """Get all test function names from a git commit."""
    # Get all .py files in module at that commit
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit],
        capture_output=True, text=True
    )
    files = [f for f in result.stdout.splitlines()
             if f.startswith(module_dir) and f.endswith(".py") and "conftest" not in f]

    tests = set()
    for f in files:
        result = subprocess.run(
            ["git", "show", f"{commit}:{f}"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("def test_"):
                name = line.split("(")[0].replace("def ", "")
                tests.add(name)
    return tests


def get_test_names_current(module_dir):
    """Get all test function names from current files."""
    import glob
    tests = set()
    for f in glob.glob(f"{module_dir}/*.py"):
        if "conftest" in f:
            continue
        with open(f) as fp:
            for line in fp:
                if line.startswith("def test_"):
                    name = line.split("(")[0].replace("def ", "").strip()
                    tests.add(name)
    return tests


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    module_dir = sys.argv[1]
    old_commit = sys.argv[2]

    old_tests = get_test_names_from_git(old_commit, module_dir)
    new_tests = get_test_names_current(module_dir)

    missing = old_tests - new_tests
    added = new_tests - old_tests

    print(f"\n{'='*50}")
    print(f"Module: {module_dir}")
    print(f"Old commit: {old_commit}")
    print(f"{'='*50}")
    print(f"OLD: {len(old_tests)} tests")
    print(f"NEW: {len(new_tests)} tests")

    if missing:
        print(f"\n❌ MISSING ({len(missing)}):")
        for t in sorted(missing):
            print(f"  - {t}")
    else:
        print("\n✅ No tests missing")

    if added:
        print(f"\n➕ ADDED ({len(added)}):")
        for t in sorted(added):
            print(f"  + {t}")

    if not missing:
        print("\n✅ REFACTOR SAFE")
    else:
        print("\n❌ REFACTOR HAS MISSING TESTS")
        sys.exit(1)
