# Contributing to SLD/MLD

Thank you for your interest in contributing to SLD/MLD! This document provides guidelines and instructions for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Adding a New Language Implementation](#adding-a-new-language-implementation)

---

## Code of Conduct

We expect all contributors to:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sld.git
   cd sld
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. **actual behavior**
- **Sample data** that causes the issue
- **Version information** (SLD v1.0 or v2.0)
- **Implementation language** (Python, JavaScript, etc.)

### Suggesting Enhancements

Enhancement suggestions should include:

- **Use case description**
- **Proposed solution**
- **Alternatives considered**
- **Impact on existing functionality**

### Documentation Improvements

Documentation contributions are highly valued! Areas include:

- Fixing typos or unclear explanations
- Adding examples
- Translating documentation
- Improving reference guides

---

## Development Setup

### General Requirements

- Git
- Text editor or IDE
- Language-specific tools (see below)

### Language-Specific Setup

#### Python
```bash
cd implementations/python
pip install -r requirements-dev.txt  # If exists
python sld.py  # Run examples
```

#### JavaScript/Node.js
```bash
cd implementations/javascript
npm install  # If package.json exists
node sld.js  # Run examples
```

#### Go
```bash
cd implementations/go
go run sld.go  # Run examples
go test       # Run tests if available
```

#### C#
```bash
cd implementations/csharp
dotnet build
dotnet run
```

#### PHP
```bash
cd implementations/php
php sld.php  # Run examples
```

#### Java
```bash
cd implementations/java
javac SLD.java
java io.github.proteo5.sld.SLDParser
```

---

## Coding Standards

### General Principles

1. **Follow v1.1 Specification**
   - Use `;` as field separator (not `|`)
   - Use `~` for SLD records, `\n` for MLD records
   - Use `[` for properties, `{` for arrays
   - Use `^` for escape sequences

2. **Maintain Consistency**
   - Follow the existing code style in each language
   - Use the same function/method names across implementations:
     - `encodeSLD()` / `encode_sld()` / `EncodeSLD()`
     - `decodeSLD()` / `decode_sld()` / `DecodeSLD()`
     - `encodeMLD()` / `encode_mld()` / `EncodeMLD()`
     - `decodeMLD()` / `decode_mld()` / `DecodeMLD()`
     - `sldToMLD()` / `sld_to_mld()` / `SLDToMLD()`
     - `mldToSLD()` / `mld_to_sld()` / `MLDToSLD()`

3. **Document Your Code**
   - Add docstrings/comments for all public functions
   - Include parameter descriptions
   - Provide usage examples

### Language-Specific Standards

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features, JSDoc comments
- **Go**: Follow `gofmt` and Go conventions
- **C#**: Follow Microsoft C# coding conventions
- **PHP**: Follow PSR-12 coding standard
- **Java**: Follow Oracle Java Code Conventions

---

## Testing Guidelines

### Required Tests

Every implementation should include tests for:

1. **Basic Encoding/Decoding**
   ```
   Input:  {"name": "Alice", "age": 30}
   SLD:    name[Alice;age[30
   MLD:    name[Alice;age[30
   ```

2. **Multiple Records**
   ```
   Input:  [{"name": "Alice"}, {"name": "Bob"}]
   SLD:    name[Alice~name[Bob~
   MLD:    name[Alice\nname[Bob
   ```

3. **Arrays**
   ```
   Input:  {"tags": ["admin", "user"]}
   SLD:    tags{admin,user
   ```

4. **Booleans**
   ```
   Input:  {"verified": true, "active": false}
   SLD:    verified[^1;active[^0
   ```

5. **Escaped Characters**
   ```
   Input:  {"note": "Price: $5;99"}
   SLD:    note[Price: $5^;99
   ```

6. **Empty/Null Values**
   ```
   Input:  {"name": "Alice", "middle": null}
   SLD:    name[Alice;middle[
   ```

7. **Format Conversion**
   ```
   SLD → MLD → SLD (should be identical)
   ```

### Running Tests

Create test files following these patterns:

- Python: `test_sld.py` (pytest)
- JavaScript: `sld.test.js` (Jest/Mocha)
- Go: `sld_test.go` (go test)
- Java: `SLDTest.java` (JUnit)
- C#: `SLDTests.cs` (NUnit/xUnit)
- PHP: `SLDTest.php` (PHPUnit)

---

## Pull Request Process

1. **Update Documentation**
   - Update README.md if adding new features
   - Update CHANGELOG.md with your changes
   - Add examples if applicable

2. **Test Your Changes**
   - Run all existing tests
   - Add tests for new functionality
   - Verify examples still work

3. **Commit Guidelines**
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable
   - Follow conventional commits format:
     ```
     feat: add MLD support to Python implementation
     fix: correct escape sequence handling in JavaScript
     docs: improve quick reference guide
     test: add array encoding tests
     ```

4. **Submit Pull Request**
   - Fill out the PR template completely
   - Link to related issues
   - Describe what changed and why
   - Include screenshots/examples if relevant

5. **Code Review**
   - Respond to feedback promptly
   - Make requested changes
   - Keep the discussion focused and constructive

---

## Adding a New Language Implementation

We welcome implementations in new languages! Follow these steps:

### 1. Create Directory Structure

```bash
mkdir -p implementations/LANGUAGE_NAME
cd implementations/LANGUAGE_NAME
```

### 2. Implement Core Functions

Your implementation MUST include:

**Encoding Functions:**
- `encodeSLD(data)` - Encode to SLD format (single line, `~` separators)
- `encodeMLD(data)` - Encode to MLD format (multi line, `\n` separators)

**Decoding Functions:**
- `decodeSLD(string)` - Decode SLD format
- `decodeMLD(string)` - Decode MLD format

**Conversion Functions:**
- `sldToMLD(string)` - Convert SLD to MLD
- `mldToSLD(string)` - Convert MLD to SLD

**Utility Functions:**
- `escapeValue(text)` - Escape special characters
- `unescapeValue(text)` - Unescape escape sequences

### 3. Follow v1.1 Specification

Ensure your implementation correctly handles:

- **Delimiters:**
  - Field: `;` (semicolon)
  - Record (SLD): `~` (tilde)
  - Record (MLD): `\n` (newline)
  - Property: `[` (square bracket)
  - Array: `{` (curly brace)
  - Escape: `^` (caret)

- **Escape Sequences:**
  - `^;` → `;`
  - `^~` → `~`
  - `^[` → `[`
  - `^{` → `{`
  - `^^` → `^`
  - `^1` → `true`
  - `^0` → `false`

- **Data Types:**
  - Strings (default)
  - Numbers (as strings, parsed by application)
  - Booleans (`^1`/`^0`)
  - Null/empty values
  - Arrays (using `{item1,item2}`)
  - Nested objects (recursive encoding)

### 4. Add Examples

Include working examples in your implementation file:

```
Example 1: Simple records
Example 2: Arrays
Example 3: Booleans
Example 4: Format conversion
Example 5: Escaped characters
```

### 5. Create README

Add `implementations/LANGUAGE_NAME/README.md`:

```markdown
# SLD/MLD Implementation for [Language]

## Installation

[Installation instructions]

## Usage

[Basic usage examples]

## API Reference

[Function documentation]

## Testing

[How to run tests]
```

### 6. Update Main README

Add your implementation to the main README.md:

- Add to installation section
- Add to language list
- Include code example

### 7. Submit Pull Request

Follow the [Pull Request Process](#pull-request-process) above.

---

## Preferred Languages for New Implementations

We're particularly interested in implementations for:

- **Rust** (for performance-critical applications)
- **C** (for embedded systems)
- **C++** (for system programming)
- **Ruby** (for web development)
- **Swift** (for iOS/macOS)
- **Kotlin** (for Android/JVM)
- **TypeScript** (for type-safe JavaScript)
- **Elixir** (for functional programming)
- **Zig** (for low-level programming)

---

## Questions or Need Help?

- **GitHub Discussions**: [github.com/proteo5/sld/discussions](https://github.com/proteo5/sld/discussions)
- **Issues**: [github.com/proteo5/sld/issues](https://github.com/proteo5/sld/issues)

---

## License

By contributing to SLD/MLD, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SLD/MLD! Your efforts help make data serialization more efficient for everyone.** 🚀
