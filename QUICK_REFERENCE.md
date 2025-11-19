# SLD Format Quick Reference v2.0

## Three Ways to Represent Data

### 1. Table Format

**Best for:** Lists of similar items, CSV-like data, tabular data

**Structure:**

- First row = headers
- Subsequent rows = data
- Fields separated by `;` (v2.0 change from `|`)
- Rows separated by `~`

**Example:**

```sld
name;price;inStock~Laptop;3999.90;^1~Mouse;149.90;^0~Headset;499.00;^1
```

**JSON Equivalent:**

```json
[
  {"name": "Laptop", "price": 3999.90, "inStock": true},
  {"name": "Mouse", "price": 149.90, "inStock": false},
  {"name": "Headset", "price": 499.00, "inStock": true}
]
```

---

### 2. Object Format

**Best for:** Single objects, configuration data, key-value pairs

**Structure:**

- Properties: `property[value;`
- Last property: `property[value~`
- Always ends with `~`

**Example:**

```sld
name[John;age[30;city[NYC;active[^1~
```

**JSON Equivalent:**

```json
{
  "name": "John",
  "age": 30,
  "city": "NYC",
  "active": true
}
```

---

### 3. Array Format

**Best for:** Named arrays, collections of objects

**Structure:**

  - An object: `id[1;name[Ana~...`
  - A table row, following a header row

**Example:**

```sld
users{id[1;name[John;lastname[Smith]~id[2;name[Juan;lastname[Perez}}
```

**JSON Equivalent:**

```json
{
  "users": [
    {"id": 1, "name": "John", "lastname": "Smith"},
    {"id": 2, "name": "Juan", "lastname": "Perez"}
  ]
}
```

---

## Delimiters Reference

| Character | Purpose | Example |
|-----------|---------|---------|
| `;` | Property/field separator | `name[John;age[30;` |
| `~` | Record separator OR last property | `city[NYC~` |
| `[` | Property value marker | `name[John` |
| `{` | Array start | `users{` |
| `}` | Array end | `...}` |
| `^` | Escape & boolean prefix | `^1`, `^0`, `^;` |

---

## Boolean Values

- `^1` = `true`
- `^0` = `false`

**Examples:**

```sld
active[^1;verified[^0;premium[^1~
```

---

## Null/Empty Values

Empty value between delimiters:

```sld
name[John;middle[;lastname[Doe~
```

(middle name is null/empty)

---

## Escape Sequences

To include literal delimiter characters:

| Escape | Result | Example |
|--------|--------|---------|
| `^;` | Literal `;` | `company[ACME^; Corp;` |
| `^~` | Literal `~` | `model[XZ^~2000;` |
| `^[` | Literal `[` | `tag[Version^[1.0]` |
| `^{` | Literal `{` | `brace[Open^{Here;` |
| `^}` | Literal `}` | `brace[Close^};` |
| `^^` | Literal `^` | `caret[Power^^2;` |

---

## Complete Examples

### E-commerce Products (Table)

```sld
id;name;price;stock;featured~1;Laptop Pro;3999.90;15;^1~2;Wireless Mouse;149.90;50;^0~3;USB-C Headset;499.00;30;^1
```

### User Profile (Object)

```sld
userId[12345;username[john_doe;email[john@example.com;verified[^1;role[admin;lastLogin[2025-11-16~
```

### Team Members (Array)

```sld
team{name[Alice;role[Developer;active[^1;level[5]~name[Bob;role[Designer;active[^1;level[3]~name[Charlie;role[Manager;active[^0;level[7}}
```

### Mixed Data with Escaping

```sld
company[Tech^;Solutions Inc;email[contact@tech.com;motto[Innovation^~Excellence;founded[2020;active[^1~
```

---

## Choosing the Right Format

| Data Type | Use Format | Why |
|-----------|------------|-----|
| CSV-like lists | **Table** | Compact headers, clear structure |
| Configuration | **Object** | Self-documenting properties |
| Named collections | **Array** | Explicit array name + objects |
| Mixed types | **Object/Array** | Flexibility for nested data |

---

## Token Efficiency Comparison

**Original JSON (125 tokens):**

```json
{
  "products": [
    {"id": 1, "name": "Laptop", "price": 3999.90},
    {"id": 2, "name": "Mouse", "price": 149.90}
  ]
}
```

**SLD Array Format (~35 tokens):**

```sld
products{id[1;name[Laptop;price[3999.90]~id[2;name[Mouse;price[149.90]}
```

**SLD Table Format (~28 tokens):**

```sld
id;name;price~1;Laptop;3999.90~2;Mouse;149.90
```

**Result:** 72-78% token reduction! 🎉

---

## Common Patterns

### Empty Array

```sld
items{}
```

### Single Item Array

```sld
users{id[1;name[John;active[^1]}
```

### Nested Properties (Flattened)

```sld
user[name[John;address_street[Main St;address_city[NYC;address_zip[10001~
```

### Multiple Boolean Flags

```sld
permissions[read[^1;write[^1;delete[^0;admin[^0~
```

---

**Remember:** Choose Table for uniformity, Object for clarity, Array for named collections!
