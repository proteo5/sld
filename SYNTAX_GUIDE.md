# SLD Format Syntax Examples

## Complete Syntax Breakdown

### Property Syntax
```
property[value|    ← Property with pipe separator
property[value~    ← Last property with tilde separator
```

### Data Types

#### Strings
```
name[John Smith|
city[New York|
```

#### Numbers
```
age[30|
price[3999.90|
count[42|
```

#### Booleans
```
active[^1|      ← true
verified[^0|    ← false
premium[^1~     ← true (last property)
```

#### Null/Empty
```
middle[|        ← empty/null value
optional[~      ← empty/null last property
```

### Three Main Formats

#### 1. TABLE FORMAT
```
┌─────────────────────────────────────────────────┐
│ header1|header2|header3                         │ ← Headers
│ ~                                               │ ← Separator
│ value1|value2|value3                            │ ← Row 1
│ ~                                               │ ← Separator
│ value4|value5|value6                            │ ← Row 2
└─────────────────────────────────────────────────┘

ACTUAL:
id|name|active~1|John|^1~2|Jane|^0
```

#### 2. OBJECT FORMAT
```
┌─────────────────────────────────────────────────┐
│ prop1[val1|                                     │ ← Property 1
│ prop2[val2|                                     │ ← Property 2
│ prop3[val3~                                     │ ← Last property
└─────────────────────────────────────────────────┘

ACTUAL:
name[John|age[30|city[NYC~
```

#### 3. ARRAY FORMAT
```
┌─────────────────────────────────────────────────┐
│ arrayName{                                      │ ← Array start
│   prop1[val1|prop2[val2~                        │ ← Object 1
│   prop1[val3|prop2[val4                         │ ← Object 2 (last, no ~)
└─────────────────────────────────────────────────┘

ACTUAL:
users{name[John|age[30~name[Jane|age[28
```

## Real-World Examples

### Example 1: Product Catalog (Table Format)

**Scenario:** E-commerce product list

**JSON:**
```json
[
  {"sku": "LAP001", "name": "Laptop Pro 15", "price": 3999.90, "stock": 25, "featured": true},
  {"sku": "MOU002", "name": "Wireless Mouse", "price": 149.90, "stock": 150, "featured": false},
  {"sku": "KEY003", "name": "Mechanical Keyboard", "price": 299.00, "stock": 75, "featured": true}
]
```

**SLD (Table):**
```
sku|name|price|stock|featured~LAP001|Laptop Pro 15|3999.90|25|^1~MOU002|Wireless Mouse|149.90|150|^0~KEY003|Mechanical Keyboard|299.00|75|^1
```

**Token Count:** JSON: ~145 tokens | SLD: ~42 tokens | **Savings: 71%**

---

### Example 2: User Profile (Object Format)

**Scenario:** User account settings

**JSON:**
```json
{
  "userId": "usr_89234",
  "username": "john_developer",
  "email": "john@example.com",
  "verified": true,
  "role": "admin",
  "twoFactorEnabled": false,
  "lastLogin": "2025-11-16T10:30:00Z"
}
```

**SLD (Object):**
```
userId[usr_89234|username[john_developer|email[john@example.com|verified[^1|role[admin|twoFactorEnabled[^0|lastLogin[2025-11-16T10:30:00Z~
```

**Token Count:** JSON: ~85 tokens | SLD: ~38 tokens | **Savings: 55%**

---

### Example 3: Team Members (Array Format)

**Scenario:** Development team roster

**JSON:**
```json
{
  "team": [
    {"id": 1, "name": "Alice Johnson", "role": "Lead Developer", "active": true, "level": 5},
    {"id": 2, "name": "Bob Smith", "role": "UI Designer", "active": true, "level": 3},
    {"id": 3, "name": "Charlie Brown", "role": "Project Manager", "active": false, "level": 7}
  ]
}
```

**SLD (Array):**
```
team{id[1|name[Alice Johnson|role[Lead Developer|active[^1|level[5~id[2|name[Bob Smith|role[UI Designer|active[^1|level[3~id[3|name[Charlie Brown|role[Project Manager|active[^0|level[7
```

**Token Count:** JSON: ~135 tokens | SLD: ~58 tokens | **Savings: 57%**

---

### Example 4: API Response with Mixed Data

**Scenario:** Search results with metadata

**JSON:**
```json
{
  "query": "laptop",
  "totalResults": 147,
  "page": 1,
  "hasMore": true,
  "results": [
    {"id": "p1", "title": "Gaming Laptop", "price": 2499.99, "rating": 4.5},
    {"id": "p2", "title": "Business Laptop", "price": 1899.00, "rating": 4.8}
  ]
}
```

**SLD (Object + Nested Array):**
```
query[laptop|totalResults[147|page[1|hasMore[^1|results{id[p1|title[Gaming Laptop|price[2499.99|rating[4.5~id[p2|title[Business Laptop|price[1899.00|rating[4.8
```

**Token Count:** JSON: ~110 tokens | SLD: ~52 tokens | **Savings: 53%**

---

## Edge Cases & Special Scenarios

### Escaped Characters Example

**Data with delimiters in values:**

**JSON:**
```json
{
  "company": "Tech|Solutions Inc",
  "slogan": "Innovation~Excellence",
  "version": "v[2.0]",
  "formula": "E=mc^2"
}
```

**SLD:**
```
company[Tech^|Solutions Inc|slogan[Innovation^~Excellence|version[v^[2.0^]|formula[E=mc^^2~
```

### Empty/Null Values Example

**JSON:**
```json
{
  "firstName": "John",
  "middleName": null,
  "lastName": "Doe",
  "suffix": ""
}
```

**SLD:**
```
firstName[John|middleName[|lastName[Doe|suffix[~
```

### Complex Nested Data (Flattened)

**JSON:**
```json
{
  "user": {
    "name": "John",
    "address": {
      "street": "123 Main St",
      "city": "NYC",
      "zip": "10001"
    }
  }
}
```

**SLD (Flattened naming):**
```
user_name[John|user_address_street[123 Main St|user_address_city[NYC|user_address_zip[10001~
```

---

## Format Selection Guide

```
┌─────────────────────┬──────────────┬────────────────────┐
│ Data Characteristic │ Best Format  │ Reason             │
├─────────────────────┼──────────────┼────────────────────┤
│ Uniform rows        │ TABLE        │ Shared headers     │
│ Single entity       │ OBJECT       │ Self-documenting   │
│ Named collection    │ ARRAY        │ Clear grouping     │
│ CSV-like data       │ TABLE        │ Natural fit        │
│ Config/Settings     │ OBJECT       │ Key clarity        │
│ Many similar items  │ TABLE/ARRAY  │ Compact            │
│ Few properties      │ OBJECT       │ Readable           │
│ Nested structures   │ OBJECT       │ Flatten with _     │
└─────────────────────┴──────────────┴────────────────────┘
```

---

## Validation Checklist

✅ **Table Format:**
- [ ] First row contains headers
- [ ] All rows have same number of fields
- [ ] Rows separated by `~`
- [ ] Fields separated by `|`

✅ **Object Format:**
- [ ] Properties use `property[value|` syntax
- [ ] Last property ends with `~`
- [ ] All properties have `[` after name
- [ ] Booleans use `^0` or `^1`

✅ **Array Format:**
- [ ] Starts with `arrayName{`
- [ ] Objects separated by `~`
- [ ] Each object follows object rules
- [ ] No trailing `~` at end

✅ **General:**
- [ ] No line breaks in output
- [ ] Special characters properly escaped
- [ ] UTF-8 encoding
- [ ] Empty values represented as `||` or `[|`

---

## Performance Tips

### Token Optimization

**Instead of this (Object):**
```
user[name[John|user[age[30|user[city[NYC~
```

**Use this (Table if multiple users):**
```
name|age|city~John|30|NYC
```

**Or this (Object with clean naming):**
```
name[John|age[30|city[NYC~
```

### Choosing Between Formats

| Items Count | Same Structure | Best Format | Why |
|-------------|----------------|-------------|-----|
| 1 item | N/A | **Object** | Most readable |
| 2-10 items | Yes | **Table** | Headers amortize |
| 2-10 items | No | **Array** | Flexibility |
| 10+ items | Yes | **Table** | Best compression |
| 10+ items | No | **Array** | Clear structure |

---

## Common Mistakes ❌

### ❌ Wrong: Mixing separators
```
name|John|age|30~    ← Missing [  after properties
```

### ✅ Correct:
```
name[John|age[30~     ← Properties have [
```

---

### ❌ Wrong: Not ending object with ~
```
name[John|age[30|     ← Missing ~ at end
```

### ✅ Correct:
```
name[John|age[30~     ← Ends with ~
```

---

### ❌ Wrong: Using true/false
```
active[true|          ← Should use ^1
```

### ✅ Correct:
```
active[^1|            ← Boolean as ^1
```

---

### ❌ Wrong: Array without {
```
users[id[1|name[John  ← Missing {
```

### ✅ Correct:
```
users{id[1|name[John  ← Array starts with { (single object, no ~ at end)
```

---

**Master these patterns and you'll be encoding SLD like a pro!** 🚀
