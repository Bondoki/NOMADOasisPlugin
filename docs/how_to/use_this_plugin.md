# How to Use This Plugin

This plugin can be used in a NOMAD Oasis installation to handle specific CRC1415 measurement data.

## Add This Plugin to Your NOMAD installation

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/plugins/plugins.html#add-a-plugin-to-your-nomad) for all details on how to deploy the plugin on your NOMAD instance.

## Supported Measurement Types

The plugin automatically handles the following measurement types through specialized entry points:

- **XRD**: Handles X-ray diffraction data and generates corresponding plots.
- **Raman**: Parses Raman spectroscopy data, including repeated byte unpacking.
- **SEM/TEM**: Processes electron microscopy data (including base64 encoded images).
- **TGA**: Handles thermogravimetric analysis data.
- **CV**: Processes cyclic voltammetry experiments.
- **IR**: Handles infrared spectroscopy measurements.
- **Adsorption**: Parses Quantachrome .txt files for adsorption data.
- **Generic**: A fallback for other measurement types that can be archived.

## Data Processing Flow

1. **Ingestion**: Raw files are uploaded to NOMAD.
2. **Parsing**: The plugin's `SchemaPackageEntryPoint` identifies the measurement type.
3. **Mapping**: Data is mapped to the `ELNMeasurement` schema.
4. **Visualization**: The `generate_plots` method creates Plotly figures for the user.

!!! note "Attention"
    If a file fails to parse, check if the file format matches the expected instrument output for the selected measurement type.
