# Tutorial

This tutorial guides you through the process of using the `CRC1415Plugin` plugin to upload and visualize measurement data in NOMAD.

## Step 1: Prepare Your Data

Ensure your measurement files are in the format expected by the plugin. The plugin supports several measurement types:  

- **XRD**: X-Ray Diffraction
- **Raman**: Raman Spectroscopy
- **SEM/TEM**: Scanning/Transmission Electron Microscopy
- **TGA**: Thermogravimetric Analysis
- **CV**: Cyclic Voltammetry
- **IR**: Infrared Spectroscopy
- **Adsorption**: Gas adsorption measurements

## Step 2: Upload to NOMAD

Use the NOMAD interface or API to upload your raw data files. The plugin will automatically detect the file type based on the schema entry points defined in the `pyproject.toml`.

## Step 3: Verify Mapping

Once uploaded, check the "Schema" section of your entry to ensure that the raw data has been correctly mapped to the NOMAD schema fields. The plugin uses specialized classes like `MeasurementXRD` or `MeasurementRaman` to handle this mapping.

## Step 4: Visualization

Navigate to the plot section to see the automatically generated plots. The plugin implements `generate_plots()` for most measurement types to provide immediate visual feedback using Plotly.
