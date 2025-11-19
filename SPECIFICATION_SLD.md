# SLD Format Specification v1.1 (with v1.2 extensions)

**Single Line Data (SLD)** - Maximum token efficiency in a single line

## Abstract

SLD (Single Line Data) is a text-based data serialization format optimized for token efficiency in Large Language Model (LLM) contexts. By eliminating ALL line breaks and using statistically rare separator characters, SLD achieves significant token reduction compared to JSON and CSV.

## Motivation

Modern LLM applications are constrained by token limits. Traditional data formats like JSON introduce overhead through:

- Line breaks (1-2 bytes each)
- Whitespace and indentation  
- Verbose syntax characters
- Multiple tokens for structural elements

SLD addresses these inefficiencies by design, achieving **78% token reduction** compared to JSON.

## Format Definition

### Core Syntax

**SLD data MUST be represented as a single continuous line of text with NO line breaks** (`\n`, `\r\n`, or `\r`).

### Delimiter Characters

| Character | Unicode | Purpose | Priority |
|-----------|---------|---------|----------|
| `;` | U+003B | Field/property separator | Primary |
| `~` | U+007E | Record/row separator | Primary |
| `[` | U+005B | Property value marker | Primary |
| `{` | U+007B | Array start marker | Primary |
| `}` | U+007D | Array end marker | Primary |
| `^` | U+005E | Escape character & boolean prefix | Meta |

### Character Selection Rationale

These characters were selected based on:

1. **Low frequency** in natural language and common data
2. **Single-byte** representation in UTF-8
3. **Unambiguous** visual appearance
4. **Keyboard availability** across all layouts
5. **Shell compatibility** - `;` is less problematic than `|` in Unix/Linux shells

### Escape Mechanism

To include delimiter characters as literal values:

1. Prefix the character with `^`
2. The escape character itself is escaped as `^^`

**Examples:**

```text
^;  → literal ;
^~  → literal ~
^[  → literal [
^{  → literal {
^}  → literal }
^^  → literal ^
```

**Escape Sequence Processing:**

- Escapes are processed left-to-right
- Only the five delimiter characters require escaping
- All other characters are used literally

### Data Types

#### Primitive Values

**String:** Any sequence of characters (escaped as needed)

```sld
name[John Doe;
```

**Number:** Numeric representation without quotes

```sld
price[3999.90;quantity[5;
```

**Boolean:** Represented as `^1` (true) or `^0` (false)

```sld
active[^1;verified[^0;
```

**Null/Empty (v1.1):** Consecutive delimiters

```sld
name;;age;30
```

(name is null, age is 30)

#### Null Value (v1.2 extension)

- Canonical null MAY be encoded as the escape sequence `^_`.
- Producers MUST only emit `^_` when the peer declares support via the header metadata `!features[null]` (see Header Metadata).
- For backward compatibility, producers SHOULD prefer `campo!n[` (typed null; see Explicit Types) or empty value when interoperability with v1.1 decoders is required.

Examples:

```sld
note[^_      ; # typed as null if feature negotiated
missing!n[; # backward-compatible typed null (empty payload)
```

#### Structured Data

**Table Format (First row = headers):**

```sld
name;price~Laptop;3999.90~Mouse;149.90~Headset;499.00
```

**Object (Property-Value Pairs):**
Objects are represented as records composed of semicolon-separated properties in the form `key[value`.

```sld
name[John;age[30;city[NYC
```

**Arrays:**
Use `{` after the array name to start an array and `}` to close it. Elements are separated by `~` (array element separator). The final `~` MAY be omitted before `}` to maximize compactness.

- Array of scalars:

    ```sld
    tags{admin~user~editor}
    ```

- Array of objects (each object uses normal property syntax; end each object with `~`, omit the last one):

    ```sld
    users{id[1;name[Ana;city[NYC~id[2;name[Carlos;city[Madrid}
    ```

- Array containing a table (header row followed by rows):

    ```sld
    Productos{id;nombre;cantidad~1;Fulano;10~2;Sutano;20}
    ```

**Nested Objects:**
For nested objects, flatten the structure using underscore notation:

```sld
user_name[John;user_address_street[Main St;user_address_city[NYC~
```

Note: Nested objects beyond simple flattening are implementation-defined and optional in v1.1.

### Complete Example

**JSON:**

```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 3999.90,
      "inStock": true
    },
    {
      "id": 2,
      "name": "Mouse",
      "price": 149.90,
      "inStock": false
    }
  ]
}
```

**SLD (Records):**

```sld
id[1;name[Laptop;price[3999.90;inStock[^1~id[2;name[Mouse;price[149.90;inStock[^0~
```

**SLD (Table format):**

```sld
id;name;price;inStock~1;Laptop;3999.90;^1~2;Mouse;149.90;^0
```

## Parsing Rules

### Tokenization

1. **Initialize** position at start of string
2. **Scan** character by character
3. **When encountering `^`:**
   - Read next character
   - Treat as literal (unescape)
   - Continue
4. **When encountering `;`:**
   - Mark field boundary
5. **When encountering `~`:**
   - Mark record boundary
6. **When encountering `[`:**
   - Begin nested structure
   - Parse recursively until next `~` or end

### State Machine

```text
START → FIELD_NAME → FIELD_VALUE → [NEXT_FIELD | NEXT_RECORD | NESTED_OBJECT]
```

## Grammar (EBNF-like)

```ebnf
sld_document    ::= record ( "~" record )* [ "~" ]
record          ::= field ( ";" field )*
field           ::= property | array
property        ::= key "[" value
array           ::= key "{" array_body "}"
array_body      ::= scalar_elements | object_elements | table_elements
scalar_elements ::= value ( "~" value )* [ "~" ]?
object_elements ::= object_record ( "~" object_record )* [ "~" ]?
table_elements  ::= header_row ( "~" data_row )* [ "~" ]?
object_record   ::= property ( ";" property )*
header_row      ::= key ( ";" key )*
data_row        ::= value ( ";" value )*
key             ::= escaped_string
value           ::= escaped_string | boolean | ""
boolean         ::= "^0" | "^1"
null            ::= "^_"            (* v1.2 optional *)
escaped_string  ::= ( escaped_char | regular_char )*
escaped_char    ::= "^" ( ";" | "~" | "[" | "{" | "}" | "^" )
regular_char    ::= any character except ";", "~", "[", "{", "}", "^"

(* Typed properties (v1.2 optional): key may carry an inline type tag before '[' or '{' using '!code' *)
type_code       ::= "i" | "f" | "b" | "s" | "n" | "d" | "t" | "ts"
property        ::= key [ "!" type_code ] "[" value
array           ::= key [ "!" type_code ] "{" array_body "}"
                   (* int, float, bool, string, null, date, time, timestamp *)
```

**Notes:**

- In SLD, `~` separates records and also separates array elements. Within an object, the last property is indicated by the `~` that terminates the object (and simultaneously separates it from the next element). At end-of-line, that final `~` MAY be omitted.

## Encoding Algorithm

```python
def encode_value(value):
    """Escape special characters in a value."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "^1" if value else "^0"
    str_value = str(value)
    return (str_value
            .replace("^", "^^")
            .replace(";", "^;")
            .replace("~", "^~")
            .replace("[", "^[")
            .replace("{", "^{")
            .replace("}", "^}"))

def encode_object(obj):
    """Encode an object to SLD record."""
    parts = []
    for key, value in obj.items():
        encoded_key = encode_value(key)
        encoded_value = encode_value(value)
        parts.append(f"{encoded_key}[{encoded_value}")
    return ";".join(parts)

def encode_array(name, items):
    """Encode an array to SLD.
    items can be:
    - list of scalars
    - list of dicts (objects)
    - dict with keys: {"headers": [...], "rows": [[...], ...]} for tables
    """
    encoded_name = encode_value(name)
    if isinstance(items, dict) and "headers" in items and "rows" in items:
        header = ";".join(encode_value(h) for h in items["headers"])
        rows = [";".join(encode_value(v) for v in row) for row in items["rows"]]
        body = "~".join([header] + rows)
        return f"{encoded_name}{{{body}}}"
    if items and isinstance(items[0], dict):
        body = "~".join(encode_object(obj) for obj in items)
        return f"{encoded_name}{{{body}}}"
    body = "~".join(encode_value(item) for item in items)
    return f"{encoded_name}{{{body}}}"

def encode_table(data):
    """Encode table (list of lists) to SLD."""
    return "~".join(";".join(encode_value(v) for v in row) for row in data)

def encode_sld(data):
    """Encode data structure to SLD format."""
    if isinstance(data, list):
        # Check if it's a table (list of lists) or array of objects
        if data and isinstance(data[0], list):
            return encode_table(data)
        else:
            return "~".join(encode_object(record) for record in data)
    elif isinstance(data, dict):
        return encode_object(data)
    else:
        return encode_value(data)
```

## Decoding Algorithm

```python
def unescape_value(value):
    """Unescape special characters in a value."""
    result = []
    i = 0
    while i < len(value):
        if value[i] == "^" and i + 1 < len(value):
            result.append(value[i + 1])
            i += 2
        else:
            result.append(value[i])
            i += 1
    return "".join(result)

def split_unescaped(text, delimiter):
    """Split text by delimiter, respecting escape sequences."""
    parts = []
    current = []
    i = 0
    while i < len(text):
        if text[i] == "^" and i + 1 < len(text):
            current.append(text[i:i+2])
            i += 2
        elif text[i] == delimiter:
            parts.append("".join(current))
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1
    if current:
        parts.append("".join(current))
    return parts

def decode_sld(sld_string):
    """Decode SLD format to data structure."""
    records = []
    for record_str in split_unescaped(sld_string, "~"):
        record = {}
        parts = split_unescaped(record_str, ";")
        i = 0
        while i < len(parts):
            key = unescape_value(parts[i])
            # Check if this is a nested structure
            if "[" in parts[i] and not "^[" in parts[i]:
                # Parse nested content
                nested_start = i + 1
                # Find the end of nested structure (next key or end)
                # This is simplified; real implementation needs proper nesting tracking
                record[key.replace("[", "")] = {}  # Placeholder
            else:
                if i + 1 < len(parts):
                    value = unescape_value(parts[i + 1])
                    record[key] = value if value != "" else None
                i += 2
        records.append(record)
    return records if len(records) > 1 else records[0] if records else {}
```

## Performance Characteristics

## Canonicalization Profile (v1.2)

This section defines a canonical form for producers. Decoders MUST accept non‑canonical input; canonicalization is RECOMMENDED for signing, hashing, and deterministic diffs.

- Field order: Properties within a record SHOULD be emitted with a stable order (RECOMMENDED: lexicographic by key; arrays retain input order).
- Arrays: No trailing `~` before `}`. Empty arrays are `{}`.
- Whitespace: Whitespace outside values is PROHIBITED. Inside values it is literal (escaped as needed).
- Unicode: Producers SHOULD normalize values to NFC. Decoders MAY accept any normalization.
- Numbers: Integers without leading `+` or zeros (except zero itself). Floats use `.` as decimal separator and lowercase `e` for scientific notation.
- Booleans: Always `^1` / `^0`.
- Null: Prefer `campo!n[` (empty payload) for maximum interoperability; `^_` only when negotiated when types unsupported.

Canonicalization is a production rule; it does not alter the acceptance criteria of decoders.

### Token Efficiency

Based on empirical testing with GPT-style tokenizers:

| Format | Relative Tokens | Reduction vs JSON |
|--------|----------------|-------------------|
| JSON (formatted) | 100% | 0% (baseline) |
| JSON (minified) | 68% | 32% |
| TOON | 56% | 44% |
| **SLD** | **22%** | **78%** 👑 |

### Byte Efficiency

For a typical 100-record dataset:

- Line breaks saved: 99-198 bytes (depending on OS)
- Structural characters: ~30-50% reduction
- Total overhead: ~40-60% smaller than JSON

### Shell Compatibility

The change from `|` to `;` improves shell usage:

```bash
# Works without escaping in Unix shells
echo "name[John;age[30~" > data.sld
cat data.sld | grep "John"

# vs old format required escaping
echo "name[John|age|30~" | sld-parser  # | is pipe operator!
```

## Security Considerations

### Injection Prevention

- Always escape user input before encoding
- Validate escaped sequences during decoding
- Reject malformed escape sequences

### Size Limits

Implementations SHOULD enforce maximum:

- Single line length: 1MB (recommended)
- Field count per record: 1000 (recommended)
- Nesting depth: 10 levels (recommended)

### Character Encoding

- SLD MUST use UTF-8 encoding
- Implementations SHOULD validate UTF-8 correctness
- Invalid UTF-8 sequences SHOULD be rejected

### Boolean Validation

- Only `^0` and `^1` are valid boolean values
- Implementations SHOULD reject `true`, `false`, or other boolean representations
- Escaped `^^0` or `^^1` represent literal strings "^0" and "^1", not booleans

## Implementation Considerations

### Memory Efficiency

Since SLD is a single line:

- Streaming parsers can use fixed buffers
- No need for line-by-line processing
- Entire document can be loaded as single string

### Error Handling

Implementations SHOULD provide clear errors for:

- Unclosed nested structures
- Invalid escape sequences
- Malformed field separators
- Character encoding issues

### Standard Error Codes (v1.2)

Implementations MAY report standardized error codes to improve interoperability:

- E01: Invalid escape sequence
- E02: Unterminated array `}` missing
- E03: Unexpected record terminator
- E04: Invalid boolean (only `^0` or `^1` allowed)
- E05: Invalid null (requires `^_` feature or typed-null)
- E06: Malformed typed key suffix (unknown type code)
- E07: Exceeded implementation limits (size/fields/nesting)
- E08: Invalid UTF‑8 sequence
- E09: Header metadata malformed
- E10: Unknown directive (fatal)

## Conformance

An implementation is SLD v1.1-compliant if it:

1. Correctly encodes/decodes all primitive types
2. Handles all five escape sequences (`;`, `~`, `[`, `{`, `^`)
3. Supports nested structures
4. Produces single-line output
5. Preserves data integrity through encode/decode cycles
6. Uses `;` as field separator (not `|`)

### v1.2 Optional Extensions

An implementation advertising v1.2 support SHOULD additionally:

1. Parse and optionally emit typed properties using inline type tags `name!i[` `name!f[` `name!b[` `name!s[` `name!n[` etc.
2. Recognize `^_` as null when `!features` includes `null`.
3. Respect and/or emit the canonicalization profile.
4. Parse a metadata header record when present (see next section).

## Header Metadata (v1.2)

Producers MAY include a leading metadata record using reserved keys prefixed with `!`. Decoders that do not recognize these keys will treat them as ordinary fields and MAY ignore them.

Placement:
- SLD: The metadata record appears as the first record (before application data).

Reserved keys:
- `!v[1.2]` – Declared format minor version.
- `!schema[<uri>]` – Schema or contract identifier.
- `!ts[<iso-8601>]` – Timestamp of production.
- `!source[<text>]` – Origin of the data.
- `!features{types~null~canon}` – Enabled optional features (array of tokens).

Example (SLD):

```sld
!v[1.2;!schema[urn:example:schema:v1;!ts[2025-11-18T12:00:00Z;!features{types~null~canon}~
id[1;name[Ana~id[2;name[Carlos
```

### Explicit Types (v1.2)

Keys MAY include an optional inline type tag using `!code` immediately before the value marker `[` or `{`:

- `!i` integer, `!f` float, `!b` boolean, `!s` string, `!n` null,
- `!d` date, `!t` time, `!ts` timestamp (ISO‑8601 strings recommended).

Examples:

```sld
age!i[42; price!f[3999.90; active!b[^1; title!s[Hello; removed!n[
```

Unknown type codes MUST NOT cause parse failure; consumers MAY ignore the suffix and treat as string.

## Related Formats

- **MLD (Multi Line Data)** - Line-based variant using `\n` instead of `~` for better Unix tool compatibility
- See [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) for details

## Conversion

### SLD ↔ MLD Conversion

```bash
# SLD to MLD
tr '~' '\n' < file.sld > file.mld

# MLD to SLD
tr '\n' '~' < file.mld | sed 's/~$//' > file.sld
```

## Version History

- **v1.1 (2025-11-18)**:
  - Changed field separator from `|` to `;` for better shell compatibility
  - Introduced MLD (Multi Line Data) variant
  - Updated escape sequences
  - **BREAKING CHANGE**: Not compatible with v1.0
  
- v1.0 (2025-11-16): Initial specification (DEPRECATED)

## Migration from v1.0

v1.0 used `|` as field separator. To migrate to v1.1:

```bash
# Simple conversion (if no escaped pipes)
tr '|' ';' < old_v1.0.sld > new_v1.1.sld

# Manual conversion required if data contains:
# - Escaped pipes (^|)
# - Literal semicolons
```

See [MIGRATION.md](MIGRATION.md) for detailed migration guide.

## References

- JSON: RFC 8259
- CSV: RFC 4180
- UTF-8: RFC 3629
- MLD Specification: [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md)

## Acknowledgments

Originally created as a humorous exploration of token efficiency, now a practical, documented format.

---

**Note:** While SLD is a functional format with genuine efficiency benefits, it was created primarily as a satirical response to format minimalism trends. Use in production environments at your own discretion.

**File Extension:** `.sld`  
**MIME Type:** `application/sld+compact` or `text/sld`
