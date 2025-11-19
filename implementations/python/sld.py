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
SLD/MLD (Single/Multi Line Data) Format - Python Implementation v2.0
A token-efficient data serialization format

Breaking changes from v1.0:
- Field separator changed from | to ; (semicolon)
- Array marker changed to { (curly brace)
- Added MLD format support (records separated by newlines)
"""

from typing import Any, Dict, List, Union


# Constants
FIELD_SEPARATOR = ";"
RECORD_SEPARATOR_SLD = "~"
RECORD_SEPARATOR_MLD = "\n"
PROPERTY_MARKER = "["
ARRAY_MARKER = "{"
ESCAPE_CHAR = "^"


def escape_value(text: str) -> str:
    """Escape special SLD/MLD characters in a string.

    Args:
        text: The text to escape

    Returns:
        Escaped text safe for SLD/MLD format
    """
    if text is None:
        return ""

    str_text = str(text)
    return (str_text
            .replace(ESCAPE_CHAR, ESCAPE_CHAR + ESCAPE_CHAR)
            .replace(FIELD_SEPARATOR, ESCAPE_CHAR + FIELD_SEPARATOR)
            .replace(RECORD_SEPARATOR_SLD, ESCAPE_CHAR + RECORD_SEPARATOR_SLD)
            .replace(PROPERTY_MARKER, ESCAPE_CHAR + PROPERTY_MARKER)
            .replace(ARRAY_MARKER, ESCAPE_CHAR + ARRAY_MARKER))


def unescape_value(text: str) -> str:
    """Unescape SLD/MLD escape sequences.

    Args:
        text: The escaped text

    Returns:
        Unescaped original text
    """
    result = []
    i = 0
    while i < len(text):
        if text[i] == ESCAPE_CHAR and i + 1 < len(text):
            next_char = text[i + 1]
            if next_char == '1':
                result.append(True)
                i += 2
            elif next_char == '0':
                result.append(False)
                i += 2
            else:
                result.append(next_char)
                i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(str(c) for c in result)


def split_unescaped(text: str, delimiter: str) -> List[str]:
    """Split text by delimiter, respecting escape sequences.

    Args:
        text: The text to split
        delimiter: The delimiter character

    Returns:
        List of split parts
    """
    parts = []
    current = []
    i = 0

    while i < len(text):
        if text[i] == ESCAPE_CHAR and i + 1 < len(text):
            current.append(text[i:i+2])
            i += 2
        elif text[i] == delimiter:
            parts.append("".join(current))
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1

    if current or text.endswith(delimiter):
        parts.append("".join(current))

    return parts


def encode_sld(data: Union[List[Dict], Dict]) -> str:
    """Encode data to SLD format.

    Args:
        data: Data to encode (dict or list of dicts)

    Returns:
        SLD-formatted string (single line with ~ separators)

    Examples:
        >>> encode_sld([{"name": "Alice", "age": 30}])
        'name[Alice;age[30~'

        >>> encode_sld({"name": "Bob", "active": True})
        'name[Bob;active[^1'
    """
    if isinstance(data, list):
        records = [_encode_record(record) for record in data]
        return RECORD_SEPARATOR_SLD.join(records) + RECORD_SEPARATOR_SLD
    elif isinstance(data, dict):
        return _encode_record(data)
    else:
        return escape_value(str(data))


def encode_mld(data: Union[List[Dict], Dict]) -> str:
    """Encode data to MLD format.

    Args:
        data: Data to encode (dict or list of dicts)

    Returns:
        MLD-formatted string (one record per line)

    Examples:
        >>> encode_mld([{"name": "Alice"}, {"name": "Bob"}])
        'name[Alice\\nname[Bob'
    """
    if isinstance(data, list):
        records = [_encode_record(record) for record in data]
        return RECORD_SEPARATOR_MLD.join(records)
    elif isinstance(data, dict):
        return _encode_record(data)
    else:
        return escape_value(str(data))


def _encode_record(record: Dict[str, Any]) -> str:
    """Encode a single record (dictionary) to SLD/MLD format.

    Args:
        record: Dictionary to encode

    Returns:
        Encoded string for the record
    """
    parts = []

    for key, value in record.items():
        escaped_key = escape_value(str(key))

        if isinstance(value, dict):
            # Nested object - not fully implemented yet
            nested = _encode_record(value)
            parts.append(f"{escaped_key}{PROPERTY_MARKER}{nested}")
        elif isinstance(value, list):
            # Array using { marker
            nested_items = [escape_value(str(item)) for item in value]
            parts.append(f"{escaped_key}{ARRAY_MARKER}{','.join(nested_items)}")
        elif isinstance(value, bool):
            # Boolean as ^1 or ^0
            bool_val = "^1" if value else "^0"
            parts.append(f"{escaped_key}{PROPERTY_MARKER}{bool_val}")
        elif value is None:
            # Null value as ^_
            parts.append(f"{escaped_key}{PROPERTY_MARKER}^_")
        else:
            # Regular value
            escaped_value = escape_value(str(value))
            parts.append(f"{escaped_key}{PROPERTY_MARKER}{escaped_value}")

    return FIELD_SEPARATOR.join(parts)


def decode_sld(sld_string: str) -> Union[List[Dict], Dict]:
    """Decode SLD format string to Python data structures.

    Args:
        sld_string: SLD-formatted string

    Returns:
        Decoded data (dict or list of dicts)

    Examples:
        >>> decode_sld('name[Alice;age[30~')
        [{'name': 'Alice', 'age': '30'}]

        >>> decode_sld('name[Bob;active[^1')
        {'name': 'Bob', 'active': True}
    """
    if not sld_string:
        return {}

    # Remove trailing ~ if present
    sld_string = sld_string.rstrip(RECORD_SEPARATOR_SLD)

    records = []

    for record_str in split_unescaped(sld_string, RECORD_SEPARATOR_SLD):
        if not record_str:
            continue
        records.append(_decode_record(record_str))

    return records if len(records) > 1 else records[0] if records else {}


def decode_mld(mld_string: str) -> Union[List[Dict], Dict]:
    """Decode MLD format string to Python data structures.

    Args:
        mld_string: MLD-formatted string (one record per line)

    Returns:
        Decoded data (dict or list of dicts)

    Examples:
        >>> decode_mld('name[Alice\\nname[Bob')
        [{'name': 'Alice'}, {'name': 'Bob'}]
    """
    if not mld_string:
        return {}

    records = []

    for line in mld_string.split(RECORD_SEPARATOR_MLD):
        if not line.strip():
            continue
        records.append(_decode_record(line))

    return records if len(records) > 1 else records[0] if records else {}


def _decode_record(record_str: str) -> Dict[str, Any]:
    """Decode a single record string.

    Args:
        record_str: Single record string

    Returns:
        Decoded dictionary
    """
    record = {}
    fields = split_unescaped(record_str, FIELD_SEPARATOR)

    for field in fields:
        if not field:
            continue

        # Check for property marker
        if PROPERTY_MARKER in field and not (ESCAPE_CHAR + PROPERTY_MARKER) in field:
            parts = field.split(PROPERTY_MARKER, 1)
            key = unescape_value(parts[0])
            value = unescape_value(parts[1]) if len(parts) > 1 else ""

            # Handle null (^_)
            if value == "^_":
                value = None
            # Handle booleans
            elif value == "True":
                value = True
            elif value == "False":
                value = False

            record[key] = value
        # Check for array marker
        elif ARRAY_MARKER in field and not (ESCAPE_CHAR + ARRAY_MARKER) in field:
            parts = field.split(ARRAY_MARKER, 1)
            key = unescape_value(parts[0])
            if len(parts) > 1:
                items = [unescape_value(item) for item in parts[1].split(',')]
                record[key] = items
            else:
                record[key] = []

    return record


def sld_to_mld(sld_string: str) -> str:
    """Convert SLD format to MLD format.

    Args:
        sld_string: SLD-formatted string

    Returns:
        MLD-formatted string
    """
    return sld_string.replace(RECORD_SEPARATOR_SLD, RECORD_SEPARATOR_MLD).rstrip(RECORD_SEPARATOR_MLD)


def mld_to_sld(mld_string: str) -> str:
    """Convert MLD format to SLD format.

    Args:
        mld_string: MLD-formatted string

    Returns:
        SLD-formatted string
    """
    return mld_string.replace(RECORD_SEPARATOR_MLD, RECORD_SEPARATOR_SLD) + RECORD_SEPARATOR_SLD


if __name__ == "__main__":
    # Example usage
    print("=== SLD/MLD Python Implementation v2.0 ===\n")

    # Example 1: Simple records with SLD
    print("Example 1: Simple user data (SLD)")
    data1 = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"}
    ]
    sld1 = encode_sld(data1)
    print(f"Encoded SLD: {sld1}")
    print(f"Decoded: {decode_sld(sld1)}\n")

    # Example 2: Same data with MLD
    print("Example 2: Same data (MLD)")
    mld1 = encode_mld(data1)
    print(f"Encoded MLD:\n{mld1}")
    print(f"Decoded: {decode_mld(mld1)}\n")

    # Example 3: Arrays
    print("Example 3: Products with tags (arrays)")
    data3 = [
        {"sku": "LAP001", "name": "UltraBook Pro", "tags": ["business", "ultrabook"]},
        {"sku": "MOU001", "name": "Wireless Mouse", "tags": ["wireless", "ergonomic"]}
    ]
    sld3 = encode_sld(data3)
    print(f"Encoded SLD: {sld3}")
    print(f"Decoded: {decode_sld(sld3)}\n")

    # Example 4: Booleans
    print("Example 4: Boolean values")
    data4 = {"name": "Alice", "verified": True, "active": False}
    sld4 = encode_sld(data4)
    print(f"Encoded SLD: {sld4}")
    print(f"Decoded: {decode_sld(sld4)}\n")

    # Example 5: Conversion SLD ↔ MLD
    print("Example 5: Format conversion")
    sld5 = "name[Alice;age[30~name[Bob;age[25~"
    mld5 = sld_to_mld(sld5)
    print(f"SLD: {sld5}")
    print(f"MLD:\n{mld5}")
    print(f"Back to SLD: {mld_to_sld(mld5)}\n")

    # Example 6: Escaped characters
    print("Example 6: Escaped characters")
    data6 = {"note": "Price: $5;99", "path": "C:\\Users"}
    sld6 = encode_sld(data6)
    print(f"Encoded: {sld6}")
    print(f"Decoded: {decode_sld(sld6)}")
