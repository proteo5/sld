# SLD Format Implementations v1.1

This directory contains reference implementations of the SLD (Single Line Data) and MLD (Multi Line Data) formats in various programming languages.

## Available Implementations

### Python
- **File**: `python/sld.py`
- **Test**: `python/test_sld.py`
- **Install**: `pip install -e implementations/python`
- **Run Tests**: `cd implementations/python && pytest test_sld.py`
- **Features**: Full SLD/MLD encode/decode with format conversion

### JavaScript/Node.js
- **File**: `javascript/sld.js`
- **Test**: `javascript/test_sld.js`
- **Install**: `npm install implementations/javascript`
- **Run Tests**: `cd implementations/javascript && npm test`
- **Features**: Works in both Node.js and browsers

### Go
- **File**: `go/sld.go`
- **Test**: `go/sld_test.go`
- **Install**: `go get github.com/proteo5/sld`
- **Run Tests**: `cd implementations/go && go test`
- **Features**: Idiomatic Go with comprehensive test coverage

### C#
- **File**: `csharp/SLD.cs`
- **Project**: `csharp/SLD.csproj`
- **Build**: `dotnet build`
- **Run Tests**: `dotnet test`
- **Features**: .NET 6.0+ with xUnit tests

### PHP
- **File**: `php/sld.php`
- **Package**: `php/composer.json`
- **Install**: `composer install`
- **Run Tests**: `composer test`
- **Features**: PSR-12 compliant with PHPUnit tests

### Java
- **File**: `java/SLD.java`
- **Project**: `java/pom.xml`
- **Build**: `mvn compile`
- **Run Tests**: `mvn test`
- **Features**: Maven project with JUnit tests

## Common Features

All v1.1 implementations support:
- ✅ SLD format encoding/decoding (single-line with `~` separator)
- ✅ MLD format encoding/decoding (multi-line with `\n` separator)
- ✅ Format conversion (SLD ↔ MLD)
- ✅ Field separator `;` (shell-safe)
- ✅ Property marker `[` and array marker `{`
- ✅ Boolean values (`^1` and `^0`)
- ✅ Escape character `^` handling
- ✅ Null/empty value support
- ✅ Array encoding with `~` element separator and explicit `}` close
- ✅ Working examples included in each file
- ✅ Unit tests with comprehensive coverage

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
