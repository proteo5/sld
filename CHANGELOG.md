# SLD Format Specification Changes - v1.1

## Summary of Updates

This document outlines the key specification changes made to the SLD format to clarify and formalize the three distinct data representation methods.

## Major Changes

### 1. Boolean Representation
**Previous:** `true` / `false`  
**New:** `^1` / `^0`

**Rationale:** 
- Consistent with escape character usage
- Shorter representation (2 chars vs 4-5 chars)
- Clear distinction from string values
- Easier to parse programmatically

**Examples:**
```
Before: active[true|verified[false|
After:  active[^1|verified[^0|
```

---

### 2. Three Distinct Formats Formalized

#### A. Table Format
**Use case:** CSV-like data, uniform records

**Structure:**
- First row = headers
- Subsequent rows = data values
- Fields separated by `|`
- Rows separated by `~`

**Example:**
```
id|name|price|stock~1|Laptop|3999.90|25~2|Mouse|149.90|150
```

**Benefits:**
- Most compact for uniform data
- Natural CSV migration path
- Headers amortized across rows

---

#### B. Object Format
**Use case:** Single entities, configuration, key-value pairs

**Structure:**
- Properties: `property[value|`
- Last property: `property[value~`
- Always ends with `~`

**Example:**
```
userId[12345|username[john_doe|email[john@example.com|verified[^1~
```

**Benefits:**
- Self-documenting properties
- Clear property-value relationship
- Easy to read and parse

---

#### C. Array Format
**Use case:** Named collections, lists of objects

**Structure:**
- Array start: `arrayName{`
- Objects separated by `~`
- Each object follows object format rules

**Example:**
```
users{id[1|name[John|active[^1~id[2|name[Jane|active[^0
```

**Benefits:**
- Explicit array naming
- Clear collection boundaries
- Supports heterogeneous objects

---

### 3. New Delimiter: `{` (Array Start)

**Added:** U+007B `{` as array start marker

**Purpose:** Distinguish between object properties and array collections

**Escape:** `^{` for literal brace character

**Example:**
```
teams{name[Engineering|size[15~name[Design|size[8
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
