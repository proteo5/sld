# SLD - Single Line Data Format

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> The ultimate token-efficient data format that makes JSON cry, CSV look bloated, and leaves GOON and BONER in the dust.

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

**SLD (Single Line Data)** is a revolutionary data serialization format designed to minimize token usage in LLM contexts by eliminating ALL line breaks and using ultra-rare separator characters. While others were arguing about JSON vs TOON vs VSC vs GOON vs BONER, we went further.

## Why SLD is Superior

### Token Comparison

| Format | Example | Token Count |
|--------|---------|-------------|
| **BONER** | Enhanced ASCII redundancy | **420 tokens** 💀 |
| **GOON** | Verbose assignment syntax | **356 tokens** |
| **JSON** | Traditional verbose format | **125 tokens** |
| **TOON** | Simplified syntax | **70 tokens** |
| **VSC** | Line-based comma format | **36 tokens** |
| **SLD** | Everything in one line | **~28 tokens** ✨ |

### The SLD Advantage

1. **True Single Line**: Unlike VSC which uses multiple lines, SLD is ACTUALLY a single line of text, saving 1-2 characters per line break (depending on OS: `\n` or `\r\n`)
2. **Rare Separators**: Uses characters that almost never appear in data (`|`, `~`, `[`, `^`)
3. **Not Binary Gibberish**: Unlike BONER's ASCII art approach with 420 tokens of redundancy
4. **Actually Readable**: Unlike GOON's verbose assignment syntax with 356 tokens
5. **Escape Strategy**: Simple escape mechanism that's rarely needed
6. **Null/Empty Support**: Easy to represent with `||`
7. **Nested Structures**: Full support for objects and arrays

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

**JSON** (125 tokens):
```json
{
  "products": [
    {"id": 1, "name": "Laptop", "price": 3999.90, "inStock": true},
    {"id": 2, "name": "Mouse", "price": 149.90, "inStock": false},
    {"id": 3, "name": "Headset", "price": 499.00, "inStock": true}
  ]
}
```

**TOON** (70 tokens):
```
products[3](id,name,price):
  1,Laptop,3999.90
  2,Mouse,149.90
  3,Headset,499.00
```

**VSC** (36 tokens):
```
Laptop,3999.90
Mouse,149.90
Headset,499.00
```

**SLD - Array** (~28 tokens):
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
║ BONER    ║ 420      ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 336% 💀  ║
║ GOON     ║ 356      ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 285%          ║
║ JSON     ║ 125      ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓ 100% (baseline)         ║
║ TOON     ║ 70       ║ ▓▓▓▓▓▓▓ 56%                           ║
║ VSC      ║ 36       ║ ▓▓▓ 29%                               ║
║ SLD      ║ 28       ║ ▓▓ 22% 👑                             ║
╚══════════╩══════════╩═══════════════════════════════════════╝
```

## Documentation

- 📖 [Full Specification](SPECIFICATION.md) - Complete technical specification
- ⚡ [Quick Reference](QUICK_REFERENCE.md) - Fast lookup guide for all three formats
- 📝 [Syntax Guide](SYNTAX_GUIDE.md) - Detailed examples and patterns
- 🇪🇸 [Documentación en Español](README.es.md) - Spanish documentation
- 💾 [Code Examples](implementations/) - Working implementations in 6 languages

---

## Why SLD Beats Every Other Format

### 🆚 SLD vs BONER (420 tokens 💀)

**The Problem with BONER:**
- Literally encodes everything as binary ASCII
- 336% MORE tokens than JSON (how is that even possible?)
- Completely unreadable by humans
- "Enhanced redundancy" is just fancy words for "extremely wasteful"
- Treating binary as a text format defeats the entire purpose

**Why SLD Wins:**
- ✅ **93% fewer tokens** than BONER (28 vs 420)
- ✅ Actually human-readable
- ✅ No pointless binary conversion overhead
- ✅ Designed for efficiency, not ASCII art experiments

### 🆚 SLD vs GOON (356 tokens)

**The Problem with GOON:**
- Verbose assignment syntax with excessive keywords (BEGIN, END, DEF, ARR, STR, NUM)
- Type annotations on EVERYTHING (overkill for data serialization)
- 285% MORE tokens than JSON
- Looks like pseudocode, not a data format
- Way too much ceremony for simple data

**Why SLD Wins:**
- ✅ **92% fewer tokens** than GOON (28 vs 356)
- ✅ No redundant type annotations
- ✅ No unnecessary BEGIN/END blocks
- ✅ Minimal syntax overhead
- ✅ Self-documenting without being verbose

### 🆚 SLD vs JSON (125 tokens)

**The Problem with JSON:**
- Excessive use of quotes, braces, brackets, colons, and commas
- Every string needs quotes (even single-word keys)
- Lots of structural characters that add no information
- Multi-line formatting wastes characters
- Token-heavy for LLM contexts

**Why SLD Wins:**
- ✅ **78% fewer tokens** than JSON (28 vs 125)
- ✅ No quotes needed for simple values
- ✅ Minimal structural overhead
- ✅ True single-line format
- ✅ Property names are self-documenting without quotes

### 🆚 SLD vs TOON (70 tokens)

**The Problem with TOON:**
- Still uses multiple lines (wastes newline characters)
- Array length declarations are redundant
- Column headers separate from type info
- Colon and parenthesis overhead
- Not as compact as it could be

**Why SLD Wins:**
- ✅ **60% fewer tokens** than TOON (28 vs 70)
- ✅ True single line (no newlines at all)
- ✅ No redundant length declarations
- ✅ Headers integrated naturally (table format)
- ✅ Simpler delimiter strategy

### 🆚 SLD vs VSC (36 tokens)

**The Problem with VSC:**
- Still uses multiple lines (1-2 bytes wasted per line break)
- Limited to simple comma-separated values
- No native support for objects or arrays
- Commas are common in data (requires escaping)
- No property names (relies on position)

**Why SLD Wins:**
- ✅ **22% fewer tokens** than VSC (28 vs 36)
- ✅ Actual single line (not multiple lines)
- ✅ Native object and array support
- ✅ Rare delimiters (less escaping needed)
- ✅ Self-documenting with property names

### 🆚 SLD vs CSV (Not even in the race)

**The Problem with CSV:**
- Multiple lines waste bytes
- Commas are extremely common in real data
- Quote escaping is a nightmare ("" to escape ")
- No standard for nested structures
- No type information
- Whitespace handling is inconsistent

**Why SLD Wins:**
- ✅ True single-line format
- ✅ Rare delimiters (`|`, `~`, `[`, `{`) = minimal escaping
- ✅ Simple escape mechanism (`^`)
- ✅ Native nested object/array support
- ✅ Boolean types built-in (`^1`, `^0`)
- ✅ Consistent, well-defined spec

---

### The Bottom Line

| Format | Token Count | vs SLD | Main Issue |
|--------|-------------|--------|------------|
| **BONER** | 420 💀 | **15x worse** | Binary gibberish masquerading as text |
| **GOON** | 356 | **12.7x worse** | Verbose ceremony with excessive keywords |
| **JSON** | 125 | **4.5x worse** | Quote and brace overhead |
| **TOON** | 70 | **2.5x worse** | Still multi-line with redundant info |
| **VSC** | 36 | **1.3x worse** | Multi-line, no objects/arrays |
| **CSV** | ~50-80 | **~2-3x worse** | Terrible escaping, no structure |
| **SLD** | **28** 👑 | **Winner** | Maximum efficiency, minimal overhead |

**SLD achieves the impossible: It's more efficient than everything while still being human-readable.**

## Contributing

Got an even more ridiculous data format idea? Open a PR! Let's see how far we can take this meme.

## License

MIT - Because even memes deserve proper licensing.

---

**Remember**: With great token efficiency comes great responsibility. Use SLD wisely, or not at all. We're not your parents.

**SLD: Because if you're going to do something ridiculous, do it right.
Single Line Data
