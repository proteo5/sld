import json
import os
import re
import sys
from typing import List, Dict, Any

from validator import parse_sld, parse_mld
from canonicalizer import canonicalize_sld, canonicalize_mld

TOKEN_SPLIT = re.compile(r"[A-Za-z0-9_]+|[{};~\n\[\]^,:.-]")


def approx_tokens(s: str) -> int:
    return len(TOKEN_SPLIT.findall(s))


def load(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main(argv: List[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(description='Approximate token benchmark for SLD/MLD vs JSON')
    p.add_argument('--json', help='Optional JSON file to compare')
    p.add_argument('--sld', help='SLD file')
    p.add_argument('--mld', help='MLD file')
    args = p.parse_args(argv)

    rows: List[Dict[str, Any]] = []

    if args.json and os.path.exists(args.json):
        js = load(args.json)
        rows.append({"format": "JSON", "chars": len(js), "tokens": approx_tokens(js)})

    if args.sld and os.path.exists(args.sld):
        s = load(args.sld)
        rows.append({"format": "SLD(raw)", "chars": len(s), "tokens": approx_tokens(s)})
        cs = canonicalize_sld(s)
        rows.append({"format": "SLD(canon)", "chars": len(cs), "tokens": approx_tokens(cs)})

    if args.mld and os.path.exists(args.mld):
        m = load(args.mld)
        rows.append({"format": "MLD(raw)", "chars": len(m), "tokens": approx_tokens(m)})
        cm = canonicalize_mld(m)
        rows.append({"format": "MLD(canon)", "chars": len(cm), "tokens": approx_tokens(cm)})

    # Print table
    if not rows:
        print("No input files provided.")
        return 1

    w_format = max(len(r['format']) for r in rows)
    print(f"{'Format'.ljust(w_format)}  Chars  Tokens")
    print(f"{'-'*w_format}  -----  ------")
    for r in rows:
        print(f"{r['format'].ljust(w_format)}  {str(r['chars']).rjust(5)}  {str(r['tokens']).rjust(6)}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
