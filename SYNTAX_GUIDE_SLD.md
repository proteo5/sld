# SLD Syntax Guide v2.0

**Comprehensive syntax examples and patterns for Single Line Data**

---

## Table of Contents

1. [Basic Syntax](#basic-syntax)
2. [Data Types in Detail](#data-types-in-detail)
3. [Escape Sequences](#escape-sequences)
4. [Arrays](#arrays)
5. [Complex Structures](#complex-structures)
6. [Real-World Examples](#real-world-examples)
7. [Anti-Patterns](#anti-patterns)
8. [Best Practices](#best-practices)

---

## Basic Syntax

### Single Property
```
name[Alice~
```
**Result:** `{"name": "Alice"}`

### Multiple Properties
```
name[Alice;age[30;city[NYC~
```
**Result:** `{"name": "Alice", "age": 30, "city": "NYC"}`

### Multiple Records
```
id[1;name[Alice~id[2;name[Bob~id[3;name[Charlie~
```
**Result:**
```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"},
  {"id": 3, "name": "Charlie"}
]
```

---

## Data Types in Detail

### Strings

**Simple string:**
```
greeting[Hello World~
```

**Empty string:**
```
value[;other[data~
```
Note: Empty between `[` and `;`

**String with spaces:**
```
address[123 Main Street, Apt 4B~
```

**Multi-word with punctuation:**
```
quote[To be, or not to be: that is the question.~
```

### Numbers

**Integer:**
```
count[42~
age[30~
year[2024~
### v2.0 Optional Features: Inline Types and Typed Null

Type hints are optional and negotiated via `!features{types}`. Place `!code` immediately before the value marker.

Codes: `!i` int, `!f` float, `!b` bool, `!s` string, `!n` null, `!d` date, `!t` time, `!ts` timestamp.

Examples:

```
age!i[42~
price!f[399.90~
active!b[^1~
title!s[Hello~
removed!n[~
ids!i{1~2~3}~
created!ts[2025-11-18T12:00:00Z~
```

Header negotiation (first record in SLD):

```
!v[1.2;!features{types~canon}~
```
```

**Decimal:**
```
price[99.99~
temperature[23.5~
```

**Negative:**
```
balance[-150.50~
celsius[-10~
```

**Scientific notation:**
```
avogadro[6.022e23~
planck[6.626e-34~
```

**Zero:**
```
offset[0~
```

### Booleans

**True:**
```
active[^1~
enabled[^1~
verified[^1~
```

**False:**
```
deleted[^0~
public[^0~
archived[^0~
```

**Mixed example:**
```
id[100;active[^1;verified[^0;premium[^1~
```

### Null Values

**Single null:**
```
middleName[;lastName[Smith~
```

**Multiple nulls:**
```
name[Alice;phone[;email[;address[123 Main St~
```

**All nulls:**
```
field1[;field2[;field3[~
```

---

## Escape Sequences

### Escaping Semicolons

**Data with semicolons:**
```
instructions[First, mix ingredients^; second, bake at 350°F~
```

**Multiple semicolons:**
```
list[Item 1^; Item 2^; Item 3^; Item 4~
```

### Escaping Tildes

**Filenames:**
```
backup[file~backup.txt becomes file^~backup.txt~
```

**URLs:**
```
permalink[http://example.com/page^~version~
```

### Escaping Brackets

**Mathematical expressions:**
```
formula[x^[0^] + y^[1^] = z~
```

**Array notation in text:**
```
code[array^{0^} = value~
```

### Escaping Carets

**Text with carets:**
```
symbol[Look up ^^ for more info~
exponent[x^^2 means x^{caret}2~
```

### Complex Escaping

**All special chars:**
```
text[Use ^; for fields^, ^~ for records^, ^[ for properties^, ^{ for arrays^, and ^^ for carets~
```

**Real example - code snippet:**
```
code[if (x ^> 5 ^&^& y ^< 10) ^{ return true^; ^}~
```

---

## Arrays

### Simple Arrays

**Strings:**
```
tags{red~green~blue}
```

**Numbers:**
```
scores{85~92~78~95~88}
```

**Mixed (treated as strings):**
```
data{Alice~30~true~null}
```

### Empty Arrays

```
items{}
```
Note: empty array closes with `}` (no elements)

### Single Element

```
singleton{value}
```

### Arrays with Escaped Content

**Elements with commas:**
```
items{Item 1^, Part A~Item 2~Item 3^, Part B}
```

**Elements with semicolons:**
```
notes{First note^; details here~Second note~Third note^; more info}
```

### Multiple Arrays in Record

```
id[1;tags{red~blue};scores{85~90};status[active~
```

---

## Complex Structures

### Nested Objects (Flattened)

**Approach 1: Underscore notation**
```
user_id[42;user_name[Alice;user_address_street[Main St;user_address_city[NYC;user_address_zip[10001~
```

**Approach 2: Dot notation**
```
user.id[42;user.name[Alice;user.address.street[Main St;user.address.city[NYC~
```

### Object with Multiple Arrays

```
user_id[42;username[alice;roles{admin~editor~viewer};permissions{read~write~delete};groups{dev~ops}~
```

### Table Format

**Headers + Data:**
```
id;name;price;stock~1;Laptop;999.99;^1~2;Mouse;29.99;^1~3;Keyboard;79.99;^0~
```

**Interpretation:**
- First record: headers
- Subsequent records: data rows

### Timestamped Records

```
ts[2024-12-01T08:00:00Z;event[login;user[alice;ip[192.168.1.100~ts[2024-12-01T08:05:00Z;event[logout;user[alice;duration[300~
```

---

## Real-World Examples

### User Profile

```
user_id[u_4892;username[alice_smith;email[alice@example.com;display_name[Alice Smith;bio[Software developer and coffee enthusiast;verified[^1;created_at[2023-05-15T10:30:00Z;avatar_url[https://cdn.example.com/avatars/alice.jpg;follower_count[1523;following_count[342;post_count[89~
```

### E-commerce Product

```
product_id[prod_8821;sku[LAPTOP-X1;name[UltraBook Pro 15;description[Lightweight laptop with 15-inch display^, 16GB RAM^, and 512GB SSD;price[1299.99;currency[USD;in_stock[^1;stock_quantity[45;categories{electronics~computers~laptops};tags{ultrabook~business~portable};rating[4.5;review_count[234;manufacturer[TechCorp;warranty_months[24~
```

### API Response

```
status[200;success[^1;message[Data retrieved successfully;timestamp[2024-12-01T14:22:33Z;data_count[3;records{id[1;name[Alice]~id[2;name[Bob]~id[3;name[Charlie]};meta_page[1;meta_per_page[20;meta_total[156~
```

### Log Entry

```
timestamp[2024-12-01T09:15:42.523Z;level[ERROR;service[payment-api;message[Payment processing failed: insufficient funds;user_id[u_9923;transaction_id[tx_44821;amount[250.00;currency[USD;error_code[E_INSUFFICIENT_FUNDS;retry_count[3;stack_trace[at processPayment (payment.js:145)~
```

### Configuration File

```
app_name[MyApp;version[2.1.0;environment[production;server_host[api.example.com;server_port[8443;server_ssl[^1;database_host[db.example.com;database_port[5432;database_name[myapp_prod;database_pool_size[20;cache_enabled[^1;cache_ttl[3600;log_level[info;allowed_origins{https://example.com~https://app.example.com};feature_flags{new_ui~beta_features~advanced_analytics}~
```

### CSV-like Data Export

```
employee_id;first_name;last_name;department;salary;hire_date;active~E001;John;Doe;Engineering;95000;2020-03-15;^1~E002;Jane;Smith;Marketing;87000;2019-07-22;^1~E003;Bob;Johnson;Sales;78000;2021-01-10;^1~E004;Alice;Williams;Engineering;102000;2018-11-05;^1~
```

---

## Anti-Patterns

### ❌ Don't: Use wrong delimiters (v1.0 syntax)

```
name|Alice|age|30
```

**Why:** v2.0 uses `;` not `|` for fields

**✅ Do:**
```
name[Alice;age[30~
```

---

### ❌ Don't: Forget to escape special characters

```
note[Cost: $50; includes tax
```

**Why:** Unescaped `;` breaks parsing

**✅ Do:**
```
note[Cost: $50^; includes tax~
```

---

### ❌ Don't: Use string literals for booleans

```
active[true;verified[false
```

**Why:** Parsed as strings, not booleans

**✅ Do:**
```
active[^1;verified[^0~
```

---

### ❌ Don't: Add line breaks

```
name[Alice
age[30
city[NYC
```

**Why:** SLD must be single-line

**✅ Do:**
```
name[Alice;age[30;city[NYC~
```
Or use MLD format for multi-line

---

### ❌ Don't: Use closing brackets/braces

```
tags[{red,green,blue}]
```

**Why:** No closing delimiters in SLD

**✅ Do:**
```
tags{red,green,blue~
```

---

### ❌ Don't: Mix property and table formats

```
name[Alice;age[30|city|NYC
```

**Why:** Inconsistent structure

**✅ Do (property format):**
```
name[Alice;age[30;city[NYC~
```

**✅ Do (table format):**
```
name;age;city~Alice;30;NYC~
```

---

### ❌ Don't: Use nested array syntax

```
matrix[[1,2],[3,4]]
```

**Why:** Arrays can't contain arrays in simple SLD

**✅ Do (flatten):**
```
row1{1,2;row2{3,4~
```

---

## Best Practices

### 1. Consistent Property Naming

**✅ Good:**
```
user_id[42;user_name[Alice;user_email[alice@example.com~
```

**❌ Inconsistent:**
```
userId[42;user_name[Alice;UserEmail[alice@example.com~
```

### 2. Explicit Booleans

**✅ Good:**
```
active[^1;verified[^0~
```

**❌ Ambiguous:**
```
active[1;verified[0~
```
(Could be numbers or booleans)

### 3. Use Null for Missing Data

**✅ Good:**
```
name[Alice;middleName[;lastName[Smith~
```

**❌ Bad:**
```
name[Alice;middleName[null;lastName[Smith~
```
(String "null" instead of actual null)

### 4. Order Properties Logically

**✅ Good (related fields together):**
```
id[42;username[alice;email[alice@example.com;created[2024-01-01;active[^1~
```

**❌ Poor (random order):**
```
active[^1;username[alice;id[42;created[2024-01-01;email[alice@example.com~
```

### 5. Quote in Shell Scripts

**✅ Good:**
```bash
data="name[Alice;age[30~"
echo "$data"
```

**❌ Bad:**
```bash
data=name[Alice;age[30~  # Shell interprets semicolons!
```

### 6. Validate Before Encoding

**✅ Good:**
```python
def safe_encode(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "^1" if value else "^0"
    return escape(str(value))
```

### 7. Use Consistent Escaping

**✅ Good:**
```python
# Escape in consistent order
s = s.replace("^", "^^")  # Always escape ^ first!
s = s.replace(";", "^;")
s = s.replace("~", "^~")
s = s.replace("[", "^[")
s = s.replace("{", "^{")
```

### 8. Document Your Schema

**✅ Good:**
```
# User schema: id, username, email, verified, created_at
id[42;username[alice;email[alice@example.com;verified[^1;created_at[2024-01-15T10:00:00Z~
```

### 9. Use SLD/MLD Appropriately

**Use SLD for:**
- Network transmission
- Single-packet data
- Embedded configs
- Memory-constrained environments

**Use MLD for:**
- Log files
- Streaming data
- Grep-friendly processing
- Human debugging

### 10. Version Your Data

**✅ Good:**
```
version[1.1;format[sld;data{id[1;name[Alice~
```

---

## Syntax Comparison

### SLD vs JSON

**JSON:**
```json
{"name": "Alice", "age": 30, "tags": ["admin", "user"]}
```

**SLD:**
```
name[Alice;age[30;tags{admin,user~
```

**Savings:** 53 bytes → 32 bytes (40% reduction)

---

### SLD vs CSV

**CSV:**
```
name,age,city
Alice,30,NYC
Bob,25,LA
```

**SLD (table format):**
```
name;age;city~Alice;30;NYC~Bob;25;LA~
```

**SLD (object format):**
```
name[Alice;age[30;city[NYC~name[Bob;age[25;city[LA~
```

---

### SLD vs XML

**XML:**
```xml
<user>
  <name>Alice</name>
  <age>30</age>
</user>
```

**SLD:**
```
name[Alice;age[30~
```

**Savings:** 58 bytes → 19 bytes (67% reduction)

---

## Advanced Patterns

### Conditional Properties

**Include property only if value exists:**
```python
def encode_with_optional(obj):
    parts = []
    for k, v in obj.items():
        if v is not None and v != "":
            parts.append(f"{escape(k)}[{escape(str(v))}")
    return ";".join(parts) + "~"
```

### Streaming Encoder

**Generate SLD incrementally:**
```python
def stream_encode(objects):
    for obj in objects:
        yield encode_object(obj)
```

### Chunked Parsing

**Parse large SLD in chunks:**
```python
def parse_chunked(sld_string, chunk_size=1000):
    records = sld_string.split('~')
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i+chunk_size]
        yield [decode_record(r) for r in chunk if r]
```

---

## Related Documents

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Full technical specification
- [QUICK_REFERENCE_SLD.md](QUICK_REFERENCE_SLD.md) - Quick lookup guide
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Multi-line variant
- [MIGRATION.md](MIGRATION.md) - v1.0 to v2.0 migration

---

**Version:** 1.1  
**Format:** SLD (Single Line Data)  
**Last Updated:** December 2024
