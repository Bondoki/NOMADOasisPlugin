# Install This Plugin

To use the `CRC1415Plugin` plugin, it must be installed in your NOMAD Oasis environment.

## Prerequisites

- A running NOMAD Oasis installation.
- Python 3.10, 3.11, or 3.12.
- Administrative access to the NOMAD instance.

## Installation Steps

1. **Clone the Repository**:
   Clone this repository to your server or include it in your Docker build.

2. **Install Dependencies**:
   The plugin requires several dependencies including `nomad-lab`, `pydantic`, `temporalio`, and `xmltodict`. These can be installed via:
   ```bash
   pip install .
   ```

3. **Add to Plugin Path**:
   Add the plugin directory to the `NOMAD_PLUGIN_PATH` environment variable or specify it in your `nomad-config.yaml`.

4. **Restart NOMAD**:
   Restart the NOMAD services to load the new schema packages and entry points.

!!! note "Attention"
    Ensure that the environment matches the Python versions specified in `pyproject.toml` to avoid compatibility issues.
