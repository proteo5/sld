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

import sys
import unicodedata
from typing import Any, Dict, List

from validator import parse_sld, parse_mld, detect_header, ESC, FIELD_SEP, REC_SEP_SLD

# Canonicalization rules (draft v1.2 profile):
# - Stable key ordering (lexicographic)
# - NFC normalization of all string scalars
# - No trailing '~' inside arrays
# - Typed null encoded as !n[
# - Booleans encoded as !b[1 or !b[0
# - Optional scalar typing for simple numeric types (int/float) using !i / !f
# - Arrays encoded with '{' elements joined by '~' and closed with '}'
# - Records separated by '~' for SLD; newline for MLD


def escape_scalar(value: str) -> str:
    # Escape special characters and caret
    return (value
            .replace('^', '^^')
            .replace(';', '^;')
            .replace('~', '^~')
            .replace('[', '^[')
            .replace('{', '^{')
            .replace('}', '^}')
            )


def encode_value(key: str, value: Any) -> str:
    # Decide typed vs untyped
    if value is None:
        return f"{key}!n["
    if isinstance(value, bool):
        return f"{key}!b[{1 if value else 0}"
    if isinstance(value, int) and not isinstance(value, bool):
        return f"{key}!i[{value}"
    if isinstance(value, float):
        # Use plain representation (could refine)
        return f"{key}!f[{value}"
    if isinstance(value, list):
        elems = []
        for elem in value:
            if elem is None:
                elems.append('!n[')  # element null
            elif isinstance(elem, bool):
                elems.append(f"!b[{1 if elem else 0}")
            elif isinstance(elem, int) and not isinstance(elem, bool):
                elems.append(f"!i[{elem}")
            elif isinstance(elem, float):
                elems.append(f"!f[{elem}")
            else:
                s = unicodedata.normalize('NFC', str(elem))
                elems.append(escape_scalar(s))
        return f"{key}{{{'~'.join(elems)}}}"  # no trailing ~
    # fallback string
    s = unicodedata.normalize('NFC', str(value))
    return f"{key}[{escape_scalar(s)}"


def encode_record(rec: Dict[str, Any]) -> str:
    parts: List[str] = []
    for k, v in sorted(rec.items(), key=lambda kv: kv[0]):
        parts.append(encode_value(k, v))
    return ';'.join(parts)


def encode_header(header: Dict[str, Any]) -> str:
    # Keep original order for header keys (already reserved with '!')
    parts: List[str] = []
    for k in sorted(header.keys()):
        v = header[k]
        parts.append(encode_value(k, v))
    return ';'.join(parts)


def canonicalize_sld(text: str) -> str:
    records = parse_sld(text)
    header, body = detect_header(records)
    out_parts: List[str] = []
    if header:
        out_parts.append(encode_header(header))
    for rec in body:
        out_parts.append(encode_record(rec))
    return '~'.join(out_parts) + '~'


def canonicalize_mld(text: str) -> str:
    records = parse_mld(text)
    header, body = detect_header(records)
    lines: List[str] = []
    if header:
        lines.append(encode_header(header))
    for rec in body:
        lines.append(encode_record(rec))
    return '\n'.join(lines)


def main(argv: List[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(description="Canonicalize SLD/MLD input")
    p.add_argument('file', help='Input .sld or .mld file')
    p.add_argument('--format', choices=['sld', 'mld'], help='Force format detection')
    args = p.parse_args(argv)

    with open(args.file, 'r', encoding='utf-8') as f:
        data = f.read()

    fmt = args.format
    if fmt is None:
        fmt = 'mld' if '\n' in data and not data.strip().endswith('~') else 'sld'

    if fmt == 'sld':
        sys.stdout.write(canonicalize_sld(data) + '\n')
    else:
        sys.stdout.write(canonicalize_mld(data) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
