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

import json
import sys
import unicodedata
from typing import Any, Dict, List, Optional, Tuple


# SLD/MLD core tokens (v2.0)
FIELD_SEP = ";"
REC_SEP_SLD = "~"
REC_SEP_MLD = "\n"
PROP_MARK = "["
ARR_OPEN = "{"
ARR_CLOSE = "}"
ESC = "^"

TYPE_CODES = {"i", "f", "b", "s", "n", "d", "t", "ts"}


class ParseError(Exception):
    def __init__(self, message: str, pos: Optional[int] = None, code: str = "E01"):
        super().__init__(message)
        self.pos = pos
        self.code = code


def _is_escaped(s: str, i: int) -> bool:
    # Not needed with our scanning approach; left for completeness
    return i > 0 and s[i - 1] == ESC


def _unescape(text: str) -> Tuple[Any, bool, bool]:
    """Unescape a scalar value.

    Returns (value, is_bool, is_null_legacy)
    - is_bool True when produced by ^1/^0
    - is_null_legacy True when produced by ^_
    """
    if text is None:
        return "", False, False

    out: List[str] = []
    i = 0
    is_bool = False
    is_null = False
    while i < len(text):
        ch = text[i]
        if ch == ESC:
            if i + 1 >= len(text):
                # dangling escape, keep literally
                out.append(ESC)
                i += 1
                continue
            nxt = text[i + 1]
            if nxt == "1":
                out.append("True")
                is_bool = True
                i += 2
            elif nxt == "0":
                out.append("False")
                is_bool = True
                i += 2
            elif nxt == "_":
                # legacy null
                is_null = True
                i += 2
            else:
                out.append(nxt)
                i += 2
        else:
            out.append(ch)
            i += 1
    s = "".join(out)
    if is_bool:
        return (True if s == "True" else False if s == "False" else s), True, False
    if is_null:
        return (None), False, True
    return s, False, False


def _read_until(s: str, start: int, stops: List[str]) -> Tuple[str, int]:
    """Read from start until an unescaped char in stops appears.

    Returns (substring_without_terminal, index_of_terminal)
    The index points to the stop character encountered (or len(s) if none).
    """
    i = start
    buf: List[str] = []
    while i < len(s):
        ch = s[i]
        if ch == ESC:
            if i + 1 < len(s):
                buf.append(s[i:i+2])
                i += 2
                continue
            else:
                buf.append(ch)
                i += 1
                continue
        if ch in stops:
            break
        buf.append(ch)
        i += 1
    return "".join(buf), i


def _split_records_sld(s: str) -> List[str]:
    # split by top-level ~ (outside arrays)
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == ESC and i + 1 < len(s):
            buf.append(s[i:i+2])
            i += 2
            continue
        if ch == ARR_OPEN:
            depth += 1
            buf.append(ch)
            i += 1
            continue
        if ch == ARR_CLOSE and depth > 0:
            depth -= 1
            buf.append(ch)
            i += 1
            continue
        if ch == REC_SEP_SLD and depth == 0:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        parts.append("".join(buf))
    return [p for p in parts if p != ""]


def _split_fields(record: str) -> List[str]:
    # split by ; outside arrays
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    i = 0
    while i < len(record):
        ch = record[i]
        if ch == ESC and i + 1 < len(record):
            buf.append(record[i:i+2])
            i += 2
            continue
        if ch == ARR_OPEN:
            depth += 1
            buf.append(ch)
            i += 1
            continue
        if ch == ARR_CLOSE and depth > 0:
            depth -= 1
            buf.append(ch)
            i += 1
            continue
        if ch == FIELD_SEP and depth == 0:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        parts.append("".join(buf))
    return [p for p in parts if p != ""]


def _parse_key_and_type(head: str) -> Tuple[str, Optional[str]]:
    # head is everything up to the value opener ('[' or '{')
    # Inline type attaches with a '!' not at position 0
    if "!" not in head:
        return head, None
    excl = head.rfind("!")
    if excl <= 0:
        # '!' at pos 0 means header key like '!v'
        return head, None
    type_candidate = head[excl + 1 :]
    if type_candidate in TYPE_CODES:
        return head[:excl], type_candidate
    return head, None


def _convert_typed(val_text: str, t: str) -> Any:
    if t == "n":
        return None
    if t == "s":
        v, _, _ = _unescape(val_text)
        return v
    if t == "b":
        v_raw, is_bool, _ = _unescape(val_text)
        if is_bool:
            return v_raw
        txt = str(v_raw).strip().lower()
        # numeric truthiness first
        try:
            return int(txt) != 0
        except Exception:
            pass
        return True if txt in ("1", "true", "t", "yes", "y") else False
    if t == "i":
        v, _, _ = _unescape(val_text)
        try:
            return int(str(v))
        except Exception:
            return v
    if t == "f":
        v, _, _ = _unescape(val_text)
        try:
            return float(str(v))
        except Exception:
            return v
    if t in ("d", "t", "ts"):
        # Keep as NFC-normalized string; parsing may be added later
        v, _, _ = _unescape(val_text)
        return unicodedata.normalize("NFC", str(v))
    # Fallback
    v, _, _ = _unescape(val_text)
    return v


def _parse_array(s: str, i: int, elem_type: Optional[str]) -> Tuple[List[Any], int]:
    # s[i] is at ARR_OPEN
    assert s[i] == ARR_OPEN
    i += 1
    items: List[Any] = []
    buf: List[str] = []
    depth = 1
    while i < len(s):
        ch = s[i]
        if ch == ESC and i + 1 < len(s):
            buf.append(s[i:i+2])
            i += 2
            continue
        if ch == ARR_OPEN:
            # nested array start; include in buf and track depth
            buf.append(ch)
            depth += 1
            i += 1
            continue
        if ch == ARR_CLOSE:
            depth -= 1
            if depth == 0:
                # finalize last element if any
                elem_text = "".join(buf)
                if elem_text != "":
                    # an element can be typed inline like !i[123] or untyped scalar
                    items.append(_parse_element_value(elem_text, elem_type))
                buf = []
                i += 1
                break
            else:
                buf.append(ch)
                i += 1
                continue
        if ch == REC_SEP_SLD and depth == 1:
            # element separator at top array level
            elem_text = "".join(buf)
            items.append(_parse_element_value(elem_text, elem_type))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    return items, i


def _parse_element_value(text: str, elem_type: Optional[str]) -> Any:
    # Allow inline typed element e.g., !i[123]
    if text.startswith("!"):
        # find !type before '['
        lb = text.find(PROP_MARK)
        if lb > 0:
            tcode = text[1:lb]
            raw = text[lb + 1 :]
            if tcode in TYPE_CODES:
                return _convert_typed(raw, tcode)
    # else use container type if provided
    if elem_type:
        return _convert_typed(text, elem_type)
    # untyped scalar
    v, is_bool, is_null = _unescape(text)
    if is_null:
        return None
    if is_bool:
        return v
    return v


def _parse_record(record: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for field in _split_fields(record):
        # locate first unescaped value opener '[' or '{'
        i = 0
        opener = None
        while i < len(field):
            ch = field[i]
            if ch == ESC and i + 1 < len(field):
                i += 2
                continue
            if ch in (PROP_MARK, ARR_OPEN):
                opener = ch
                break
            i += 1
        if opener is None:
            # key with empty value
            key_raw = field
            key, tcode = _parse_key_and_type(key_raw)
            out[key] = None
            continue
        head = field[:i]
        key, tcode = _parse_key_and_type(head)

        if opener == PROP_MARK:
            # scalar value up to field or record end (handled by parent split)
            value_text = field[i + 1 :]
            # Trim accidental trailing ']' (not a grammar token)
            if value_text.endswith(']') and not value_text.endswith('^]'):
                value_text = value_text[:-1]
            if tcode:
                # typed scalar
                if tcode == "n":
                    # Type code 'n' no longer used for null in v2.0 (use ^_ instead)
                    # Preserve for backward compatibility
                    out[key] = None
                else:
                    out[key] = _convert_typed(value_text, tcode)
            else:
                v, is_bool, is_null = _unescape(value_text)
                if is_null:
                    out[key] = None
                elif is_bool:
                    out[key] = v
                else:
                    out[key] = v
        else:
            # array container; element type from tcode if present
            arr_items, _ = _parse_array(field, i, tcode)
            out[key] = arr_items
    return out


def parse_sld(text: str) -> List[Dict[str, Any]]:
    # Normalize accidental newlines (e.g., CRLF in files saved on Windows)
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text = text.rstrip(REC_SEP_SLD)
    if not text:
        return []
    recs = _split_records_sld(text)
    return [_parse_record(r) for r in recs]


def parse_mld(text: str) -> List[Dict[str, Any]]:
    lines = [ln for ln in text.split(REC_SEP_MLD) if ln.strip()]
    return [_parse_record(ln) for ln in lines]


def detect_header(records: List[Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    if not records:
        return None, records
    first = records[0]
    if all(k.startswith("!") for k in first.keys()):
        return first, records[1:]
    return None, records


def to_canonical(obj: Any) -> Any:
    if isinstance(obj, dict):
        # sort keys; NFC normalize strings recursively
        return {k: to_canonical(v) for k, v in sorted(obj.items(), key=lambda kv: kv[0])}
    if isinstance(obj, list):
        return [to_canonical(x) for x in obj]
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    return obj


def main(argv: List[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(description="SLD/MLD validator")
    p.add_argument("file", nargs="?", help="Input file (.sld or .mld). If omitted, reads stdin")
    p.add_argument("--canon", action="store_true", help="Emit canonicalized JSON (sorted keys, NFC strings)")
    p.add_argument("--format", choices=["sld", "mld"], help="Force input format detection")
    args = p.parse_args(argv)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = f.read()
    else:
        data = sys.stdin.read()

    fmt = args.format
    if fmt is None:
        # naive detect: if contains '\n' treat as MLD
        fmt = "mld" if "\n" in data and not data.strip().endswith(REC_SEP_SLD) else "sld"

    try:
        records = parse_mld(data) if fmt == "mld" else parse_sld(data)
        header, body = detect_header(records)
        out = {"header": header, "records": body}
        if args.canon:
            out = to_canonical(out)
        # Ensure UTF-8 output on Windows
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except ParseError as e:
        sys.stderr.write(f"Parse error {e.code}: {e} at {e.pos}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
