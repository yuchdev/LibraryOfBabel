### Build/Configuration Instructions

- **Environment**: This project requires Python 3.11 or higher.
- **Package Manager**: Uses `hatchling` as the build backend.
- **Setup**: To set up the development environment, navigate to the `babel/` directory and install the package in editable mode with development dependencies:
  ```bash
  cd babel
  python -m pip install -e ".[dev]"
  ```
- **Structure**: The source code is located in `babel/src/babel/`. Note that the package name for imports is `babel`.

### Testing Information

- **Execution**: Run all tests from the `babel/` directory using `pytest`:
  ```bash
  python -m pytest
  ```
- **Adding New Tests**:
  - Place new test files in the `babel/tests/` directory.
  - Test files should be named `test_*.py`.
  - Use `pytest` fixtures for common setup (see `babel/tests/conftest.py`).
- **Demo Test**:
  Here is a simple test case demonstrating how to test the math library:
  ```python
  import math
  from babel.mathlib.logmath import log10_pow

  def test_example_log10_pow():
      # Verify that 10^2 = 100, so log10(100) = 2
      assert log10_pow(10, 2) == 2.0
      # Verify log10(2^3) matches math.log10(8)
      assert math.isclose(log10_pow(2, 3), math.log10(8))
  ```

### Additional Development Information

- **Core Rules**:
  1. **Local-Only**: No HTTP requests during normal execution.
  2. **Lazy Generation**: Only generate requested pages, never full books in memory.
  3. **Determinism**: Use `deterministic_uint64(seed, namespace, position)` from `babel.utils.hashing`. Never use Python's `hash()` or `random.seed()`.
  4. **Log-Space Math**: Use `log10_*` functions from `babel.mathlib.logmath` for large numbers to avoid overflow.
- **Code Style**:
  - Follow PEP 8 with a line length limit of 100 characters.
  - Use `ruff` for linting (`E`, `F`, `I` rules).
  - Target Python 3.11 features.
- **Generator Modes**: To add a new generator mode, create a new class inheriting from `LibraryGenerator` in `babel/src/babel/generators/` and register it in `babel/src/babel/cli.py`.
