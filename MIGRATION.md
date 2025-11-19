# Migration Guide: SLD v1.0 → v2.0

This guide helps you migrate from SLD v1.0 (using `|` delimiter) to v2.0 (using `;` delimiter) and choose between SLD and MLD formats.

## Table of Contents

- [Breaking Changes](#breaking-changes)
- [Why Migrate?](#why-migrate)
- [Migration Steps](#migration-steps)
- [Format Selection](#format-selection)
- [Conversion Tools](#conversion-tools)
- [Validation](#validation)
- [Implementation Updates](#implementation-updates)
- [FAQ](#faq)

## Breaking Changes

### ⚠️ v2.0 is NOT backward compatible with v1.0

**Primary Change: Field Separator**
- v1.0: `|` (pipe, U+007C)
- v2.0: `;` (semicolon, U+003B)

**Escape Sequences Updated:**
- v1.0: `^|` for literal pipe
- v2.0: `^;` for literal semicolon

**New Format Added:**
- MLD (Multi Line Data) with newline record separator

## Why Migrate?

### 1. Shell Safety
The pipe character `|` is a command separator in Unix shells:

```bash
# v1.0 - DANGEROUS
echo "name[Alice|age[30~" | grep age  # Creates pipeline!

# v2.0 - SAFE
echo "name[Alice;age[30~" | grep age  # Works correctly
```

### 2. Terminal Compatibility
Semicolon requires less escaping in interactive shells:

```bash
# v1.0
DATA="name[Alice\|age[30~"  # Must escape pipe

# v2.0
DATA="name[Alice;age[30~"   # No escaping needed in most shells
```

### 3. Unix Tool Integration
MLD format enables powerful Unix tool usage:

```bash
# Filter log files
grep "level[ERROR" app.mld

# Count records
wc -l users.mld

# Monitor in real-time
tail -f logs.mld
```

### 4. Streaming Support
MLD allows constant-memory processing:

```bash
# Process million-line file with constant memory
while IFS= read -r record; do
  # Process each record
  echo "$record"
done < huge_dataset.mld
```

## Migration Steps

### Step 1: Backup Your Data

```bash
# Create backup
cp data.sld data.sld.v1.0.backup
```

### Step 2: Manual Conversion

**⚠️ Automatic conversion is NOT recommended** due to ambiguity between escaped and unescaped delimiters.

**Required changes:**

1. Replace unescaped `|` → `;`
2. Replace `^|` → `^;`

**Example:**

```
# v1.0
name[John Doe|email[john@example.com|note[Use | symbol here: ^|~

# v2.0
name[John Doe;email[john@example.com;note[Use ; symbol here: ^;~
```

### Step 3: Choose Format (SLD or MLD)

See [Format Selection](#format-selection) section below.

### Step 4: Validate

Parse with v2.0 decoder and verify:

```python
# Python validation
from sld import decode_sld

try:
    data = decode_sld(your_converted_string)
    print("✓ Valid SLD v2.0")
except Exception as e:
    print(f"✗ Invalid: {e}")
```

## Format Selection

### Use SLD When:

✅ **Network Transmission**
- API responses
- WebSocket messages
- Message queue payloads

✅ **Compact Storage**
- Embedded systems
- Memory-constrained environments
- Token-limited LLM contexts

✅ **Single-Record Processing**
- Configuration files
- Small datasets
- Quick serialization

**Example:**
```
user_id[42;username[alice;email[alice@example.com;verified[^1~
```

### Use MLD When:

✅ **Log Files**
- Application logs
- Access logs
- Audit trails

✅ **Streaming Data**
- Real-time event processing
- Large dataset processing
- Line-by-line analysis

✅ **Unix Tool Processing**
- grep filtering
- awk transformations
- sed editing
- head/tail sampling

**Example:**
```
timestamp[2024-12-01T10:00:00Z;level[INFO;message[User login
timestamp[2024-12-01T10:01:00Z;level[ERROR;message[Auth failed
timestamp[2024-12-01T10:02:00Z;level[INFO;message[User logout
```

### Conversion Between SLD and MLD

**Lossless bidirectional conversion:**

```bash
# SLD → MLD
tr '~' '\n' < data.sld > data.mld

# MLD → SLD
tr '\n' '~' < data.mld > data.sld
```

**Note:** Both commands preserve all data without loss.

## Conversion Tools

### Bash Script

```bash
#!/bin/bash
# convert_v10_to_v11.sh

if [ $# -ne 2 ]; then
  echo "Usage: $0 <input_v1.0.sld> <output_v2.0.sld>"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

# WARNING: This simple replacement may not handle all edge cases
# Manual review is STRONGLY recommended

sed 's/\^|/\x00/g' "$INPUT" | \  # Temporarily replace ^|
  sed 's/|/;/g' | \                # Replace all remaining |
  sed 's/\x00/^;/g' \              # Restore as ^;
  > "$OUTPUT"

echo "Conversion complete. MANUALLY REVIEW $OUTPUT before use!"
```

### Python Script

```python
#!/usr/bin/env python3
# convert_v10_to_v11.py

import re
import sys

def convert_v10_to_v11(v10_string):
    """Convert SLD v1.0 to v2.0 format."""
    # This is a SIMPLISTIC conversion
    # Manual review required for production data
    
    result = []
    i = 0
    while i < len(v10_string):
        if v10_string[i:i+2] == '^|':
            # Escaped pipe becomes escaped semicolon
            result.append('^;')
            i += 2
        elif v10_string[i] == '|':
            # Unescaped pipe becomes semicolon
            result.append(';')
            i += 1
        else:
            result.append(v10_string[i])
            i += 1
    
    return ''.join(result)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 convert_v10_to_v11.py <input.sld> <output.sld>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        v10_data = f.read()
    
    v11_data = convert_v10_to_v11(v10_data)
    
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(v11_data)
    
    print(f"Converted {sys.argv[1]} → {sys.argv[2]}")
    print("⚠️  MANUALLY REVIEW output before production use!")
```

## Validation

### Pre-Migration Checklist

- [ ] Backed up all v1.0 data
- [ ] Identified all SLD files in project
- [ ] Reviewed escape sequences in data
- [ ] Tested conversion on sample data
- [ ] Updated parser libraries to v2.0

### Post-Migration Validation

```python
# Validate data integrity
import json
from sld_v10 import decode_sld as decode_v10
from sld_v11 import decode_sld as decode_v11

# Read original and converted
with open('data.v1.0.sld') as f:
    original = decode_v10(f.read())

with open('data.v2.0.sld') as f:
    converted = decode_v11(f.read())

# Compare as JSON
assert json.dumps(original, sort_keys=True) == \
       json.dumps(converted, sort_keys=True), \
       "Data mismatch after conversion!"

print("✓ Validation passed - data integrity preserved")
```

### Common Issues

**Issue 1: Semicolons in data**
```
# v1.0
text[Hello; World|author[Alice~

# v2.0 - WRONG
text[Hello; World;author[Alice~  # Semicolon breaks parsing!

# v2.0 - CORRECT
text[Hello^; World;author[Alice~  # Escape the semicolon
```

**Issue 2: Shell escaping**
```bash
# v2.0 - May need escaping in some contexts
echo 'data[value;next[value'  # Single quotes = safe
echo "data[value;next[value"  # Double quotes = safe
echo data[value;next[value    # No quotes = may need escaping
```

**Issue 3: Mixed formats**
```
# Don't mix SLD and MLD delimiters
name[Alice;age[30~next[Bob  # SLD - OK (uses ~)
name[Alice;age[30           # MLD - OK (newline ends record)
name[Alice;age[30~          # Mixed - WRONG
```

## Implementation Updates

### Update Field Separator Constant

```python
# v1.0
FIELD_SEPARATOR = '|'

# v2.0
FIELD_SEPARATOR = ';'
```

```javascript
// v1.0
const FIELD_SEPARATOR = '|';

// v2.0
const FIELD_SEPARATOR = ';';
```

### Add MLD Support

```python
# New MLD functions
def encode_mld(records):
    """Encode records to MLD format (newline-separated)."""
    return '\n'.join(encode_sld_record(r) for r in records)

def decode_mld(mld_string):
    """Decode MLD format."""
    return [decode_sld_record(line) for line in mld_string.split('\n') if line]
```

### Update Tests

```python
# Update all test cases
def test_encode_object_v11():
    data = {"name": "Alice", "age": 30}
    result = encode_sld(data)
    assert result == "name[Alice;age[30~"  # Not name[Alice|age[30~
```

## FAQ

### Q: Can I automatically convert v1.0 to v2.0?

**A:** Not safely. The conversion scripts provided are **helpers only**. Manual review is essential because:

1. Data may contain unescaped semicolons that need escaping
2. Escaped pipes (`^|`) must become escaped semicolons (`^;`)
3. Context-dependent edge cases exist

### Q: Should I use SLD or MLD for my use case?

**A:** 
- **SLD**: Network APIs, compact storage, single-record configs
- **MLD**: Log files, streaming data, Unix tool processing

Both are interconvertible, so you can use both in different contexts.

### Q: Will v1.0 parsers work with v2.0 data?

**A:** No. v1.0 parsers expect `|` delimiters and will fail on `;` delimiters.

### Q: Will v2.0 parsers work with v1.0 data?

**A:** No. v2.0 parsers expect `;` delimiters and will fail on `|` delimiters.

### Q: How do I handle existing APIs using v1.0?

**A:** Three strategies:

1. **Breaking change**: Update API to v2.0, version endpoint (e.g., `/api/v2/`)
2. **Dual support**: Accept both formats, detect version, deprecate v1.0
3. **Gateway conversion**: Convert v1.0→v2.0 at API boundary

### Q: What about performance impact?

**A:** Negligible. Semicolon vs pipe has no performance difference. MLD may be slightly slower for single-record parsing but much faster for streaming.

### Q: Can I mix SLD and MLD in the same application?

**A:** Yes! Common pattern:
- **Receive**: SLD over network
- **Process**: Convert to MLD for processing
- **Store**: MLD in log files
- **Transmit**: Convert back to SLD for responses

## Resources

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Complete SLD v2.0 specification
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Complete MLD v2.0 specification  
- [CHANGELOG.md](CHANGELOG.md) - Detailed version history
- [examples/](examples/) - Example files in both formats
- [implementations/](implementations/) - Reference implementations

## Support

- **Issues**: [GitHub Issues](https://github.com/proteo5/sld/issues)
- **Discussions**: [GitHub Discussions](https://github.com/proteo5/sld/discussions)

---

**Migration Checklist:**

- [ ] Read this entire guide
- [ ] Back up all v1.0 data
- [ ] Choose SLD or MLD for each use case
- [ ] Convert data (manually review!)
- [ ] Update parser libraries
- [ ] Update application code
- [ ] Update tests
- [ ] Validate data integrity
- [ ] Deploy with versioned API endpoints
- [ ] Monitor for issues
- [ ] Deprecate v1.0 support

**Happy migrating! 🚀**

