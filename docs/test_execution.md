# Test Execution Record

## Environment

- Date: 13 September 2026
- Operating system: Windows
- Python: 3.12.1
- Test framework: pytest
- Coverage tool: pytest-cov
- Static analysis: Ruff
- Database: temporary SQLite database
- External services: none required

## Test Execution

Command:

```powershell
python -m pytest --cov=app --cov=trackmate_lib --cov-branch --cov-report=term-missing --cov-report=html

Result: **20 passed** in 8.1 seconds.
The HTML report is generated in `htmlcov/index.html` and is intentionally ignored by Git.
```
