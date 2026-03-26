# Task Completion Checklist

1. Write tests first (TDD)
2. Run tests to see RED (should fail)
3. Implement the feature
4. Run tests to see GREEN (all pass)
5. Format code: `ruff format src/ tests/`
6. Type check: `mypy src/`
7. Commit with message in format: `feat:` or `fix:` or `test:`
8. Push to remote
9. Report: status, test results, commit hash

## Push Conflicts
If push fails with conflict (Task 5 running in parallel):
- Run: `git pull --rebase`
- Then: `git push`
