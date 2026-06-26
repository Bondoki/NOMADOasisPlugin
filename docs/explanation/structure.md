# Project Structure

This document provides a technical overview of the `NOMAD-CRC1415Plugin` directory structure and the architectural patterns used for extending the plugin's functionality.

## Directory Tree

```text
NOMAD-CRC1415Plugin/
├── docs/                       # Documentation source files
│   ├── assets/                 # Images and static files
│   ├── explanation/            # Conceptual and architectural guides
│   │   ├── explanation.md       # High-level overview
│   │   └── structure.md        # Project structure and design patterns
│   ├── how_to/                 # Step-by-step guides for users and contributors
│   ├── reference/              # API and schema references
│   ├── stylesheets/            # Custom CSS for documentation
│   ├── theme/                  # Documentation theme overrides
│   └── tutorial/               # Onboarding tutorials
├── src/                        # Source code
│   └── crc1415plugin/          # Main plugin package
│       ├── __init__.py
│       └── schema_packages/     # NOMAD schema definitions
│           ├── __init__.py
│           ├── ELNSampleOverviewSchema.py
│           └── schemas_measurement/  # Measurement-specific schemas
│               ├── __init__.py       # Registration point for measurement schemas
│               ├── MeasurementAdsorption.py
│               ├── MeasurementCV.py
│               ├── MeasurementGeneric.py
│               ├── MeasurementIR.py
│               ├── MeasurementRaman.py
│               ├── MeasurementSEM.py
│               ├── MeasurementTEM.py
│               ├── MeasurementTGA.py
│               └── MeasurementXRD.py
└── tests/                      # Test suite
    ├── datacrc1415plugin/      # Integration tests and test data (archives, raw files)
    └── schema_packages/        # Unit tests for schemas
```

## Component Breakdown

### `src/`
The `src/` directory contains the core logic of the plugin. The primary package `crc1415plugin` houses the `schema_packages` directory, where the NOMAD-compatible schemas are defined. The organization separates general sample overview schemas from specific measurement schemas to maintain modularity as the number of supported techniques grows.

### `tests/`
The `tests/` directory is divided into two main areas:
- **`schema_packages/`**: Contains unit tests to validate the logic and structure of individual schemas.
- **`datacrc1415plugin/`**: Acts as a repository for test fixtures. This includes both raw measurement files (e.g. `.cif`, `.tif`, `.raw`, `.txt`) and pre-processed NOMAD archive YAML files used to verify that the plugin correctly parses and maps data to the schemas.

### `docs/`
The `docs/` directory follows a structured documentation hierarchy:
- **`how_to/`**: Practical guides for installation and contribution.
- **`explanation/`**: High-level technical explanations of the "why" and "how" behind the plugin's design.
- **`reference/`**: Detailed technical specifications.

---

## Design Pattern: Adding New Measurement Types

The plugin employs a **Modular Registration Pattern** for measurement schemas. This ensures that adding a new measurement technique does not require modifying the core plugin logic, only the schema package.

### Implementation Steps

To add a new measurement type (e.g., `MeasurementXPS`), follow these steps:

1.  **Create the Schema File**: 
    Create a new Python file in `src/crc1415plugin/schema_packages/schemas_measurement/` following the naming convention `Measurement<Technique>.py`. Define the schema class within this file.
    
2.  **Register the Schema**: 
    Add an **explicit absolute import** in `src/crc1415plugin/schema_packages/schemas_measurement/__init__.py`.
    
    Example:
    ```python
    from crc1415plugin.schema_packages.schemas_measurement.MeasurementXPS import MeasurementXPS
    ```
    
    By importing the class into the `__init__.py` of the `schemas_measurement` package, the schema becomes an attribute of the package namespace, allowing the plugin's registry to discover and load it automatically.

3.  **Add Test Data**:
    Place representative raw data files and a corresponding `.archive.yaml` test case in `tests/datacrc1415plugin/` to verify the mapping logic.

4.  **Verify**: 
    Run the test suite in `tests/schema_packages/` to ensure the new schema is correctly integrated and validated.
