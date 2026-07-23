from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field

# class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')
# 
#     def load(self):
#         from crc1415testsample.schema_packages.schema_package import m_package
# 
#         return m_package
# 
# 
# schema_package_entry_point = NewSchemaPackageEntryPoint(
#     name='NewSchemaPackage',
#     description='New schema package entry point configuration.',
# )
# 
# 
# class CRC1414SchemaEntryPoint(SchemaPackageEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')
# 
#     def load(self):
#         from crc1415testsample.schema_packages.CRC1415_A04_schema import m_package
# 
#         return m_package
# 
# 
# CRC1415_A04_schema = CRC1414SchemaEntryPoint(
#     name='CRC1415Schema',
#     description='New test schema package for CRC1415.',
# )

class CRC1414SampleEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.ELNSampleOverviewSchema import m_package

        return m_package


CRC1415SampleOverview = CRC1414SampleEntryPoint(
    name='CRC1415SampleOverview',
    description='Schema package for CRC1415 for the sample overview schema.',
)

class CRC1414MeasurementGenericEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementGeneric import (
            m_package,
        )

        return m_package


CRC1415MeasurementGeneric = CRC1414MeasurementGenericEntryPoint(
    name='CRC1415MeasurementGeneric',
    description='Schema package for CRC1415 - MeasurementGeneric.',
)

class CRC1414MeasurementXRDEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementXRD import (
            m_package,
        )

        return m_package


CRC1415MeasurementXRD = CRC1414MeasurementXRDEntryPoint(
    name='CRC1415MeasurementXRD',
    description='Schema package for CRC1415 - MeasurementXRD.',
)

class CRC1414MeasurementIREntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementIR import (
            m_package,
        )

        return m_package


CRC1415MeasurementIR = CRC1414MeasurementIREntryPoint(
    name='CRC1415MeasurementIR',
    description='Schema package for CRC1415 - MeasurementIR.',
)

class CRC1414MeasurementSEMEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementSEM import (
            m_package,
        )

        return m_package


CRC1415MeasurementSEM = CRC1414MeasurementSEMEntryPoint(
    name='CRC1415MeasurementSEM',
    description='Schema package for CRC1415 - MeasurementSEM.',
)

class CRC1414MeasurementTEMEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementTEM import (
            m_package,
        )

        return m_package


CRC1415MeasurementTEM = CRC1414MeasurementTEMEntryPoint(
    name='CRC1415MeasurementTEM',
    description='Schema package for CRC1415 - MeasurementTEM.',
)

class CRC1414MeasurementRamanEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementRaman import (
            m_package,
        )

        return m_package


CRC1415MeasurementRaman = CRC1414MeasurementRamanEntryPoint(
    name='CRC1415MeasurementRaman',
    description='Schema package for CRC1415 - MeasurementRaman.',
)

class CRC1414MeasurementAdsorptionEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementAdsorption import (
            m_package,
        )

        return m_package


CRC1415MeasurementAdsorption = CRC1414MeasurementAdsorptionEntryPoint(
    name='CRC1415MeasurementAdsorption',
    description='Schema package for CRC1415 - MeasurementAdsorption.',
)

class CRC1414MeasurementTGAEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementTGA import (
            m_package,
        )

        return m_package


CRC1415MeasurementTGA = CRC1414MeasurementTGAEntryPoint(
    name='CRC1415MeasurementTGA',
    description='Schema package for CRC1415 - MeasurementTGA.',
)

class CRC1414MeasurementCVEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementCV import (
            m_package,
        )

        return m_package


CRC1415MeasurementCV = CRC1414MeasurementCVEntryPoint(
    name='CRC1415MeasurementCV',
    description='Schema package for CRC1415 - MeasurementCV.',
)

class CRC1414MeasurementImagesEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415plugin.schema_packages.schemas_measurement.MeasurementImages import (
            m_package,
        )

        return m_package


CRC1415MeasurementImages = CRC1414MeasurementImagesEntryPoint(
    name='CRC1415MeasurementImages',
    description='Schema package for CRC1415 - MeasurementImages.',
)

# class CRCGMSchemaEntryPoint(SchemaPackageEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter here')
# 
#     def load(self):
#         from crc1415testsample.schema_packages.MeasurementGeneric import m_package
# 
#         return m_package
# 
# 
# MeasurementGeneric = CRCGMSchemaEntryPoint(
#     name='CRC1415GM',
#     description='New test schema package for CRC1415 Generic ELN.',
# )
