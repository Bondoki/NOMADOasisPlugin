# Reference

This section provides technical specifications for the `NOMAD-CRC1415Plugin`.

## Plugin Entry Points

The plugin registers several entry points in `pyproject.toml` to allow NOMAD to discover the schema packages.

| Entry Point | Target Class | Description |
|-------------|--------------|-------------|
| `CRC1415SampleOverview` | `CRC1415SampleOverview` | General sample overview schema |
| `CRC1415MeasurementXRD` | `CRC1415MeasurementXRD` | X-Ray Diffraction mapping |
| `CRC1415MeasurementRaman` | `CRC1415MeasurementRaman` | Raman Spectroscopy mapping |
| `CRC1415MeasurementSEM` | `CRC1415MeasurementSEM` | Scanning Electron Microscopy mapping |
| `CRC1415MeasurementTEM` | `CRC1415MeasurementTEM` | Transmission Electron Microscopy mapping |
| `CRC1415MeasurementTGA` | `CRC1415MeasurementTGA` | Thermogravimetric Analysis mapping |
| `CRC1415MeasurementCV` | `CRC1415MeasurementCV` | Cyclic Voltammetry mapping |
| `CRC1415MeasurementIR` | `CRC1415MeasurementIR` | Infrared Spectroscopy mapping |
| `CRC1415MeasurementAdsorption` | `CRC1415MeasurementAdsorption` | Adsorption measurement mapping |
| `CRC1415MeasurementGeneric` | `CRC1415MeasurementGeneric` | Generic measurement fallback |

## Schema Components

### `ELNMeasurement`
The base class for all measurement schemas. It provides the core structure for mapping raw data to NOMAD fields.

### `PlotSection`
A mixin class that enables the `generate_plots()` method, allowing the plugin to create Plotly figures for the NOMAD UI.

### `ArchiveSection`
A mixin class used to handle the archiving of raw data files and their associated metadata.

## Glossary

- **Mapping**: The process of transforming raw instrument data into a structured NOMAD schema.
- **Entry Point**: A mechanism in Python packaging that allows a plugin to register itself with a host application (NOMAD).
- **Schema Package**: A collection of definitions that describe the structure of data for a specific scientific domain.
