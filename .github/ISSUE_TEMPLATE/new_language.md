---
name: New Language Implementation
about: Propose or contribute a new language implementation
title: '[IMPL] Add [Language] implementation'
labels: new-language, enhancement
assignees: ''
---

## Language Information
- **Language**: [e.g., Rust, C++, Ruby, Swift]
- **Minimum Version**: [e.g., Rust 1.70+, C++17, Ruby 3.0+]
- **Package Manager**: [e.g., Cargo, CMake, RubyGems]

## Implementation Status
- [ ] Planning phase
- [ ] In progress
- [ ] Ready for review
- [ ] Complete (submitting PR)

## Checklist
Implementation Requirements (see CONTRIBUTING.md):
- [ ] Implements `encodeSLD()` function
- [ ] Implements `decodeSLD()` function
- [ ] Implements `encodeMLD()` function
- [ ] Implements `decodeMLD()` function
- [ ] Implements `sldToMLD()` conversion
- [ ] Implements `mldToSLD()` conversion
- [ ] Handles all escape sequences (`^;`, `^~`, `^[`, `^{`, `^^`)
- [ ] Supports boolean encoding (`^1`/`^0`)
- [ ] Supports array encoding with `{` marker
- [ ] Supports null/empty values
- [ ] Includes working examples
- [ ] Includes comprehensive tests:
  - [ ] Basic encoding/decoding
  - [ ] Multiple records
  - [ ] Arrays
  - [ ] Booleans
  - [ ] Escaped characters
  - [ ] Null values
  - [ ] Format conversion
- [ ] Package manifest (e.g., Cargo.toml, CMakeLists.txt)
- [ ] README with usage instructions
- [ ] Follows language-specific style guide

## Additional Features
Optional enhancements:
- [ ] Streaming/incremental parsing
- [ ] Performance benchmarks
- [ ] Type safety (for statically typed languages)
- [ ] Custom error types
- [ ] CLI tool

## Code Sample
```rust
// Example of proposed API
use sld::{encode_sld, decode_sld};

let data = HashMap::from([
    ("name", "Alice"),
    ("age", "30"),
]);

let sld = encode_sld(&data);
let decoded = decode_sld(&sld);
```

## Repository Structure
Where will the implementation be located?
```
implementations/
  rust/
    - sld.rs (or lib.rs)
    - tests.rs
    - Cargo.toml
    - README.md
```

## Timeline
Expected completion date (if applicable): 

## Help Needed
Are there any areas where you need assistance?
- [ ] Understanding the specification
- [ ] Testing strategy
- [ ] Package configuration
- [ ] Documentation
- [ ] Code review

## References
- Specification: [SPECIFICATION_SLD.md](../../SPECIFICATION_SLD.md)
- Contribution Guide: [CONTRIBUTING.md](../../CONTRIBUTING.md)
- Reference Implementation: [Python implementation](../../implementations/python/sld.py)
