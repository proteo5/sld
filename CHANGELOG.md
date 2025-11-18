# Changelog

All notable changes to the SLD/MLD format will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-01

### Breaking Changes

⚠️ **This version is NOT backward compatible with v1.0**

- **Changed field separator from `|` to `;`**
  - Rationale: The pipe character (`|`) requires escaping in Unix shells (bash, zsh) and causes conflicts in terminal usage
  - Semicolon (`;`) is statistically rarer in natural text and causes fewer shell conflicts
  - Migration: Replace all unescaped `|` with `;` and `^|` with `^;`

### Added

- **MLD (Multi Line Data) format introduced**
  - New variant using newline (`\n`) as record separator instead of tilde (`~`)
  - File extension: `.mld`
  - MIME type: `text/mld`
  - Optimized for:
    - Log files and streaming data
    - Unix tool processing (grep, awk, sed, head, tail)
    - Line-by-line processing with constant memory
    - Human debugging and inspection
  
- **Bidirectional conversion between SLD and MLD**
  - SLD → MLD: `tr '~' '\n' < file.sld > file.mld`
  - MLD → SLD: `tr '\n' '~' < file.mld > file.sld`
  - Lossless conversion in both directions

- **Comprehensive documentation**
  - SPECIFICATION_SLD.md - Complete SLD technical specification
  - SPECIFICATION_MLD.md - Complete MLD technical specification
  - QUICK_REFERENCE_SLD.md - SLD quick reference guide
  - QUICK_REFERENCE_MLD.md - MLD quick reference guide with Unix tools
  - SYNTAX_GUIDE_SLD.md - Detailed SLD syntax examples
  - SYNTAX_GUIDE_MLD.md - Detailed MLD syntax with streaming patterns
  - Spanish versions: REFERENCIA_RAPIDA_*.md, GUIA_SINTAXIS_*.md

- **Example files**
  - 7 SLD examples: simple, products, users, escaped, complex, logs, config
  - 7 MLD examples: same content in multi-line format
  - Comprehensive README with usage patterns and Unix tool examples

### Changed

- **Delimiter table updated**
  - Field separator: `|` (U+007C) → `;` (U+003B)
  - All escape sequences updated: `^|` → `^;`
  - Record separator: `~` (U+007E) - unchanged for SLD, `\n` for MLD
  - Property marker: `[` (U+005B) - unchanged
  - Array marker: `{` (U+007B) - unchanged
  - Escape character: `^` (U+005E) - unchanged

- **File extensions clarified**
  - `.sld` - Single Line Data (SLD format)
  - `.mld` - Multi Line Data (MLD format)

- **MIME types defined**
  - `application/sld+compact` - SLD format
  - `text/mld` - MLD format

### Deprecated

- **v1.0 format using `|` as field separator**
  - SPECIFICATION.md marked as deprecated
  - No migration path provided - clean break
  - Legacy implementations should upgrade to v1.1

### Security

- Shell safety improved by using semicolon instead of pipe
- Reduced risk of command injection in shell contexts
- Same escape mechanism security properties maintained

### Performance

- Token efficiency unchanged: 78% reduction vs JSON
- Byte efficiency unchanged for SLD
- MLD adds Unix tool compatibility with minimal overhead

## [1.0.0] - 2024-11-16

### Added

- Initial SLD format specification
- Field separator: `|` (U+007C)
- Record separator: `~` (U+007E)
- Property marker: `[` (U+005B)
- Array marker: `{` (U+007B)
- Escape character: `^` (U+005E)
- Boolean values: `^1` (true), `^0` (false)
- Single-line format optimized for token efficiency
- 78% token reduction compared to JSON
- Basic documentation and examples

### Notes

- Created as satirical response to format minimalism trends
- Functional but primarily educational/experimental

---

## Migration Notes

### Upgrading from v1.0 to v1.1

**Automatic conversion is NOT possible** due to ambiguity in escape sequences.

**Manual steps required:**

1. **Replace field separators:**
   - Find: `|` (unescaped pipes)
   - Replace: `;`

2. **Update escape sequences:**
   - Find: `^|` (escaped pipes)
   - Replace: `^;`

3. **Validate data:**
   - Parse with v1.1 decoder
   - Verify all records load correctly
   - Check for data integrity

4. **Choose format:**
   - Use SLD (`.sld`) for network transmission, compact storage
   - Use MLD (`.mld`) for logs, streaming, Unix tool processing

5. **Update implementations:**
   - Upgrade parsers to v1.1
   - Update field separator constant
   - Add MLD support if needed

### Format Selection Guide

**Use SLD when:**
- Sending data over network
- Minimizing token count for LLMs
- Storing in memory-constrained environments
- Single-record processing

**Use MLD when:**
- Writing log files
- Processing with grep/awk/sed
- Streaming large datasets
- Line-by-line processing needed
- Human debugging/inspection

Both formats are interconvertible without data loss.

---

## Comparison with Other Formats

### Token Efficiency (v1.1)

| Format | Tokens | Reduction vs JSON |
|--------|--------|-------------------|
| JSON (formatted) | 100 | 0% |
| JSON (minified) | 68 | 32% |
| CSV | 29 | 71% |
| **SLD/MLD** | **22** | **78%** |

### Use Case Comparison

| Feature | SLD | MLD | JSON | CSV |
|---------|-----|-----|------|-----|
| Token efficiency | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Human readability | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Unix tool support | ⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| Nested structures | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Streaming | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Network transmission | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

[1.1.0]: https://github.com/proteo5/sld/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/proteo5/sld/releases/tag/v1.0.0
braces[Open^{|Close^}~
```

---

### 4. Property Syntax Clarification

**Specification:** All object properties MUST use `property[value` syntax

**Previous (ambiguous):**
```
key1|value1|key2|value2  ← Could be table or object
```

**New (explicit):**
```
Table:  key1|key2~value1|value2     ← Headers then values
Object: key1[value1|key2[value2~    ← Properties with [
```

---

### 5. Last Property Indicator

**Rule:** Last property in an object MUST end with `~` instead of `|`

**Purpose:** Clear object termination without ambiguity

**Example:**
```
name[John|age[30|city[NYC~    ← ~ indicates end
```

---

## Escape Sequence Updates

### Added Escapes

| Sequence | Meaning | Example |
|----------|---------|---------|
| `^{` | Literal `{` | `text[Code^{block^}|` |

### Complete Escape List

| Sequence | Result | Context |
|----------|--------|---------|
| `^|` | Literal `|` | Data contains pipe |
| `^~` | Literal `~` | Data contains tilde |
| `^[` | Literal `[` | Data contains bracket |
| `^{` | Literal `{` | Data contains brace |
| `^^` | Literal `^` | Data contains caret |
| `^1` | Boolean true | Boolean value |
| `^0` | Boolean false | Boolean value |

---

## Grammar Updates

### Previous Grammar (Simplified)
```
record ::= field ("|" field)*
field  ::= key "|" value
```

### New Grammar (Complete)
```
sld_document  ::= table | object | array
table         ::= header_row ("~" data_row)*
object        ::= property ("|" property)* last_property
array         ::= key "{" object ("~" object)*
property      ::= key "[" value
last_property ::= key "[" value "~"
value         ::= boolean | escaped_string | ""
boolean       ::= "^0" | "^1"
```

---

## Token Efficiency Impact

### Before (Mixed Syntax)
```
products[id|1|name|Laptop|price|3999.90
```
**~18 tokens**

### After (Optimized by Format)

**Array Format:**
```
products{id[1|name[Laptop|price[3999.90~
```
**~15 tokens**

**Table Format:**
```
id|name|price~1|Laptop|3999.90
```
**~12 tokens**

**Improvement:** Up to 33% additional token savings by choosing optimal format!

---

## Migration Guide

### Boolean Values
```diff
- active[true|
+ active[^1|

- verified[false|
+ verified[^0|
```

### Arrays
```diff
- items[item1|item2|item3
+ items{id[1|name[item1~id[2|name[item2~id[3|name[item3

OR (if simple list):
+ item~item1~item2~item3
```

### Objects
```diff
- key1|value1|key2|value2
+ key1[value1|key2[value2~
```

### Tables (No Change if Already Using)
```
header1|header2|header3~value1|value2|value3~value4|value5|value6
```
✅ Already correct!

---

## Validation Rules

### Table Format
- [ ] First row contains headers (no `[` characters)
- [ ] All rows have equal field count
- [ ] No `[` or `{` in data (unless escaped)
- [ ] Each row ends with field value (no `~` in middle)

### Object Format
- [ ] All properties use `property[value` syntax
- [ ] Last property ends with `~`
- [ ] Each property has exactly one `[`
- [ ] Boolean values use `^0` or `^1`

### Array Format
- [ ] Starts with `arrayName{`
- [ ] Each object is valid (follows object rules)
- [ ] Objects separated by `~`
- [ ] No closing `}` needed (end of string terminates)

---

## Examples: Before & After

### Example 1: Product List

**Before (ambiguous):**
```
id|1|name|Laptop|price|3999.90~id|2|name|Mouse|price|149.90
```

**After (clear - Array):**
```
products{id[1|name[Laptop|price[3999.90~id[2|name[Mouse|price[149.90
```

**After (clear - Table):**
```
id|name|price~1|Laptop|3999.90~2|Mouse|149.90
```

---

### Example 2: User Profile

**Before:**
```
userId|12345|username|john|verified|true
```

**After (Object):**
```
userId[12345|username[john|verified[^1~
```

---

### Example 3: Mixed Boolean

**Before:**
```
active|true|premium|false|verified|true
```

**After:**
```
active[^1|premium[^0|verified[^1~
```

---

## Breaking Changes

⚠️ **Warning:** These changes are NOT backward compatible with v1.0

### What Breaks:
1. Boolean values `true`/`false` → Must change to `^1`/`^0`
2. Object syntax without `[` → Must add `property[value` format
3. Arrays without `{` → Must use `arrayName{` syntax

### Migration Required:
- Update all parsers to recognize three formats
- Convert boolean representations
- Add proper delimiters for objects/arrays

---

## Implementation Checklist

For language implementations:

- [ ] Support all three formats (Table, Object, Array)
- [ ] Parse `^0`/`^1` as booleans
- [ ] Recognize `{` as array delimiter
- [ ] Enforce `property[value` syntax for objects
- [ ] Validate last property ends with `~`
- [ ] Escape `{` character when needed
- [ ] Provide format detection/validation

---

## Version History

**v1.0** (2025-11-16): Initial specification  
**v1.1** (2025-11-16): Three-format clarification, boolean update

---

## References

- [SPECIFICATION.md](SPECIFICATION.md) - Complete technical spec
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Format quick guide
- [SYNTAX_GUIDE.md](SYNTAX_GUIDE.md) - Detailed examples

---

**Status:** ✅ Specification finalized and documented
