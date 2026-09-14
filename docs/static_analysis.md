# Static Analysis Record

Executed on 2026-09-13:

```powershell
ruff check app trackmate_lib tests
```

Result: **33 findings**. Ruff reported import ordering/formatting (`I001`), unused imports (`F401`), and timezone-aware datetime suggestions (`DTZ001`, `DTZ005`).

These are recorded rather than mass-fixed because most predate the test work and a broad formatting rewrite would not improve application behavior. The test pass fixed the functional validation issue that Ruff helped highlight around numeric input handling. No secrets were printed or required by the normal test suite.
