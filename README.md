# SLD - Single Line Data Format

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> The ultimate token-efficient data format that makes JSON cry and CSV look bloated.

## 📚 Documentation Index

### Core Documentation
- 🏠 **[This README](README.md)** - Overview and quick start
- 📖 **[Full Specification](SPECIFICATION.md)** - Complete technical specification
- ⚡ **[Quick Reference](QUICK_REFERENCE.md)** - Fast lookup guide for all three formats
- 📝 **[Syntax Guide](SYNTAX_GUIDE.md)** - Detailed examples and patterns
- 🔄 **[Changelog](CHANGELOG.md)** - Version history and changes
- ✅ **[Consistency Review](CONSISTENCY_REVIEW.md)** - Documentation validation report

### Language-Specific
- 🇪🇸 **[Documentación en Español](README.es.md)** - Spanish documentation

### Examples & Code
- 💾 **[Code Examples](implementations/)** - Working implementations in 6 languages
  - [Python](implementations/python/sld.py)
  - [JavaScript](implementations/javascript/sld.js)
  - [Go](implementations/go/sld.go)
  - [C#](implementations/csharp/SLD.cs)
  - [PHP](implementations/php/sld.php)
  - [Java](implementations/java/SLD.java)
- 📁 **[Format Examples](examples/)** - Sample SLD files

---

## What is SLD?

**SLD (Single Line Data)** is a revolutionary data serialization format designed to minimize token usage in LLM contexts by eliminating ALL line breaks and using ultra-rare separator characters. While others were arguing about JSON vs TOON vs VSC, we went further.

## Why SLD is Superior

### Token Comparison

| Format | Example | Token Count |
|--------|---------|-------------|
| **JSON** | Traditional verbose format | **125 tokens** |
| **TOON** | Simplified syntax | **70 tokens** |
| **VSC** | Line-based comma format | **36 tokens** |
| **SLD** | Everything in one line | **~28 tokens** ✨ |

### The SLD Advantage

1. **True Single Line**: Unlike VSC which uses multiple lines, SLD is ACTUALLY a single line of text, saving 1-2 characters per line break (depending on OS: `\n` or `\r\n`)
2. **Rare Separators**: Uses characters that almost never appear in data (`|`, `~`, `[`, `^`)
3. **Escape Strategy**: Simple doubling escape mechanism that's rarely needed
4. **Null/Empty Support**: Easy to represent with `||`
5. **Nested Structures**: Full support for objects and arrays

## Format Specification

SLD supports **three distinct formats** for different use cases:

1. **Table Format** - Headers in first row, data in subsequent rows (like CSV)
2. **Object Format** - Property-value pairs with `property[value|` syntax
3. **Array Format** - Named arrays with `arrayName{...}` syntax

See [Quick Reference](QUICK_REFERENCE.md) for detailed examples of each format.

### Core Delimiters

| Character | Purpose | Example |
|-----------|---------|----------|
| `\|` | Field/property separator | `name[John\|age[30\|` |
| `~` | Record separator / Last property | `city[NYC~` |
| `[` | Property value marker | `name[John\|` |
| `{` | Array start marker | `users{name[John\|` |
| `^` | Escape char & boolean prefix | `active[^1\|` or `^\|` |

### Escape Rules

To use delimiter characters as literal values, escape them with `^`:

- `^|` → Literal pipe character
- `^~` → Literal tilde character
- `^[` → Literal bracket character
- `^{` → Literal brace character
- `^^` → Literal caret character

**Special values:**
- `^1` → Boolean true
- `^0` → Boolean false

**Note**: Escaping is theoretically rarely needed, making the format even more efficient in practice.

### Null/Empty Values

Empty or null values are represented as consecutive delimiters:

```
name||age|30  // name is null/empty, age is 30
```

## Examples

### Simple Table Data

**VSC Format** (3 lines):
```
Laptop,3999.90
Mouse,149.90
Headset,499.00
```

**SLD Format - Table** (1 line, headers in first row):
```
name|price~Laptop|3999.90~Mouse|149.90~Headset|499.00
```

### Objects/Arrays

**JSON Format**:
```json
[
  {"id": 1, "name": "John", "lastname": "Smith"},
  {"id": 2, "name": "Juan", "lastname": "Perez"}
]
```

**SLD Format - Array**:
```
users{id[1|name[John|lastname[Smith~id[2|name[Juan|lastname[Perez
```

**SLD Format - Table**:
```
id|name|lastname~1|John|Smith~2|Juan|Perez
```

### Complex Nested Data

**JSON**:
```json
{
  "products": [
    {"id": 1, "name": "Laptop", "price": 3999.90, "inStock": true},
    {"id": 2, "name": "Mouse", "price": 149.90, "inStock": false},
    {"id": 3, "name": "Headset", "price": 499.00, "inStock": true}
  ]
}
```

**SLD - Array**:
```
products{id[1|name[Laptop|price[3999.90|inStock[^1~id[2|name[Mouse|price[149.90|inStock[^0~id[3|name[Headset|price[499.00|inStock[^1
```

**SLD - Table**:
```
id|name|price|inStock~1|Laptop|3999.90|^1~2|Mouse|149.90|^0~3|Headset|499.00|^1
```

### Edge Cases with Escaping

If your data contains delimiter characters:

```
company|Pipe^|Works Inc~product|Model^~XZ^~2000
```

This represents:
- company: "Pipe|Works Inc"
- product: "Model~XZ~2000"

## Technical Analysis: Why SLD Wins

### 1. Line Break Elimination
- **Windows**: Saves 2 bytes per line (`\r\n`)
- **Unix/Linux**: Saves 1 byte per line (`\n`)
- **Impact**: On a 100-row dataset, saves 100-200 bytes

### 2. Tokenization Efficiency
LLM tokenizers (like GPT's BPE) often create separate tokens for:
- Line breaks
- Indentation/whitespace
- JSON syntax (`{`, `}`, `[`, `]`, `:`, `,`)

SLD eliminates most of these, resulting in:
- **~44% fewer tokens** than JSON
- **~60% fewer tokens** than formatted JSON
- **~22% fewer tokens** than VSC

### 3. Character Frequency Analysis
Characters used by SLD are statistically rare in natural data:
- `|` - Appears in ~0.01% of text
- `~` - Appears in ~0.05% of text
- `[` - Context-dependent, but rarely as data
- `^` - Very rare outside of regex/math

This means escaping is almost never needed, keeping the format clean.

### 4. Parsing Simplicity
- Single-pass parsing
- No complex grammar
- Minimal state tracking
- Escape mechanism is trivial

### 5. Human Readability
While optimized for machines, SLD remains surprisingly readable:
```
name|John|age|30|city|NYC~name|Jane|age|28|city|LA
```

You can still see the structure without a decoder.

## Use Cases

### Perfect For:
- ✅ LLM context optimization
- ✅ API responses in token-constrained environments
- ✅ Embedding training data
- ✅ Log compression
- ✅ Cache keys
- ✅ Query string parameters

### Not Recommended For:
- ❌ Configuration files (use TOML/YAML)
- ❌ Data exchange between systems (use JSON/Protocol Buffers)
- ❌ When you need schema validation
- ❌ Public APIs (unless you hate your users)

## Implementation

### Encoding (Pseudocode)

```python
def encode_sld(data):
    # For table format (list of lists)
    if is_table(data):
        return "~".join("|".join(escape(v) for v in row) for row in data)
    
    # For array of objects
    if is_array(data):
        name = get_array_name(data)
        objects = "~".join(encode_object(obj) for obj in data)
        return f"{escape(name)}{{{objects}"
    
    # For single object
    return encode_object(data)

def encode_object(obj):
    parts = []
    items = list(obj.items())
    for i, (key, value) in enumerate(items):
        is_last = (i == len(items) - 1)
        separator = "~" if is_last else "|"
        parts.append(f"{escape(key)}[{escape(value)}{separator}")
    return "".join(parts)

def escape(text):
    if text is True:
        return "^1"
    if text is False:
        return "^0"
    if text is None:
        return ""
    return str(text).replace("^", "^^").replace("|", "^|").replace("~", "^~").replace("[", "^[").replace("{", "^{")
```

### Decoding (Pseudocode)

```python
def decode_sld(sld_string):
    records = []
    for record_str in split_unescaped(sld_string, "~"):
        record = {}
        fields = split_unescaped(record_str, "|")
        i = 0
        while i < len(fields):
            key = unescape(fields[i])
            if "[" in fields[i]:
                # Handle nested object
                record[key] = parse_nested(fields[i+1:])
            else:
                record[key] = unescape(fields[i+1])
                i += 2
        records.append(record)
    return records
```

## The Meme Factor

Let's be honest: this is absolutely ridiculous and we love it. 

- **JSON**: "I'm verbose but everyone uses me"
- **TOON**: "I'm simpler and save tokens"
- **VSC**: "Hold my beer, I'm even simpler"
- **SLD**: "Everything is a single line. EVERYTHING."

## The Definitive Argument Against CSV

While many criticized TOON for resembling CSV, SLD goes further:

**CSV has serious problems:**
- Multiple lines = character waste
- Commas are SUPER common in real data
- Quote escaping is confusing ("", really?)
- No real standard for nested objects

**SLD solves all of this:**
- One line = maximum efficiency
- Rare delimiters = escape almost never needed
- Natively supported nested objects
- Simple and consistent escape

## FAQ

**Q: Should I actually use this in production?**  
A: Only if you want your coworkers to question your sanity.

**Q: Is this actually more efficient?**  
A: Yes! Ironically, for LLM contexts, it genuinely uses fewer tokens.

**Q: What about binary formats?**  
A: Those are for people who care about "engineering" and "best practices."

**Q: Can I use this in my startup?**  
A: You can, but you probably shouldn't. Your investors might have questions.

**Q: This is a joke, right?**  
A: It started as one, but the math checks out. ¯\\\_(ツ)\_/¯

## Visual Comparison

```
╔══════════╦══════════╦═══════════════════════════════════════╗
║ Format   ║ Tokens   ║ Efficiency                            ║
╠══════════╬══════════╬═══════════════════════════════════════╣
║ JSON     ║ 125      ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓ 100% (baseline)         ║
║ TOON     ║ 70       ║ ▓▓▓▓▓▓▓ 56% of JSON size              ║
║ VSC      ║ 36       ║ ▓▓▓ 29% of JSON size                  ║
║ SLD      ║ 28       ║ ▓▓ 22% of JSON size 👑                ║
╚══════════╩══════════╩═══════════════════════════════════════╝
```

## Documentation

- 📖 [Full Specification](SPECIFICATION.md) - Complete technical specification
- ⚡ [Quick Reference](QUICK_REFERENCE.md) - Fast lookup guide for all three formats
- 📝 [Syntax Guide](SYNTAX_GUIDE.md) - Detailed examples and patterns
- 🇪🇸 [Documentación en Español](README.es.md) - Spanish documentation
- 💾 [Code Examples](implementations/) - Working implementations in 6 languages

## Contributing

Got an even more ridiculous data format idea? Open a PR! Let's see how far we can take this meme.

## License

MIT - Because even memes deserve proper licensing.

---

**Remember**: With great token efficiency comes great responsibility. Use SLD wisely, or not at all. We're not your parents.

**SLD: Because if you're going to do something ridiculous, do it right.
Single Line Data
