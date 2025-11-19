#!/usr/bin/env python3
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

"""
SLD/MLD/JSON converter supporting bidirectional transformations:
- JSON → SLD/MLD (with optional v2.0 typing)
- SLD/MLD → JSON
- SLD ↔ MLD
"""
import json
import sys
import unicodedata
from typing import Any, Dict, List, Optional

from validator import parse_sld, parse_mld, detect_header
from canonicalizer import encode_record, encode_header, escape_scalar


def json_to_records(data: Any) -> tuple[Optional[Dict], List[Dict]]:
    """Convert JSON to (header, records) tuple."""
    if isinstance(data, dict):
        # Check if top-level has 'records' key (with or without header)
        if 'records' in data:
            header = data.get('header')
            records = data['records']
            # Ensure records is a list
            if not isinstance(records, list):
                records = [records]
            return header, records
        # Single record (flat dict with no 'records' key)
        return None, [data]
    elif isinstance(data, list):
        return None, data
    else:
        # Scalar value wrapped
        return None, [{"value": data}]


def records_to_json(header: Optional[Dict], records: List[Dict]) -> Dict:
    """Convert (header, records) to JSON structure."""
    return {"header": header, "records": records}


def json_to_sld(json_path: str, typed: bool = False) -> str:
    """Convert JSON file to SLD format."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    header, records = json_to_records(data)
    parts: List[str] = []

    if header:
        parts.append(encode_header(header))

    for rec in records:
        parts.append(encode_record(rec))

    return '~'.join(parts) + '~'


def json_to_mld(json_path: str, typed: bool = False) -> str:
    """Convert JSON file to MLD format."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    header, records = json_to_records(data)
    lines: List[str] = []

    if header:
        lines.append(encode_header(header))

    for rec in records:
        lines.append(encode_record(rec))

    return '\n'.join(lines)


def sld_to_json(sld_path: str) -> str:
    """Convert SLD file to JSON."""
    with open(sld_path, 'r', encoding='utf-8') as f:
        data = f.read()

    records = parse_sld(data)
    header, body = detect_header(records)
    result = records_to_json(header, body)

    return json.dumps(result, ensure_ascii=False, indent=2)


def mld_to_json(mld_path: str) -> str:
    """Convert MLD file to JSON."""
    with open(mld_path, 'r', encoding='utf-8') as f:
        data = f.read()

    records = parse_mld(data)
    header, body = detect_header(records)
    result = records_to_json(header, body)

    return json.dumps(result, ensure_ascii=False, indent=2)


def sld_to_mld(sld_path: str) -> str:
    """Convert SLD to MLD (preserving structure)."""
    with open(sld_path, 'r', encoding='utf-8') as f:
        data = f.read()

    records = parse_sld(data)
    header, body = detect_header(records)
    lines: List[str] = []

    if header:
        lines.append(encode_header(header))

    for rec in body:
        lines.append(encode_record(rec))

    return '\n'.join(lines)


def mld_to_sld(mld_path: str) -> str:
    """Convert MLD to SLD (preserving structure)."""
    with open(mld_path, 'r', encoding='utf-8') as f:
        data = f.read()

    records = parse_mld(data)
    header, body = detect_header(records)
    parts: List[str] = []

    if header:
        parts.append(encode_header(header))

    for rec in body:
        parts.append(encode_record(rec))

    return '~'.join(parts) + '~'


def main(argv: List[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(
        description='Convert between JSON, SLD, and MLD formats',
        epilog='Examples:\n'
               '  convert.py --from json --to sld data.json\n'
               '  convert.py --from sld --to json data.sld\n'
               '  convert.py --from sld --to mld data.sld\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument('input', help='Input file path')
    p.add_argument('--from', dest='from_format', required=True,
                   choices=['json', 'sld', 'mld'],
                   help='Source format')
    p.add_argument('--to', dest='to_format', required=True,
                   choices=['json', 'sld', 'mld'],
                   help='Target format')
    p.add_argument('--typed', action='store_true',
                   help='Use v2.0 inline type tags (only for JSON→SLD/MLD)')
    p.add_argument('-o', '--output', help='Output file (default: stdout)')

    args = p.parse_args(argv)

    # Route conversion
    result = None

    if args.from_format == 'json' and args.to_format == 'sld':
        result = json_to_sld(args.input, args.typed)
    elif args.from_format == 'json' and args.to_format == 'mld':
        result = json_to_mld(args.input, args.typed)
    elif args.from_format == 'sld' and args.to_format == 'json':
        result = sld_to_json(args.input)
    elif args.from_format == 'mld' and args.to_format == 'json':
        result = mld_to_json(args.input)
    elif args.from_format == 'sld' and args.to_format == 'mld':
        result = sld_to_mld(args.input)
    elif args.from_format == 'mld' and args.to_format == 'sld':
        result = mld_to_sld(args.input)
    elif args.from_format == args.to_format:
        # No-op: same format
        with open(args.input, 'r', encoding='utf-8') as f:
            result = f.read()
    else:
        sys.stderr.write(f"Unsupported conversion: {args.from_format} → {args.to_format}\n")
        return 1

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
            if not result.endswith('\n'):
                f.write('\n')
    else:
        sys.stdout.write(result)
        if not result.endswith('\n'):
            sys.stdout.write('\n')

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
