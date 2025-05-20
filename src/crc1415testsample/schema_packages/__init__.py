from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from crc1415testsample.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
)


class CRC1414SchemaEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from crc1415testsample.schema_packages.CRC1415_A04_schema import m_package

        return m_package


CRC1415_A04_schema = CRC1414SchemaEntryPoint(
    name='CRC1415Schema',
    description='New test schema package for CRC1415.',
)

class CRC1414SampleEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter for sample')

    def load(self):
        from crc1415testsample.schema_packages.ELNSample2_schema import m_package

        return m_package


CRC1415Chemical = CRC1414SampleEntryPoint(
    name='CRC1415Chemical',
    description='New test sample2 package for CRC1415.',
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
