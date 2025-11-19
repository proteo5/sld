# SLD Quick Reference v2.0

## Single Line Data — Fast reference for developers

---

## Delimiters (v2.0)

| Character | Purpose | Example |
|-----------|---------|---------|
| `;` | Field separator | `name[Alice;age[30` |
| `~` | Record separator | `record1~record2` |
| `[` | Property marker | `name[value` |
| `{` | Array marker | `tags{red~blue}` |
| `^` | Escape character | `text[Hello^; World` |

**⚠️ Breaking Change in v2.0:** Field separator changed from `|` (v1.0) to `;` for better shell compatibility.

---

## Escape Sequences

| Sequence | Result |
|----------|--------|
| `^;` | Literal `;` |
| `^~` | Literal `~` |
| `^[` | Literal `[` |
| `^{` | Literal `{` |
| `^}` | Literal `}` |
| `^^` | Literal `^` |

**Example:**

```sld
desc[Price: $100^; includes tax
```

---

## Data Types

### String

```sld
name[Alice
city[New York
```

### Number

```sld
age[30
price[99.99
scientific[6.022e23
```

### Boolean

```sld
active[^1        # true
verified[^0      # false
```

### Null

```sld
middleName[;age[30    # middleName is null
```

### Array

```sld
tags{red~green~blue}
scores{85~92~78}
```


## v2.0 Optional Features (inline types and typed null)

These features are additive and negotiated via a metadata header (`!features{types}`); decoders without support may ignore type hints.

### Inline Type Tags

- Place `!code` immediately before `[` or `{`.
- Codes: `!i` int, `!f` float, `!b` bool, `!s` string, `!n` null, `!d` date, `!t` time, `!ts` timestamp.

Examples:

```sld
age!i[42; price!f[399.90; active!b[^1; title!s[Hello~
ids!i{1~2~3}
created!ts[2025-11-18T12:00:00Z~
removed!n[    # typed null (empty payload)
```

### Header Metadata (first record)

```sld
!v[1.2;!features{types~canon}~
id!i[1;name!s[Ana~
## Basic Examples

### Simple Object

```sld
name[Alice;age[30;city[NYC~
```

### Multiple Records

```sld
id[1;name[Alice~id[2;name[Bob~id[3;name[Charlie~
```

### Object with Array

```sld
user[alice;tags{admin~user};score[95~
```

### Escaped Content

```sld
note[Use semicolons^; not commas;date[2024-01-15~
```

---

## Common Patterns

### User Record

```sld
id[42;username[alice;email[alice@example.com;verified[^1;role[admin~
```

### Product Catalog

```sld
sku[LAP001;name[Laptop;price[999.99;stock[^1;tags{electronics~computers}~
```

### Transaction Log

```sld
tx[1234;amount[150.50;currency[USD;status[completed;timestamp[2024-12-01T10:30:00Z~
```

### Configuration

```sld
host[localhost;port[8080;ssl[^1;timeout[30;retries[3~
```

---

## Encoding Cheatsheet

**Python:**

```python
def escape(s):
    return (s.replace("^", "^^")
             .replace(";", "^;")
             .replace("~", "^~")
             .replace("[", "^[")
             .replace("{", "^{")
             .replace("}", "^}"))

def encode_object(obj):
    return ";".join(f"{escape(k)}[{escape(str(v))}" for k, v in obj.items())
```

**JavaScript:**

```javascript
const escape = s => s
    .replace(/\^/g, '^^')
    .replace(/;/g, '^;')
    .replace(/~/g, '^~')
    .replace(/\[/g, '^['])
    .replace(/\{/g, '^{')
    .replace(/\}/g, '^}');

const encodeObject = obj => Object
    .entries(obj)
    .map(([k, v]) => `${escape(k)}[${escape(String(v))}`)
    .join(';');
```

---

## Decoding Cheatsheet

**Python:**

```python
def unescape(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '^' and i + 1 < len(s):
            result.append(s[i + 1])
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

def decode(sld):
    records = []
    for record_str in sld.split('~'):
        props = record_str.split(';')
        obj = {}
        for prop in props:
            if '[' in prop:
                key, value = prop.split('[', 1)
                obj[unescape(key)] = unescape(value)
        records.append(obj)
    return records
```

---

## Conversion (SLD ↔ MLD)

**SLD to MLD:**

```bash
tr '~' '\n' < data.sld > data.mld
```

**MLD to SLD:**

```bash
tr '\n' '~' < data.mld > data.sld
```

---

## Common Mistakes

### ❌ Wrong: Using `|` (v1.0 delimiter)

```sld
name|Alice|age|30
```

### ✅ Correct: Using `;` (v2.0 delimiter)

```sld
name[Alice;age[30~
```

---

### ❌ Wrong: Not escaping special chars

```sld
note[Cost: $50; tax included
```

### ✅ Correct: Escaping semicolons

```sld
note[Cost: $50^; tax included~
```

---

### ❌ Wrong: Using string "true"

```sld
active[true
```

### ✅ Correct: Using boolean `^1`

```sld
active[^1~
```

---

### ❌ Wrong: Multiple lines

```sld
name[Alice
age[30
```

### ✅ Correct: Single line with separator

```sld
name[Alice;age[30~
```

---

## Performance Tips

1. **Use SLD for:** Network transmission, embedded data, single-packet sends
2. **Use MLD for:** Logs, streaming, grep filtering
3. **Token efficiency:** 78% smaller than JSON
4. **Byte efficiency:** 40-60% smaller than formatted JSON
5. **Parsing:** O(n) linear scan, no backtracking

---

## Shell Usage

### Extract property value (basic)

```bash
echo "name[Alice;age[30~" | grep -oP 'name\[\K[^;~]*'
# Output: Alice
```

### Filter records by property

```bash
# Convert to MLD first for easier filtering
tr '~' '\n' < data.sld | grep "status\[active"
```

### Count records

```bash
echo "rec1~rec2~rec3~" | tr '~' '\n' | grep -c '^'
# Output: 3
```

---

## Migration from v1.0

**Find and replace:**

- Replace all `|` field separators with `;`
- Update escape sequences: `^|` → `^;`
- Update parsers to split on `;` instead of `|`

**Example:**

```diff
- name[Alice|age[30|city[NYC~
+ name[Alice;age[30;city[NYC~
```

See [MIGRATION.md](MIGRATION.md) for complete guide.

---

## Related Documents

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Full technical specification
- [SYNTAX_GUIDE_SLD.md](SYNTAX_GUIDE_SLD.md) - Detailed syntax examples
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Multi-line variant
- [MIGRATION.md](MIGRATION.md) - v1.0 to v2.0 migration guide

---

## Quick Troubleshooting

**Problem:** Parser fails on semicolons in data  
**Solution:** Escape them with `^;`

**Problem:** Boolean values parsed as strings  
**Solution:** Use `^1` (true) or `^0` (false), not "true"/"false"

**Problem:** Last property missing  
**Solution:** Ensure record ends with `~`

**Problem:** Shell interprets semicolons  
**Solution:** Quote the SLD string: `"name[Alice;age[30~"`

---

**Version:** 1.1  
**Format:** SLD (Single Line Data)  
**Last Updated:** December 2024
