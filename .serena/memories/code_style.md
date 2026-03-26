# Code Style & Conventions

## General
- Line length: 100 characters (ruff)
- Python 3.10+ only
- Type hints required (strict mypy mode)
- English docstrings required (+ PT-BR optional)
- No nested ifs - use early returns / guard clauses

## Formatting
- ruff format (automatic formatting)
- ruff lint with E, F, I, UP, B, SIM rules
- mypy strict mode enabled

## Naming
- Classes: PascalCase
- Functions/methods: snake_case
- Constants: UPPER_SNAKE_CASE
- Private members: _leading_underscore

## Testing
- pytest framework
- Use respx for HTTP mocking
- TDD approach: tests first, then implementation
- Test file location: tests/test_<module>.py
