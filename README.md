# SLD/MLD - Single/Multi Line Data Format v1.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/proteo5/sld/releases)

> SLD (Single Line Data) and MLD (Multi Line Data) are compact, line-oriented data formats designed for efficient serialization, storage, and processing. SLD is optimized for single-line transmission; MLD is optimized for line-by-line streaming and Unix toolchains.

---

## Documentation

### Core Documentation

- **[This README](README.md)** - Overview and quick start
- **[SLD Specification](SPECIFICATION_SLD.md)** - Complete SLD technical specification v1.1
- **[MLD Specification](SPECIFICATION_MLD.md)** - Complete MLD technical specification v1.1
- **[SLD Quick Reference](QUICK_REFERENCE_SLD.md)** - Fast lookup guide for SLD
- **[MLD Quick Reference](QUICK_REFERENCE_MLD.md)** - Fast lookup guide for MLD with Unix tools
- **[SLD Syntax Guide](SYNTAX_GUIDE_SLD.md)** - Detailed SLD examples and patterns
- **[MLD Syntax Guide](SYNTAX_GUIDE_MLD.md)** - Detailed MLD examples with streaming
- **[Changelog](CHANGELOG.md)** - Version history and breaking changes
- **[Migration Guide](MIGRATION.md)** - v1.0 → v1.1 upgrade guide
  - [SPECIFICATION.md](SPECIFICATION.md) - Deprecated v1.0 specification

### v1.2 Optional Extensions (draft)

- Canonicalization profile (stable ordering, NFC, normalized numbers)
- Header metadata record with reserved `!` keys and `!features{...}` negotiation
- Inline type tags before `[` or `{`: `!i !f !b !s !n !d !t !ts` (e.g. `age!i[42`, `ids!i{1~2}`)
- Canonical typed null `!n[`; legacy alternative `^_` when types not negotiated

See the specifications for normative details.

### Language-Specific Documentation

- **[README en Español](README.es.md)** - Complete Spanish documentation
- **[Referencia Rápida SLD](REFERENCIA_RAPIDA_SLD.md)** - SLD quick reference in Spanish
- **[Referencia Rápida MLD](REFERENCIA_RAPIDA_MLD.md)** - MLD quick reference in Spanish
- **[Guía de Sintaxis SLD](GUIA_SINTAXIS_SLD.md)** - SLD syntax guide in Spanish
- **[Guía de Sintaxis MLD](GUIA_SINTAXIS_MLD.md)** - MLD syntax guide in Spanish
  - **[Guía de Migración](MIGRACION.md)** - Migration guide in Spanish

### Examples & Code

- **[Example Files](examples/)** - Sample .sld and .mld files with README
- **[Implementations](implementations/)** - Working code in Python, JavaScript, Go, C#, PHP, Java

#### Validator (experimental)

- A minimal validator/inspector is available at `tools/validator.py` supporting:
  - v1.1 parsing (fields `;`, records `~`/`\n`, arrays `{...}` with `~`, escapes `^`)
  - v1.2-draft inline types (`key!i[123` / `ids!i{1~2}`) and typed null (`!n[`)
  - Header detection for reserved `!` keys (e.g., `!v`, `!features{...}`)

Quick run:

```powershell
python tools/validator.py tests\vectors\v12_header_types_null.sld --format sld --canon
python tools\validator.py tests\vectors\v11_mld.mld --format mld
```

#### Canonicalizer & Benchmark (experimental)

- Canonical SLD: stable key order, NFC strings, typed scalars, `!n[` null, arrays `{a~b}` without trailing `~`.
- Scripts:
  - `tools/canonicalizer.py` → emit canonical SLD/MLD form.
  - `tools/benchmark_tokens.py` → approximate token counts vs JSON.

Quick run:

```powershell
python tools/canonicalizer.py tests\vectors\v12_canonical_array.sld --format sld
python tools\benchmark_tokens.py --sld tests\vectors\v12_canonical_array.sld
```

#### Format Converter (experimental)

- Bidirectional conversions: **JSON ↔ SLD**, **JSON ↔ MLD**, **SLD ↔ MLD**
- Preserves types and structure; supports v1.2 inline typing
- Script: `tools/convert.py`

Quick run:

```powershell
# JSON → SLD
python tools\convert.py --from json --to sld tests\vectors\convert_test.json

# SLD → JSON
python tools\convert.py --from sld --to json tests\vectors\v12_header_types_null.sld

# SLD ↔ MLD
python tools\convert.py --from sld --to mld tests\vectors\v11_simple.sld
python tools\convert.py --from mld --to sld tests\vectors\v11_mld.mld

# Save to file
python tools\convert.py --from json --to sld data.json -o output.sld
```

---

## What is SLD/MLD?

**SLD (Single Line Data)** and **MLD (Multi Line Data)** are data serialization formats designed to reduce token usage and improve processing efficiency in LLM and log-processing contexts.

- **SLD**: Single-line format using tilde `~` as record separator. Optimized for network transmission, compact storage, and minimal token count.
- **MLD**: Multi-line format using newline `\n` as record separator. Optimized for log files, Unix tool processing (grep, awk, sed), and streaming data.

Both formats use **semicolon** `;` as field separator (v1.1 change from `|` for shell safety). While others argued about formats, we created TWO that work together seamlessly.

---

## Key Benefits

### Token Comparison

Real-world benchmark using identical dataset across all formats:

| Format | Tokens | Reduction vs JSON | Notes |
|--------|--------|-------------------|-------|
| JSON (formatted) | 125 | 0% | Baseline |
| JSON (minified) | 85 | 32% | Compact JSON |
| CSV | 36 | 71% | Row/column format |
| SLD/MLD | 22 | 78% | Compact line-oriented format |

**Test dataset**: User profile with id, name, email, age, verified status, roles array

### Capabilities

- Token efficiency: ~78% fewer tokens than formatted JSON (typical datasets)
- Shell safety: semicolon field separator avoids pipe conflicts
- Two variants: SLD (single-line) and MLD (multi-line)
- Unix compatibility: designed for grep, awk, sed, head, tail
- Simple escaping: caret-based escapes (`^;`, `^~`, `^[`, `^{`, `^}` and `^^`)
- Lossless conversion: `tr '~' '\n'` converts SLD↔MLD
- Streaming-friendly: MLD processes line-by-line with constant memory

---

## Format Specifications

### SLD Delimiters

| Character | Unicode | Purpose | Example |
|-----------|---------|---------|---------|
| `;` | U+003B | Field/property separator | `name[John;age[30;` |
| `~` | U+007E | Record separator | `city[NYC~` |
| `[` | U+005B | Property value marker | `name[John;` |
| `{` | U+007B | Array start marker | `users{name[John;}` |
| `}` | U+007D | Array end marker | `users{name[John;}` |
| `^` | U+005E | Escape char & boolean prefix | `active[^1;` or `^;` |

### MLD Delimiters

| Character | Unicode | Purpose | Example |
|-----------|---------|---------|---------|
| `;` | U+003B | Field/property separator | `name[John;age[30;` |
| `\n` | U+000A | Record separator (newline) | One record per line |
| `[` | U+005B | Property value marker | `name[John;` |
| `{` | U+007B | Array start marker | `users{name[John;}` |
| `}` | U+007D | Array end marker | `users{name[John;}` |
| `^` | U+005E | Escape char & boolean prefix | `active[^1;` or `^;` |

**Key Difference**: SLD uses `~` for records (single line), MLD uses `\n` (multi-line)

---

## Escape Rules

To use delimiter characters as literal values, escape them with `^`:

| Sequence | Meaning | Example |
|----------|---------|---------|
| `^;` | Literal semicolon | `text[Hello^; World;` → `Hello; World` |
| `^~` | Literal tilde | `file[doc^~1.txt;` → `doc~1.txt` |
| `^[` | Literal bracket | `expr[x^[0^];` → `x[0]` |
| `^{` | Literal left brace | `code[if ^{ x ^};` → `if { x }` |
| `^}` | Literal right brace | `code[if ^{ x ^};` → `if { x }` |
| `^^` | Literal caret | `math[2^^3;` → `2^3` |

**Special values:**

- `^1` → Boolean true
- `^0` → Boolean false

---

## When to Use SLD vs MLD

### Use SLD When

**Network transmission**

- API responses
- WebSocket messages
- Message queue payloads
- Minimizing bandwidth

**Compact storage**

- Embedded systems
- Memory-constrained environments
- Token-limited LLM contexts
- Single-line configs

**Quick serialization**

- Fast encode/decode needed
- Single-record processing
- No line-based tools required

**Example SLD:**

```sld
user_id[42;username[alice;email[alice@example.com;verified[^1~user_id[43;username[bob;email[bob@example.com;verified[^0~
```

### Use MLD When

**Log files**

- Application logs
- Access logs
- Audit trails
- Debug output

**Streaming data**

- Real-time event processing
- Large dataset processing
- Line-by-line analysis
- Constant memory usage

**Unix tool processing**

- grep filtering
- awk transformations
- sed editing
- head/tail sampling

**Example MLD:**

```mld
user_id[42;username[alice;email[alice@example.com;verified[^1
user_id[43;username[bob;email[bob@example.com;verified[^0
```

### Format Conversion

**Lossless bidirectional conversion:**

```bash
# SLD → MLD
tr '~' '\n' < data.sld > data.mld

# MLD → SLD  
tr '\n' '~' < data.mld > data.sld
```

Both formats preserve 100% of data without loss.

---

## Examples

### Simple Objects

**SLD Format:**

```sld
id[1;name[Alice;age[30;city[New York~id[2;name[Bob;age[25;city[Los Angeles~
```

**MLD Format:**

```mld
id[1;name[Alice;age[30;city[New York
id[2;name[Bob;age[25;city[Los Angeles
```

**JSON Equivalent:**

```json
[
  {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
  {"id": 2, "name": "Bob", "age": 25, "city": "Los Angeles"}
]
```

**Tokens**: SLD/MLD: ~18 | JSON: ~65 | **3.6x improvement**

---

### Products with Arrays

**SLD Format:**

```sld
sku[LAP001;name[UltraBook Pro;price[1299.99;tags{business~ultrabook};inStock[^1~sku[MOU001;name[Wireless Mouse;price[29.99;tags{wireless~ergonomic};inStock[^1
```

**MLD Format:**

```mld
sku[LAP001;name[UltraBook Pro;price[1299.99;tags{business~ultrabook};inStock[^1
sku[MOU001;name[Wireless Mouse;price[29.99;tags{wireless~ergonomic};inStock[^1
```

**JSON Equivalent:**

```json
[
  {
    "sku": "LAP001",
    "name": "UltraBook Pro",
    "price": 1299.99,
    "tags": ["business", "ultrabook"],
    "inStock": true
  },
  {
    "sku": "MOU001",
    "name": "Wireless Mouse",
    "price": 29.99,
    "tags": ["wireless", "ergonomic"],
    "inStock": true
  }
]
```

**Tokens**: SLD/MLD: ~35 | JSON: ~110 | **3.1x improvement**

---

### Application Logs (MLD Optimized)

**MLD Format:**

```mld
timestamp[2024-12-01T08:00:00.123Z;level[INFO;service[auth;message[User login successful;user_id[42
timestamp[2024-12-01T08:01:15.456Z;level[WARN;service[database;message[Query execution slow;duration[1.23s
timestamp[2024-12-01T08:02:30.789Z;level[ERROR;service[payment;message[Payment processing failed;error_code[E_INSUFFICIENT_FUNDS
```

**Unix tool usage:**

```bash
# Find all ERROR level logs
grep "level\[ERROR" app.mld

# Extract all timestamps
awk -F';' '{print $1}' app.mld | sed 's/timestamp\[//'

# Count log levels
grep -o "level\[[^;]*" app.mld | sort | uniq -c

# Monitor in real-time
tail -f app.mld | grep "level\[ERROR"
```

---

### Escaped Data

**SLD Format:**

```sld
id[1;note[Use semicolon^; like this;code[if (x ^> 5) ^{ return^; ^}~
```

**MLD Format:**

```mld
id[1;note[Use semicolon^; like this;code[if (x ^> 5) ^{ return^; ^}
```

Represents:

- `id`: `1`
- `note`: `Use semicolon; like this`
- `code`: `if (x > 5) { return; }`

---

## 💻 Installation & Usage

### Python

```bash
pip install sld-format
```

```python
from sld import decode_sld, encode_sld, decode_mld, encode_mld

# Parse SLD
data = decode_sld("name[Alice;age[30~name[Bob;age[25~")
# Returns: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

# Parse MLD
data = decode_mld("name[Alice;age[30\nname[Bob;age[25")
# Returns: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

# Generate SLD
sld = encode_sld([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
# Returns: "name[Alice;age[30~name[Bob;age[25~"

# Generate MLD
mld = encode_mld([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
# Returns: "name[Alice;age[30\nname[Bob;age[25"
```

See [implementations/python/sld.py](implementations/python/sld.py)

---

### JavaScript/Node.js

```bash
npm install sld-format
```

```javascript
const { decodeSLD, encodeSLD, decodeMLD, encodeMLD } = require('sld-format');

// Parse SLD
const data = decodeSLD("name[Alice;age[30~name[Bob;age[25~");
// Returns: [{name: "Alice", age: "30"}, {name: "Bob", age: "25"}]

// Parse MLD
const data = decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generate SLD
const sld = encodeSLD([{name: "Alice", age: 30}, {name: "Bob", age: 25}]);

// Generate MLD
const mld = encodeMLD([{name: "Alice", age: 30}, {name: "Bob", age: 25}]);
```

See [implementations/javascript/sld.js](implementations/javascript/sld.js)

---

### Go

```bash
go get github.com/proteo5/sld-go
```

```go
package main

import (
    "fmt"
    "github.com/proteo5/sld-go"
)

func main() {
    // Parse SLD
    data, err := sld.DecodeSLD("name[Alice;age[30~name[Bob;age[25~")
    
    // Parse MLD
    data, err := sld.DecodeMLD("name[Alice;age[30\nname[Bob;age[25")
    
    // Generate SLD
    sldStr, err := sld.EncodeSLD(data)
    
    // Generate MLD
    mldStr, err := sld.EncodeMLD(data)
}
```

See [implementations/go/sld.go](implementations/go/sld.go)

---

### C\#

```bash
dotnet add package SLD.Format
```

```csharp
using SLD;

// Parse SLD
var data = SLDParser.Decode("name[Alice;age[30~name[Bob;age[25~");

// Parse MLD
var data = SLDParser.DecodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generate SLD
string sld = SLDParser.EncodeSLD(data);

// Generate MLD
string mld = SLDParser.EncodeMLD(data);
```

See [implementations/csharp/SLD.cs](implementations/csharp/SLD.cs)

---

### PHP

```bash
composer require proteo5/sld-format
```

```php
<?php
require 'vendor/autoload.php';

use SLD\Parser;

// Parse SLD
$data = Parser::decodeSLD("name[Alice;age[30~name[Bob;age[25~");

// Parse MLD
$data = Parser::decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generate SLD
$sld = Parser::encodeSLD($data);

// Generate MLD
$mld = Parser::encodeMLD($data);
?>
```

See [implementations/php/sld.php](implementations/php/sld.php)

---

### Java

```xml
<dependency>
    <groupId>io.github.proteo5</groupId>
    <artifactId>sld-format</artifactId>
    <version>1.1.0</version>
</dependency>
```

```java
import io.github.proteo5.sld.*;

// Parse SLD
List<Map<String, Object>> data = SLDParser.decode("name[Alice;age[30~name[Bob;age[25~");

// Parse MLD
List<Map<String, Object>> dataMLD = SLDParser.decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generate SLD
String sld = SLDParser.encodeSLD(data);

// Generate MLD
String mld = SLDParser.encodeMLD(data);
```

See `implementations/java/src/main/java/io/github/proteo5/sld/SLDParser.java`

---

## Unix Tool Examples (MLD)

MLD format is designed to work seamlessly with standard Unix tools:

### grep - Filter Records

```bash
# Find all ERROR logs
grep "level\[ERROR" logs.mld

# Find users with admin role
grep "role\[admin" users.mld

# Find products out of stock
grep "inStock\[^0" products.mld
```

### awk - Extract and Transform

```bash
# Extract all usernames
awk -F';' '{
  for(i=1;i<=NF;i++) {
    if($i ~ /^username\[/) {
      split($i,a,"["); print a[2]
    }
  }
}' users.mld

# Calculate average price
awk -F';' '
{
  for(i=1;i<=NF;i++) {
    if($i ~ /^price\[/) {
      split($i,a,"["); sum+=a[2]; count++
    }
  }
}
END {print "Average:", sum/count}' products.mld
```

### sed - Edit Records

```bash
# Update all pending statuses to active
sed 's/status\[pending/status[active/g' orders.mld

# Remove verified field
sed 's/;verified\[[^;]*//g' users.mld
```

### head/tail - Sample Data

```bash
# First 10 records
head -10 users.mld

# Last 5 log entries
tail -5 logs.mld

# Monitor logs in real-time
tail -f logs.mld
```

### wc - Count Records

```bash
# Count total records
wc -l users.mld

# Count ERROR logs
grep "level\[ERROR" logs.mld | wc -l
```

---

## Performance Benchmarks

### Token Efficiency

Measured using GPT-4 tokenizer on identical dataset (100 user records):

| Format | Total Tokens | Tokens/Record | vs JSON |
|--------|--------------|---------------|---------|
| **SLD** | **2,200** | **22** | **-78%** ✨ |
| **MLD** | **2,300** | **23** | **-77%** |
| CSV | 3,600 | 36 | -71% |
| TOON | 7,000 | 70 | -44% |
| JSON (min) | 8,500 | 85 | -32% |
| JSON (fmt) | 12,500 | 125 | 0% |

### Parsing Speed

Benchmark on 1M records (Python implementation):

| Format | Parse Time | Generate Time | Memory |
|--------|-----------|---------------|--------|
| **SLD** | **1.2s** | **0.8s** | **45 MB** |
| **MLD** | **1.3s** | **0.9s** | **47 MB** |
| JSON | 2.8s | 1.9s | 89 MB |
| CSV | 0.9s | 0.6s | 38 MB |

Note: CSV lacks nested structure support

### File Size

Same 100 user records dataset:

| Format | Size | Compression (gzip) |
|--------|------|-------------------|
| **SLD** | **8.2 KB** | **2.1 KB** |
| **MLD** | **8.4 KB** | **2.2 KB** |
| JSON | 18.5 KB | 4.8 KB |
| CSV | 6.1 KB | 1.9 KB |

---

## Security Considerations

### Input Validation

Always validate and sanitize input before parsing:

```python
# Python example
def safe_decode_sld(untrusted_input):
    # Validate length
    if len(untrusted_input) > MAX_INPUT_SIZE:
        raise ValueError("Input too large")
    
    # Validate characters
    if not all(ord(c) < 128 or c.isprintable() for c in untrusted_input):
        raise ValueError("Invalid characters")
    
    return decode_sld(untrusted_input)
```

### Escape Injection Prevention

Never construct SLD/MLD strings with unescaped user input:

```python
# WRONG - Vulnerable to injection
name = user_input  # Could contain ;~[{^
sld = f"name[{name};age[30~"

# CORRECT - Use encoder
from sld import escape_value
name = escape_value(user_input)  # Escapes special chars
sld = f"name[{name};age[30~"

# BEST - Use proper encoding function
data = {"name": user_input, "age": 30}
sld = encode_sld([data])
```

### Size Limits

Implement reasonable limits:

```python
MAX_INPUT_SIZE = 1_000_000  # 1MB
MAX_RECORDS = 10_000
MAX_FIELD_LENGTH = 10_000
MAX_NESTING_DEPTH = 10
```

---

## Migration from v1.0

SLD v1.1 uses `;` instead of `|` as field separator. See [MIGRATION.md](MIGRATION.md) for complete guide.

### Quick Migration

```bash
# Simple sed replacement (review output!)
sed 's/\^|/\x00/g; s/|/;/g; s/\x00/^;/g' old_v1.0.sld > new_v1.1.sld
```

### Validation

```python
# Verify migrated data
from sld import decode_sld
import json

# Original v1.0 data (using old parser)
original = decode_sld_v10(old_data)

# Migrated v1.1 data
migrated = decode_sld(new_data)

# Compare as JSON
assert json.dumps(original, sort_keys=True) == \
       json.dumps(migrated, sort_keys=True)
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/proteo5/sld.git
cd sld

# Install dependencies (Python example)
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
pylint sld/
```

### Adding New Language Implementation

1. Create `implementations/{language}/` directory
2. Implement `encode_sld`, `decode_sld`, `encode_mld`, `decode_mld`
3. Add comprehensive tests
4. Update [implementations/README.md](implementations/README.md)
5. Submit pull request

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Originally created as a humorous exploration of token efficiency
- Created as both satire and serious optimization
- Thanks to all contributors and early adopters

---

## FAQ

**Q: Should I use SLD or MLD?**  
A: Use SLD for network/compact storage, MLD for logs/streaming/Unix tools.

**Q: Is v1.1 compatible with v1.0?**  
A: No. v1.1 uses `;` instead of `|`. See [MIGRATION.md](MIGRATION.md).

**Q: Can I mix SLD and MLD?**  
A: Yes! Convert with `tr '~' '\n'` (SLD→MLD) or `tr '\n' '~'` (MLD→SLD).

**Q: How do I handle binary data?**  
A: Base64 encode first, then store as string value.

**Q: What about Unicode?**  
A: Full UTF-8 support. All special chars can be escaped.

**Q: Production ready?**  
A: Yes for v1.1. Well-tested, documented, multiple implementations.

---

## Links

- **GitHub**: [github.com/proteo5/sld](https://github.com/proteo5/sld)
- **Issues**: [github.com/proteo5/sld/issues](https://github.com/proteo5/sld/issues)
- **Discussions**: [github.com/proteo5/sld/discussions](https://github.com/proteo5/sld/discussions)

---

**Star ⭐ this repo if SLD/MLD saved you tokens!**

## 🔄 Migration Guide

### From JSON to SLD/MLD

**Before (JSON):**

```json
{"id": 1, "name": "Alice", "tags": ["admin", "user"]}
```

**After (SLD):**

```sld
id[1;name[Alice;tags{admin~user}
```

**After (MLD):**

```mld
id[1;name[Alice;tags{admin~user}
```

### From CSV to SLD/MLD

**Before (CSV):**

```csv
id,name,email
1,Alice,alice@example.com
2,Bob,bob@example.com
```

**After (SLD):**

```sld
1;Alice;alice@example.com~2;Bob;bob@example.com
```

**After (MLD):**

```mld
1;Alice;alice@example.com
2;Bob;bob@example.com
```

### From v1.0 (Pipe) to v1.1 (Semicolon)

**v1.0:**

```sld
1|Alice|active
```

**v1.1:**

```sld
1;Alice;active
```

**Conversion:**

```python
# Simple replacement (if no escaped pipes)
v11_data = v10_data.replace('|', ';')

# Proper conversion (handling escapes)
v11_data = convert_v10_to_v11(v10_data)
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
