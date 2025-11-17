# SLD Format Implementations

This directory contains reference implementations of the SLD (Single Line Data) format in various programming languages.

## Available Implementations

### Python
- **File**: `python/sld.py`
- **Run**: `python python/sld.py`
- **Features**: Full encode/decode support with examples

### JavaScript/Node.js
- **File**: `javascript/sld.js`
- **Run**: `node javascript/sld.js`
- **Features**: Works in both Node.js and browsers

### Go
- **File**: `go/sld.go`
- **Usage**: Import as package or run example
- **Features**: Idiomatic Go with interfaces

### C#
- **File**: `csharp/SLD.cs`
- **Compile**: `csc SLD.cs` or use Visual Studio
- **Run**: `SLD.exe`
- **Features**: LINQ-friendly implementation

### PHP
- **File**: `php/sld.php`
- **Run**: `php php/sld.php`
- **Features**: Class-based with static methods

### Java
- **File**: `java/SLD.java`
- **Compile**: `javac SLD.java`
- **Run**: `java SLD`
- **Features**: Generic collections support

## Common Features

All implementations support:
- ✅ Encoding data to SLD format
- ✅ Decoding SLD strings back to native structures
- ✅ Proper escape sequence handling
- ✅ Null/empty value support
- ✅ Nested structures (simplified)
- ✅ Working examples

## Usage Examples

### Encoding

**Python:**
```python
from sld import encode

data = [{"name": "Laptop", "price": "3999.90"}]
sld_string = encode(data)
# Output: name|Laptop|price|3999.90
```

**JavaScript:**
```javascript
const { encode } = require('./sld');

const data = [{ name: "Laptop", price: "3999.90" }];
const sldString = encode(data);
// Output: name|Laptop|price|3999.90
```

**Go:**
```go
import "sld"

data := []map[string]interface{}{
    {"name": "Laptop", "price": "3999.90"},
}
sldString := sld.Encode(data)
// Output: name|Laptop|price|3999.90
```

### Decoding

**Python:**
```python
from sld import decode

sld_string = "name|Laptop|price|3999.90"
data = decode(sld_string)
# Output: {'name': 'Laptop', 'price': '3999.90'}
```

**JavaScript:**
```javascript
const { decode } = require('./sld');

const sldString = "name|Laptop|price|3999.90";
const data = decode(sldString);
// Output: { name: 'Laptop', price: '3999.90' }
```

## Testing

Each implementation includes example usage in its main section. Run the files directly to see:
- Simple product data encoding/decoding
- User records with multiple fields
- Escape character handling
- Null value support

## Implementation Notes

### Nested Structures
The current implementations provide simplified nested structure support. For complex deeply nested objects, you may need to enhance the parsing logic.

### Type Preservation
Most implementations treat values as strings. For type-safe deserialization, you may need to add schema validation or type hints.

### Performance
These are reference implementations optimized for clarity. For production use, consider:
- Streaming parsers for large datasets
- Buffer pooling to reduce allocations
- Compiled regex for splitting (where applicable)

## Contributing

To add a new language implementation:

1. Create a new directory with the language name
2. Implement the core functions:
   - `escape(text)` - Escape special characters
   - `unescape(text)` - Unescape sequences
   - `encode(data)` - Convert to SLD format
   - `decode(sldString)` - Parse SLD to native structures
3. Add working examples
4. Update this README

## License

All implementations are released under the MIT License, same as the main SLD project.
