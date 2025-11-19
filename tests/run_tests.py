# Copyright 2025 Alfredo Pinto Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TOOLS = os.path.join(ROOT, "tools")
VALIDATOR = os.path.join(TOOLS, "validator.py")
VEC_DIR = os.path.join(os.path.dirname(__file__), "vectors")


def run_case(inp_path: str, exp_path: str, force_fmt: str = None) -> bool:
    cmd = [sys.executable, VALIDATOR, inp_path]
    if force_fmt:
        cmd += ["--format", force_fmt]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        print(f"FAIL: {os.path.basename(inp_path)} exit={p.returncode} err={p.stderr.strip()[:100]}")
        return False
    try:
        got = json.loads(p.stdout)
        with open(exp_path, "r", encoding="utf-8") as f:
            exp = json.load(f)
        if got != exp:
            print(f"FAIL: {os.path.basename(inp_path)} output mismatch")
            print(f"  GOT: {json.dumps(got, ensure_ascii=False)[:200]}")
            print(f"  EXP: {json.dumps(exp, ensure_ascii=False)[:200]}")
            return False
        print(f"PASS: {os.path.basename(inp_path)}")
        return True
    except Exception as e:
        print(f"FAIL: {os.path.basename(inp_path)} exception {e}")
        return False


def discover_tests():
    """Auto-discover test pairs (*.sld/*.mld → *.json)"""
    tests = []

    # Find all .sld files with matching .json
    for sld_path in glob.glob(os.path.join(VEC_DIR, "*.sld")):
        base = os.path.splitext(sld_path)[0]
        json_path = base + ".json"
        if os.path.exists(json_path):
            tests.append((sld_path, json_path, "sld"))

    # Find all .mld files with matching .json
    for mld_path in glob.glob(os.path.join(VEC_DIR, "*.mld")):
        base = os.path.splitext(mld_path)[0]
        json_path = base + ".json"
        if os.path.exists(json_path):
            tests.append((mld_path, json_path, "mld"))

    return tests


def main() -> int:
    tests = discover_tests()

    if not tests:
        print("No test vectors found!")
        return 1

    print(f"Running {len(tests)} conformance tests...\n")

    passed = 0
    failed = 0

    for inp_path, exp_path, fmt in sorted(tests):
        if run_case(inp_path, exp_path, fmt):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
