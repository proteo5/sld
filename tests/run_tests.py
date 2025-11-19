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
        print(f"FAIL: {os.path.basename(inp_path)} exit={p.returncode} err={p.stderr}")
        return False
    try:
        got = json.loads(p.stdout)
        with open(exp_path, "r", encoding="utf-8") as f:
            exp = json.load(f)
        if got != exp:
            print(f"FAIL: {os.path.basename(inp_path)} output mismatch\nGOT: {json.dumps(got, ensure_ascii=False)}\nEXP: {json.dumps(exp, ensure_ascii=False)}")
            return False
        print(f"OK  : {os.path.basename(inp_path)}")
        return True
    except Exception as e:
        print(f"FAIL: {os.path.basename(inp_path)} exception {e}")
        return False


def main() -> int:
    ok = True
    ok &= run_case(os.path.join(VEC_DIR, "v11_simple.sld"), os.path.join(VEC_DIR, "v11_simple.json"), "sld")
    ok &= run_case(os.path.join(VEC_DIR, "v11_bools_and_array.sld"), os.path.join(VEC_DIR, "v11_bools_and_array.json"), "sld")
    ok &= run_case(os.path.join(VEC_DIR, "v12_header_types_null.sld"), os.path.join(VEC_DIR, "v12_header_types_null.json"), "sld")
    ok &= run_case(os.path.join(VEC_DIR, "v11_mld.mld"), os.path.join(VEC_DIR, "v11_mld.json"), "mld")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
