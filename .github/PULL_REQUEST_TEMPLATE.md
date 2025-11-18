## Description
<!-- Provide a clear and concise description of your changes -->

## Type of Change
<!-- Mark the relevant option with an 'x' -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] New language implementation
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Test improvement

## Implementation
<!-- Which implementation(s) does this PR affect? -->
- [ ] Python
- [ ] JavaScript
- [ ] Go
- [ ] C#
- [ ] PHP
- [ ] Java
- [ ] New language: _____________
- [ ] Documentation only
- [ ] Multiple implementations

## Checklist
<!-- Mark completed items with an 'x' -->
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## For New Language Implementations
<!-- If adding a new language, complete this section -->
- [ ] Implements all required functions (encodeSLD, decodeSLD, encodeMLD, decodeMLD)
- [ ] Implements format conversion (sldToMLD, mldToSLD)
- [ ] Includes comprehensive test suite (see CONTRIBUTING.md for required tests)
- [ ] Includes package manifest (e.g., Cargo.toml, go.mod, package.json)
- [ ] Includes README with installation and usage instructions
- [ ] Follows language-specific coding standards
- [ ] Added to implementations/README.md
- [ ] Added CI workflow to .github/workflows/ci.yml

## Testing
<!-- Describe the tests you ran to verify your changes -->
```bash
# Provide commands to run tests
cd implementations/[language]
[test command]
```

### Test Results
<!-- Paste test output here -->
```
[Test output]
```

## Breaking Changes
<!-- If this introduces breaking changes, describe them and the migration path -->

## Related Issues
<!-- Link related issues using #issue_number -->
Fixes #
Related to #

## Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## Additional Notes
<!-- Any additional information that reviewers should know -->
