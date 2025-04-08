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
