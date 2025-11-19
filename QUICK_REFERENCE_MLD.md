# MLD Quick Reference v2.0

**Multi Line Data - Fast reference for developers**

---

## Delimiters (v2.0)

| Symbol | Purpose | Example |
|--------|---------|---------|
| `;` | Field separator | `name[Alice;age[30` |
| `\n` | Record separator (newline) | One record per line |
| `[` | Property marker | `name[value` |
| `{` | Array start | `tags{red~blue}` |
| `}` | Array end | `...}` |
| `^` | Escape character | `text[Hello^; World` |

**Key Difference from SLD:** MLD uses actual newlines (`\n`) instead of tilde (`~`) to separate records.

---

## Escape Sequences

| Sequence | Result |
|----------|--------|
| `^;` | Literal `;` |
| `^[` | Literal `[` |
| `^{` | Literal `{` |
| `^}` | Literal `}` |
| `^^` | Literal `^` |

Note: Represent newlines inside values as the two characters `\n`.

**Example:**
```
desc[Price: $100^; includes tax
```

---

## Data Types

### String
```
name[Alice
city[New York
```

### Number
```
age[30
price[99.99
scientific[6.022e23
```

### Boolean
```
active[^1        # true
verified[^0      # false
```

### Null
```
middleName[;age[30    # middleName is null
```

### Array
```
tags{red~green~blue}
scores{85~92~78}
```

---
## v2.0 Optional Features (inline types and typed null)

These features are additive and negotiated via a metadata header (`!features{types}`); decoders without support may ignore type hints.

### Inline Type Tags

- Place `!code` immediately before `[` or `{`.
- Codes: `!i` int, `!f` float, `!b` bool, `!s` string, `!n` null, `!d` date, `!t` time, `!ts` timestamp.

Examples:

```
age!i[42; price!f[399.90; active!b[^1; title!s[Hello
ids!i{1~2~3}
created!ts[2025-11-18T12:00:00Z
removed!n[    # typed null (empty payload)
```

### Header Metadata (line 0)

```
!v[1.2;!features{types~canon}
id!i[1;name!s[Ana
```

## Basic Examples

### Simple Object (Single Line)
```
name[Alice;age[30;city[NYC
```

### Multiple Records (Multiple Lines)
```
id[1;name[Alice
id[2;name[Bob
id[3;name[Charlie
```

### Object with Array
```
user[alice;tags{admin~user};score[95
```

### Escaped Content
```
note[Use semicolons^; not commas;date[2024-01-15
```

---

## Common Patterns

### User Record
```
id[42;username[alice;email[alice@example.com;verified[^1;role[admin
```

### Product Catalog
```
sku[LAP001;name[Laptop;price[999.99;stock[^1;tags{electronics~computers}
```

### Log Entry
```
timestamp[2024-12-01T10:30:00Z;level[INFO;service[api;message[Request processed;user[alice
```

### Configuration
```
host[localhost;port[8080;ssl[^1;timeout[30;retries[3
```

---

## Unix Tool Usage

### Filter with grep
```bash
# Find all ERROR level logs
grep "level\[ERROR" app.mld

# Find specific user activity
grep "user\[alice" activity.mld

# Case-insensitive search
grep -i "status\[active" users.mld
```

### Count with wc
```bash
# Count total records
wc -l data.mld

# Count errors
grep "level\[ERROR" logs.mld | wc -l
```

### Head/Tail
```bash
# First 10 records
head -10 data.mld

# Last 20 records
tail -20 data.mld

# Real-time log monitoring
tail -f logs.mld
```

### Extract with awk
```bash
# Extract name field from each record
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^name\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}' users.mld
```

### Process with sed
```bash
# Replace status values
sed 's/status\[pending/status[active/g' tasks.mld

# Delete records
sed '/deleted\[^1/d' users.mld
```

---

## Encoding Cheatsheet

**Python:**
```python
def escape(s):
  return (
    s.replace("^", "^^")
     .replace(";", "^;")
     .replace("[", "^[")
     .replace("{", "^{")
     .replace("}", "^}")
     .replace("\n", "\\n")
  )

def encode_record(obj):
    parts = [f"{escape(k)}[{escape(str(v))}" for k, v in obj.items()]
    return ";".join(parts)

# Write multiple records
with open('data.mld', 'w') as f:
    for record in records:
        f.write(encode_record(record) + '\n')
```

**JavaScript:**
```javascript
const escape = s => (
  s
    .replace(/\^/g, '^^')
    .replace(/;/g, '^;')
    .replace(/\[/g, '^[')
    .replace(/\{/g, '^{')
    .replace(/\}/g, '^}')
    .replace(/\n/g, '\\n')
);

const encodeRecord = obj => {
  const pairs = Object.entries(obj).map(([k, v]) => `${escape(k)}[${escape(String(v))}`);
  return pairs.join(';');
};

// Write to file
const lines = records.map(r => encodeRecord(r)).join('\n');
fs.writeFileSync('data.mld', lines);
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

def decode_record(line):
    obj = {}
    for prop in line.split(';'):
        if '[' in prop:
            key, value = prop.split('[', 1)
            obj[unescape(key)] = unescape(value)
    return obj

# Read file line by line
records = []
with open('data.mld', 'r') as f:
    for line in f:
        records.append(decode_record(line.rstrip('\n')))
```

---

## Conversion (MLD ↔ SLD)

**MLD to SLD:**
```bash
tr '\n' '~' < data.mld > data.sld
```

**SLD to MLD:**
```bash
tr '~' '\n' < data.sld > data.mld
```

**Python conversion:**
```python
# MLD to SLD
with open('data.mld', 'r') as f:
    sld = f.read().replace('\n', '~')
    
# SLD to MLD
with open('data.sld', 'r') as f:
    mld = f.read().replace('~', '\n')
```

---

## Common Mistakes

### ❌ Wrong: Embedding unescaped newlines

```
description[First line
Second line
```

### ✅ Correct: Escape newlines or keep on one line

```
description[First line^\nSecond line
```

---

### ❌ Wrong: Using tilde separator

```
name[Alice;age[30~
```

### ✅ Correct: Use newline (one record per line)

```
name[Alice;age[30
```

---

### ❌ Wrong: Not escaping semicolons

```
note[Cost: $50; includes tax
```

### ✅ Correct: Escape semicolons

```
note[Cost: $50^; includes tax
```

---

## MLD vs SLD - When to Use

### Use MLD for:

✅ **Log files** - Real-time monitoring with `tail -f`  
✅ **Streaming data** - Process records incrementally  
✅ **Grep filtering** - Fast text search without parsing  
✅ **Line-based tools** - sed, awk, head, tail, wc  
✅ **Human debugging** - One record per line, easy to read  
✅ **Large datasets** - Process with constant memory

### Use SLD for:

✅ **Network transmission** - Single-packet data  
✅ **Embedded configs** - Single-line strings in code  
✅ **Memory-constrained** - Slightly smaller footprint  
✅ **Bulk transfer** - Fewer delimiters (minimal overhead)

---

## Streaming Example

**Process large MLD file with constant memory:**

```python
def process_mld_stream(filename, callback):
    """Process MLD file line by line."""
    with open(filename, 'r') as f:
        for line in f:
            record = decode_record(line.rstrip('\n'))
            callback(record)

# Usage
def handle_record(record):
    if record.get('level') == 'ERROR':
        print(f"Error: {record.get('message')}")

process_mld_stream('logs.mld', handle_record)
```

---

## Real-Time Log Monitoring

```bash
# Monitor logs in real-time
tail -f app.mld | grep "level\[ERROR"

# Count errors per minute
tail -f app.mld | grep "level\[ERROR" | while read line; do
  echo "$(date): ERROR detected"
done

# Extract and process
tail -f app.mld | awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^message\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}'
```

---

## Performance Tips

1. **Streaming:** Process line-by-line for large files
2. **Memory:** MLD uses constant memory with streaming
3. **Grep:** Faster than parsing for simple filters
4. **Indexing:** Build line offset index for random access
5. **Parallel:** Process chunks in parallel with `split`

**Split file for parallel processing:**
```bash
# Split into 4 chunks
split -n 4 data.mld chunk_

# Process in parallel
for chunk in chunk_*; do
  process_chunk.sh "$chunk" &
done
wait
```

---

## Quick Troubleshooting

**Problem:** Grep not finding records  
**Solution:** Check for escaped semicolons in search pattern

**Problem:** Extra blank lines in output  
**Solution:** Use `grep -v '^$'` to filter empty lines

**Problem:** Records split across lines  
**Solution:** Ensure no literal newlines in property values

**Problem:** Performance slow on large files  
**Solution:** Use streaming/line-by-line processing, not loading full file

---

## Related Documents

- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Full technical specification
- [SYNTAX_GUIDE_MLD.md](SYNTAX_GUIDE_MLD.md) - Detailed syntax examples
- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Single-line variant
- [MIGRATION.md](MIGRATION.md) - v1.0 to v2.0 migration guide

---

**Version:** 1.1  
**Format:** MLD (Multi Line Data)  
**Last Updated:** December 2024
