# SLD Examples

This directory contains various SLD format examples.

## Files

### simple.sld
Basic table data with products and prices.

**Equivalent JSON:**
```json
[
  {"name": "Laptop", "price": 3999.90},
  {"name": "Mouse", "price": 149.90},
  {"name": "Headset", "price": 499.00}
]
```

**Note:** First row contains headers (name|price), subsequent rows contain data.

### objects.sld
Array of user objects with multiple fields.

**Equivalent JSON:**
```json
{
  "users": [
    {"id": 1, "name": "John", "lastname": "Smith"},
    {"id": 2, "name": "Juan", "lastname": "Perez"}
  ]
}
```

**Note:** Uses `{` to denote array start, properties use `property[value|` format.

### complex.sld
Nested structure with a products array including boolean values.

**Equivalent JSON:**
```json
{
  "products": [
    {"id": 1, "name": "Laptop", "price": 3999.90, "inStock": true},
    {"id": 2, "name": "Mouse", "price": 149.90, "inStock": false},
    {"id": 3, "name": "Headset", "price": 499.00, "inStock": true}
  ]
}
```

**Note:** Booleans are represented as `^1` (true) and `^0` (false).

### escaped.sld
Demonstrates escape sequences for delimiter characters.

**Equivalent JSON:**
```json
[
  {"company": "Pipe|Works Inc"},
  {"product": "Model~XZ~2000"},
  {"email": "user^admin@example.com"}
]
```

Note: The literal characters `|`, `~`, and `^` in the data are escaped as `^|`, `^~`, and `^^`.
