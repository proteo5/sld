# SLD/MLD Examples

This directory contains example files demonstrating the SLD (Single Line Data) and MLD (Multi Line Data) formats.

## Directory Structure

```
examples/
├── sld/          # Single Line Data examples
│   ├── simple.sld
│   ├── products.sld
│   ├── users.sld
│   ├── escaped.sld
│   ├── complex.sld
│   ├── logs.sld
│   └── config.sld
│
└── mld/          # Multi Line Data examples
    ├── simple.mld
    ├── products.mld
    ├── users.mld
    ├── escaped.mld
    ├── complex.mld
    ├── logs.mld
    └── config.mld
```

## Example Files

### simple.sld / simple.mld
Basic records with simple properties (id, name, age, city).

**Use case:** Learning the format, basic data storage

### products.sld / products.mld
Product catalog with SKUs, prices, stock status, and tags.

**Use case:** E-commerce applications, inventory management

### users.sld / users.mld
User profiles with authentication info, roles, and metadata.

**Use case:** User management systems, authentication databases

### escaped.sld / escaped.mld
Examples demonstrating escape sequences for special characters.

**Use case:** Understanding how to handle semicolons, brackets, and other delimiters in data

### complex.sld / complex.mld
Complex transactions with nested items, addresses, and multiple properties.

**Use case:** Order processing, complex data structures, nested objects

### logs.sld / logs.mld
Application logs with timestamps, levels, services, and messages.

**Use case:** Log aggregation, monitoring, debugging

### config.sld / config.mld
Application configuration with various settings and feature flags.

**Use case:** Configuration management, environment settings

## Converting Between Formats

### SLD to MLD
```bash
tr '~' '\n' < examples/sld/simple.sld > examples/mld/simple.mld
```

### MLD to SLD
```bash
tr '\n' '~' < examples/mld/simple.mld > examples/sld/simple.sld
```

## Processing Examples

### Using grep (MLD only)
```bash
# Find all ERROR level logs
grep "level\[ERROR" examples/mld/logs.mld

# Find products in stock
grep "inStock\[^1" examples/mld/products.mld

# Find admin users
grep "role\[admin" examples/mld/users.mld
```

### Using awk (MLD)
```bash
# Extract all usernames
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^username\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}' examples/mld/users.mld

# Calculate average price
awk -F';' '
{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^price\[/) {
      split($i, arr, "[")
      sum += arr[2]
      count++
    }
  }
}
END {
  if (count > 0) print "Average price:", sum/count
}' examples/mld/products.mld
```

### Using sed (MLD)
```bash
# Update all pending statuses to active
sed 's/status\[pending/status[active/g' examples/mld/complex.mld

# Remove deleted users
sed '/deleted\[^1/d' examples/mld/users.mld
```

### Using head/tail (MLD)
```bash
# First 3 records
head -3 examples/mld/users.mld

# Last 2 log entries
tail -2 examples/mld/logs.mld

# Monitor logs in real-time (if appending)
tail -f examples/mld/logs.mld
```

## Parsing Examples

### Python
```python
def decode_mld_file(filename):
    records = []
    with open(filename, 'r') as f:
        for line in f:
            record = {}
            for prop in line.strip().split(';'):
                if '[' in prop:
                    key, value = prop.split('[', 1)
                    record[key] = value
            records.append(record)
    return records

# Usage
users = decode_mld_file('examples/mld/users.mld')
for user in users:
    print(f"{user['username']}: {user['email']}")
```

### JavaScript
```javascript
const fs = require('fs');

function decodeMLD(filename) {
  const content = fs.readFileSync(filename, 'utf-8');
  return content.trim().split('\n').map(line => {
    const record = {};
    line.split(';').forEach(prop => {
      const [key, value] = prop.split('[');
      if (key && value !== undefined) {
        record[key] = value;
      }
    });
    return record;
  });
}

// Usage
const users = decodeMLD('examples/mld/users.mld');
users.forEach(user => {
  console.log(`${user.username}: ${user.email}`);
});
```

## Validation

### Check for Unescaped Special Characters
```bash
# Find lines with unescaped semicolons (potential issues)
grep -n '[^^];' examples/mld/*.mld

# Find lines with unescaped brackets
grep -n '[^^]\[' examples/mld/*.mld
```

### Count Records
```bash
# SLD (count tildes + 1)
echo $(($(tr -cd '~' < examples/sld/users.sld | wc -c) + 1))

# MLD (count lines)
wc -l examples/mld/users.mld
```

## Performance Testing

### Large File Generation
```bash
# Generate 10,000 user records (MLD)
for i in {1..10000}; do
  echo "user_id[u_$i;username[user$i;email[user$i@example.com;verified[^1;created[2024-01-01T00:00:00Z"
done > examples/mld/users_large.mld

# Convert to SLD
tr '\n' '~' < examples/mld/users_large.mld > examples/sld/users_large.sld
```

### Benchmark Grep vs Full Parse
```bash
# Fast: grep (MLD only)
time grep "username\[user5000" examples/mld/users_large.mld

# Slower: full parse and filter
time python -c "
import sys
for line in open('examples/mld/users_large.mld'):
    if 'username[user5000' in line:
        print(line)
"
```

## Best Practices

1. **Use MLD for logs and streaming data** - Easier to process line-by-line
2. **Use SLD for network transmission** - Single-line format, fewer bytes
3. **Always escape special characters** - Use `^;`, `^[`, `^{`, `^^`
4. **Validate data before encoding** - Check for null values, types
5. **Use Unix tools for MLD** - grep, awk, sed are very efficient
6. **Compress for storage** - Both formats compress well with gzip

## Related Documentation

- [SPECIFICATION_SLD.md](../SPECIFICATION_SLD.md) - SLD format specification
- [SPECIFICATION_MLD.md](../SPECIFICATION_MLD.md) - MLD format specification
- [QUICK_REFERENCE_SLD.md](../QUICK_REFERENCE_SLD.md) - SLD quick reference
- [QUICK_REFERENCE_MLD.md](../QUICK_REFERENCE_MLD.md) - MLD quick reference
- [SYNTAX_GUIDE_SLD.md](../SYNTAX_GUIDE_SLD.md) - Detailed SLD syntax
- [SYNTAX_GUIDE_MLD.md](../SYNTAX_GUIDE_MLD.md) - Detailed MLD syntax
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
