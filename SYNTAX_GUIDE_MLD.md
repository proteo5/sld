# MLD Syntax Guide v2.0

## Comprehensive syntax examples and patterns for Multi Line Data

---

## Table of Contents

1. [Basic Syntax](#basic-syntax)
2. [Data Types in Detail](#data-types-in-detail)
3. [Escape Sequences](#escape-sequences)
4. [Arrays](#arrays)
5. [Unix Tool Integration](#unix-tool-integration)
6. [Real-World Examples](#real-world-examples)
7. [Streaming Patterns](#streaming-patterns)
8. [Anti-Patterns](#anti-patterns)
9. [Best Practices](#best-practices)

---

## Basic Syntax

### Single Record (One Line)

```sld
name[Alice;age[30;city[NYC
```
**Result:** `{"name": "Alice", "age": 30, "city": "NYC"}`

### Multiple Records (Multiple Lines)

```sld
id[1;name[Alice
id[2;name[Bob
id[3;name[Charlie
```
**Result:**
```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"},
  {"id": 3, "name": "Charlie"}
]
```

### Empty File

```text
(no content)
```
**Result:** `[]` (empty collection)

### Single Property Record

```sld
status[ok
```
**Result:** `{"status": "ok"}`

---

## Data Types in Detail

### Strings

**Simple string:**
```
greeting[Hello World
```

**Empty string:**
```
value[;other[data
```

**String with spaces:**
```
address[123 Main Street, Apt 4B
```

### v2.0 Optional Features: Inline Types

Type hints are optional and negotiated via `!features{types}`. Place `!code` immediately before the value marker.

Codes: `!i` int, `!f` float, `!b` bool, `!s` string, `!d` date, `!t` time, `!ts` timestamp.

Null values use escape sequence `^_`.

Examples:

```
age!i[42
price!f[399.90
active!b[^1
title!s[Hello
removed[^_
ids!i{1~2~3}
created!ts[2025-11-18T12:00:00Z
```

Header negotiation (line 0 in MLD):

```
!v[1.2;!features{types~canon}
```

**Multi-line text (escaped):**
```
description[Line 1\nLine 2\nLine 3
```
Note: Literal newlines must be escaped within property values

### Numbers

**Integers:**
```
count[42
age[30
year[2024
```

**Decimals:**
```
price[99.99
temperature[23.5
```

**Negative:**
```
balance[-150.50
offset[-10
```

**Scientific notation:**
```
avogadro[6.022e23
planck[6.626e-34
```

### Booleans

**True:**
```
active[^1
enabled[^1
verified[^1
```

**False:**
```
deleted[^0
public[^0
archived[^0
```

**Multiple booleans:**
```
id[100;active[^1;verified[^0;premium[^1
```

### Null Values

**Single null:**
```
middleName[;lastName[Smith
```

**Multiple nulls:**
```
name[Alice;phone[;email[;address[123 Main
```

### Arrays

**String array:**

```sld
tags{red~green~blue}
```

**Number array:**

```sld
scores{85~92~78~95}
```

**Mixed (as strings):**

```sld
data{Alice~30~NYC}
```

**Empty array:**

```sld
items{}
```

---

## Escape Sequences

### Escaping Semicolons

**Simple:**
```
note[First item^; second item^; third item
```

**In description:**
```
instructions[Mix ingredients^; bake at 350°F^; cool for 10 minutes
```

### Escaping Newlines

**Multi-line content:**
```
message[Hello\nThis is line 2\nAnd line 3
```

**Poem:**
```
poem[Roses are red\nViolets are blue\nData is compact\nAnd efficient too
```

### Escaping Brackets

**Code snippet:**
```
code[array^[0^] = value
```

**Expression:**
```
formula[x^[2^] + y^[3^] = z
```

### Escaping Braces

**JSON-like text:**
```
example[Use ^{key: value^} for objects
```

### Escaping Carets

**Exponent notation:**
```
math[2^^3 means 2 to the power of 3
```

**Multiple escapes:**
```
text[Use ^^; ^^ is the escape character
```

---

## Arrays

### Simple Arrays

```sld
colors{red~orange~yellow~green~blue}
numbers{1~2~3~4~5~6~7~8~9~10}
```

### Arrays with Escaped Tildes

```sld
items{Item 1^~ part A~Item 2~Item 3^~ part B}
```

### Multiple Arrays in Record

```sld
id[1;tags{web~mobile~api};scores{95~87~92};status[active
```

### Long Arrays

```sld
keywords{javascript~python~java~cpp~csharp~go~rust~ruby~php~swift~kotlin~typescript
```

---

## Unix Tool Integration

### Grep Examples

**Find records by field value:**
```bash
# All active users
grep "status\[active" users.mld

# Specific user
grep "username\[alice" users.mld

# Error logs
grep "level\[ERROR" app.mld

# Multiple patterns
grep -E "level\[(ERROR|WARN)" app.mld
```

**Count matches:**
```bash
# Count errors
grep -c "level\[ERROR" app.mld

# Count active users
grep -c "active\[^1" users.mld
```

**Invert match:**
```bash
# All non-deleted records
grep -v "deleted\[^1" data.mld
```

### Awk Examples

**Extract specific field:**
```bash
# Extract all usernames
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^username\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}' users.mld
```

**Calculate statistics:**
```bash
# Average age
awk -F';' '
{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^age\[/) {
      split($i, arr, "[")
      sum += arr[2]
      count++
    }
  }
}
END {
  if (count > 0) print "Average age:", sum/count
}' users.mld
```

**Filter and transform:**
```bash
# Extract name and email
awk -F';' '{
  name = ""; email = ""
  for (i=1; i<=NF; i++) {
    if ($i ~ /^name\[/) { split($i, a, "["); name = a[2] }
    if ($i ~ /^email\[/) { split($i, a, "["); email = a[2] }
  }
  if (name && email) print name, email
}' users.mld
```

### Sed Examples

**Replace values:**
```bash
# Update status
sed 's/status\[pending/status[completed/g' tasks.mld

# Update prices
sed 's/price\[99.99/price[79.99/g' products.mld
```

**Delete lines:**
```bash
# Remove deleted records
sed '/deleted\[^1/d' data.mld

# Remove test data
sed '/^test/d' data.mld
```

### Head/Tail Examples

**First/last records:**
```bash
# First 10 records
head -10 data.mld

# Last 20 records
tail -20 data.mld

# Skip first 100, show next 10
tail -n +101 data.mld | head -10
```

**Real-time monitoring:**
```bash
# Follow log file
tail -f app.mld

# Follow with filter
tail -f app.mld | grep "level\[ERROR"

# Follow multiple files
tail -f app.mld access.mld
```

### Sort Examples

**Sort by extracted field:**
```bash
# Sort by age
awk -F';' '{
  age = 0
  for (i=1; i<=NF; i++) {
    if ($i ~ /^age\[/) { split($i, a, "["); age = a[2] }
  }
  print age "\t" $0
}' users.mld | sort -n | cut -f2-
```

### Uniq Examples

**Count duplicates:**
```bash
# Count records per status
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^status\[/) { split($i, a, "["); print a[2] }
  }
}' tasks.mld | sort | uniq -c
```

### Combining Tools

**Complex pipeline:**
```bash
# Find active premium users, extract emails, sort
grep "active\[^1" users.mld | \
  grep "premium\[^1" | \
  awk -F';' '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /^email\[/) { split($i, a, "["); print a[2] }
    }
  }' | \
  sort | \
  uniq
```

---

## Real-World Examples

### Application Logs

```
timestamp[2024-12-01T08:00:00Z;level[INFO;service[auth;message[User login;user[alice;ip[192.168.1.10
timestamp[2024-12-01T08:01:15Z;level[WARN;service[database;message[Slow query;duration[1.2s;query[SELECT * FROM users
timestamp[2024-12-01T08:02:30Z;level[ERROR;service[payment;message[Payment failed;user[bob;amount[99.99;error[E_CARD_DECLINED
timestamp[2024-12-01T08:03:45Z;level[INFO;service[auth;message[User logout;user[alice;session_duration[225s
```

**Process with grep:**
```bash
# All errors
grep "level\[ERROR" app.mld

# Errors for specific service
grep "level\[ERROR" app.mld | grep "service\[payment"

# Today's logs
grep "2024-12-01" app.mld
```

### User Database

```
id[1;username[alice;email[alice@example.com;verified[^1;created[2023-01-15;role[admin;last_login[2024-12-01
id[2;username[bob;email[bob@example.com;verified[^1;created[2023-03-22;role[user;last_login[2024-11-30
id[3;username[charlie;email[charlie@example.com;verified[^0;created[2024-01-10;role[user;last_login[
id[4;username[diana;email[diana@example.com;verified[^1;created[2022-11-05;role[moderator;last_login[2024-12-01
```

**Queries:**
```bash
# Verified users
grep "verified\[^1" users.mld

# Admins
grep "role\[admin" users.mld

# Never logged in
grep "last_login\[;" users.mld
```

### Product Catalog

```
sku[LAP001;name[UltraBook Pro 15;price[1299.99;stock[^1;quantity[45;category[laptops;tags{business~ultrabook~portable}
sku[MOU001;name[Wireless Mouse;price[29.99;stock[^1;quantity[200;category[accessories;tags{wireless~ergonomic}
sku[KEY001;name[Mechanical Keyboard;price[149.99;stock[^0;quantity[0;category[accessories;tags{mechanical~rgb~gaming}
sku[MON001;name[4K Monitor 27-inch;price[499.99;stock[^1;quantity[15;category[monitors;tags{4k~ips~professional}
```

**Queries:**
```bash
# In stock items
grep "stock\[^1" products.mld

# Out of stock
grep "stock\[^0" products.mld

# Price range (requires awk)
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^price\[/) {
      split($i, a, "[")
      if (a[2] >= 100 && a[2] <= 500) print $0
    }
  }
}' products.mld
```

### Access Logs

```
timestamp[2024-12-01T10:00:00Z;method[GET;path[/api/users;status[200;duration[45ms;ip[192.168.1.100
timestamp[2024-12-01T10:00:05Z;method[POST;path[/api/login;status[200;duration[120ms;ip[192.168.1.101
timestamp[2024-12-01T10:00:10Z;method[GET;path[/api/products;status[404;duration[15ms;ip[192.168.1.102
timestamp[2024-12-01T10:00:15Z;method[DELETE;path[/api/users/5;status[403;duration[10ms;ip[192.168.1.103
```

**Analysis:**
```bash
# 404 errors
grep "status\[404" access.mld

# Slow requests
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^duration\[/) {
      split($i, a, "[")
      if (a[2] ~ /[0-9]+ms/ && int(a[2]) > 100) print $0
    }
  }
}' access.mld

# Request count by method
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^method\[/) { split($i, a, "["); print a[2] }
  }
}' access.mld | sort | uniq -c
```

---

## Streaming Patterns

### Line-by-Line Processing

**Python:**
```python
def process_mld_file(filename):
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = decode_record(line.rstrip('\n'))
                process_record(record)
            except Exception as e:
                print(f"Error on line {line_num}: {e}")
```

**Node.js:**
```javascript
const fs = require('fs');
const readline = require('readline');

async function processMLD(filename) {
  const fileStream = fs.createReadStream(filename);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  for await (const line of rl) {
    const record = decodeRecord(line);
    processRecord(record);
  }
}
```

### Filtering While Streaming

**Python:**
```python
def filter_mld(input_file, output_file, predicate):
    with open(input_file, 'r') as fin:
        with open(output_file, 'w') as fout:
            for line in fin:
                record = decode_record(line.rstrip('\n'))
                if predicate(record):
                    fout.write(line)

# Usage
filter_mld('all.mld', 'active.mld', lambda r: r.get('active') == '^1')
```

### Chunked Processing

**Python:**
```python
def process_chunks(filename, chunk_size=1000):
    chunk = []
    with open(filename, 'r') as f:
        for line in f:
            chunk.append(decode_record(line.rstrip('\n')))
            if len(chunk) >= chunk_size:
                process_chunk(chunk)
                chunk = []
        if chunk:  # Process remaining
            process_chunk(chunk)
```

---

## Anti-Patterns

### ❌ Don't: Embed literal newlines

```
description[This is line 1
This is line 2
```

**Why:** Creates multiple records instead of one

**✅ Do:**
```
description[This is line 1\nThis is line 2
```

---

### ❌ Don't: Forget to escape semicolons

```
note[Price is $50; tax included
```

**Why:** Parser sees two fields

**✅ Do:**
```
note[Price is $50^; tax included
```

---

### ❌ Don't: Load entire file for simple queries

```python
# Bad: Load everything
with open('huge.mld', 'r') as f:
    all_data = f.read()
    # Parse and search...
```

**✅ Do: Stream and filter:**
```python
# Good: Stream line by line
with open('huge.mld', 'r') as f:
    for line in f:
        if 'status[ERROR' in line:
            print(line)
```

---

### ❌ Don't: Use MLD for single-packet transmission

**Why:** SLD is more efficient for network sends

**✅ Do: Convert to SLD:**
```python
# Read MLD, send as SLD
with open('data.mld', 'r') as f:
    sld = f.read().replace('\n', '~')
    send_over_network(sld)
```

---

## Best Practices

### 1. One Record Per Line (Always)

**✅ Good:**
```
id[1;name[Alice
id[2;name[Bob
```

### 2. Escape All Special Characters

**✅ Good:**
```python
def escape_for_mld(s):
    s = s.replace("^", "^^")
    s = s.replace(";", "^;")
    s = s.replace("[", "^[")
  s = s.replace("{", "^{")
  s = s.replace("}", "^}")
  s = s.replace("\n", "\\n")
    return s
```

### 3. Use Streaming for Large Files

**✅ Good:**
```python
# Process 1GB file with constant memory
for line in open('huge.mld'):
    record = decode_record(line.rstrip('\n'))
    if record['status'] == 'active':
        process(record)
```

### 4. Leverage Unix Tools

**✅ Good:**
```bash
# Fast filtering without parsing
grep "level\[ERROR" app.mld | wc -l
```

### 5. Validate Line Endings

**✅ Good:**
```python
# Normalize line endings
with open('data.mld', 'r') as f:
    for line in f:
        line = line.rstrip('\r\n')  # Handle \r\n or \r
        # Process line...
```

### 6. Index for Random Access

**✅ Good:**
```python
# Build index of line offsets
def build_index(filename):
    index = []
    with open(filename, 'rb') as f:
        while True:
            offset = f.tell()
            line = f.readline()
            if not line:
                break
            index.append(offset)
    return index

# Random access using index
def get_record(filename, index, record_num):
    with open(filename, 'rb') as f:
        f.seek(index[record_num])
        line = f.readline().decode('utf-8')
        return decode_record(line.rstrip('\n'))
```

### 7. Compress for Storage

**✅ Good:**
```bash
# MLD compresses very well
gzip data.mld  # Often 80-90% reduction

# Process compressed directly
zcat data.mld.gz | grep "status\[active"
```

### 8. Use Appropriate Tools

**For simple filtering:** Use `grep`  
**For field extraction:** Use `awk`  
**For transformations:** Use `sed`  
**For complex logic:** Use Python/Node.js

---

## Related Documents

- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Full technical specification
- [QUICK_REFERENCE_MLD.md](QUICK_REFERENCE_MLD.md) - Quick lookup guide
- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Single-line variant
- [MIGRATION.md](MIGRATION.md) - v1.0 to v2.0 migration

---

**Version:** 1.1  
**Format:** MLD (Multi Line Data)  
**Last Updated:** December 2024
