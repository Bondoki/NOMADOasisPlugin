# Contribute to This Plugin

We welcome contributions to the `crc1415testsample` plugin. Whether you are adding a new measurement type or fixing a bug, please follow these guidelines.

## Development Environment

To set up your development environment, install the optional development dependencies:
```bash
pip install ".[dev]"
```
This installs tools like `ruff` for linting and `pytest` for testing.

## Adding a New Measurement Type

The plugin uses a **Modular Registration Pattern**. To add a new technique (e.g., `MeasurementXPS`):

1. **Create the Schema File**: 
   Create `src/crc1415plugin/schema_packages/schemas_measurement/MeasurementXPS.py`.
2. **Implement the Class**: 
   Inherit from `ELNMeasurement`, `PlotSection`, and `ArchiveSection`. Implement `generate_plots()` for visualization.
3. **Register the Schema**: 
   Add an absolute import in `src/crc1415plugin/schema_packages/schemas_measurement/__init__.py`.
4. **Update Entry Points**: 
   Add the new entry point to the `[project.entry-points.'nomad.plugin']` section in `pyproject.toml`.
5. **Add Tests**: 
   Create a test case in `tests/schema_packages/test_crc1415plugin.py` and provide sample data in `tests/datacrc1415plugin/`.

## Testing

Run the test suite to ensure your changes didn't break existing functionality:
```bash
pytest
```
