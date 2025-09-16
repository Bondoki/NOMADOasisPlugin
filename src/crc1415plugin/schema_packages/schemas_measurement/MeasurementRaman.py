
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
from PIL import Image
import base64
import io
import pint
import struct # for binary files

import os    

import re
import json

import zipfile

from nomad.datamodel.metainfo.plot import PlotSection
from nomad.datamodel.metainfo.eln import ELNMeasurement
#from nomad.parsing.tabular import TableData
from nomad.datamodel.data import UserReference, AuthorReference
from nomad.datamodel.metainfo.eln import BasicEln
from nomad.datamodel.metainfo.basesections.v1 import ReadableIdentifiers
from nomad.datamodel.metainfo.basesections.v1 import PureSubstance
from nomad.datamodel.metainfo.basesections.v1 import PureSubstanceSection
from nomad.datamodel.metainfo.eln import ELNInstrument
from nomad.datamodel.metainfo.eln import Chemical
from nomad.datamodel.data import EntryData


from typing import (
    TYPE_CHECKING,
)
from nomad.metainfo import (
    MSection,
    Package,
    SchemaPackage,
    Quantity,
    SubSection,
    MEnum,
    Reference,
    Datetime,
    Section,
)
from nomad.datamodel.data import (
    EntryData,
    ArchiveSection,
)
from nomad.datamodel.data import (
    EntryDataCategory,
)
from nomad.metainfo.metainfo import (
    Category,
)
from nomad.units import ureg
from nomad.datamodel.metainfo.plot import (
    PlotlyFigure,
    PlotSection,
)
from nomad.config import config
# from nomad.metainfo.elasticsearch_extension import (
#     Elasticsearch,
#     material_entry_type,
#     entry_type as es_entry_type,
#     create_searchable_quantity,
# )

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )
    
class DataFileError(Exception):
    """Custom exception for data file errors."""
    pass


class CRC1415CategoryMeasurement(EntryDataCategory):
    """
    A category for all plugins defined in the `crc1415-plugin` plugin.
    """

    m_def = Category(label='CRC1415-Measurement', categories=[EntryDataCategory])




class RamanData(ArchiveSection):
    """General data section for Raman spectroscopy"""

    m_def = Section(
        label_quantity='name',
        a_eln={
            # "overview": False,
            # "hide": [
            #     "name",
            #     "lab_id",
            #     "method",
            #     "samples",
            #     "measurement_identifiers"
            # ],
            "properties": {
                "order": [
                    "name",
                    "data_as_tvf_or_txt_file",
                ]
            }
        },
    )
    
    name = Quantity(
        type=str,
        #default='TestName',
        description='Name of the section or Raman measurement',
        a_eln={'component': 'StringEditQuantity'},
    )
    
    
    data_as_tvf_or_txt_file = Quantity(
        type=str,
        description="A reference to an uploaded TriVista .tvf or .txt file produced by the Raman instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
        
    Raman_shift = Quantity(
        type=np.float64,
        shape=["*"],
        unit='1/centimeter',
        description='The wavenumber range of the spectrogram.',
    )
    Intensity = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The intensity or counts at each Raman wavenumber value, dimensionless',
    )
    
class ReferencedRamanData(ArchiveSection):
    """General data section for Raman spectroscopy"""

    m_def = Section(
        label_quantity='name',
        a_eln={
            # "overview": False,
            # "hide": [
            #     "name",
            #     "lab_id",
            #     "method",
            #     "samples",
            #     "measurement_identifiers"
            # ],
            "properties": {
                "order": [
                    "name",
                    "Reference_to_Raman_Data",
                ]
            }
        },
    )
    
    name = Quantity(
        type=str,
        #default='TestName',
        description='Name of the section or brief title',
        a_eln={'component': 'StringEditQuantity'},
    )
    
    Reference_to_Raman_Data = Quantity(
        type='RamanData',
        description='If you want to plot the data, then reference it here.',
        a_eln={
            "component": "ReferenceEditQuantity"
        },
        shape=["*"],
    )
    
    

class MeasurementRaman(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of Raman spectroscopy.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-Raman',
        a_eln={
            "overview": True,
            "hide": [
                #"name",
                "lab_id",
                "method",
                "samples",
                "measurement_identifiers"
            ],
            "properties": {
                "order": [
                    "tags",
                    "name",
                    "datetime",
                    "location",
                    "data_as_tvb_file",
                    "processed_data_as_zip_file",
                    "Laser_Excitation_Wavelength",
                    "Laser_Power",
                    "Ramification_Objective",
                    "Groove_Density",
                    "Accumulation_Time",
                    "No_of_Accumulations",
                    "description",
                    "Raman_data_entries",
                    "Raman_processed_data_entries",
                    "Raman_referenced_data_entries",
                ]
            }
        },
        )
            
    lab_id = Quantity(
        type=str,
        a_display={
            "visible": False
        },
    )
        
    name = Quantity(
        type=str,
        #default='TestName',
        description='Name of the section of Raman measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'Raman: Brief title of the measurement'},
    )
    
    Laser_Excitation_Wavelength = Quantity(
        type=np.float64,
        unit='nanometer',
        description='The wavelength of the laser for Raman spectroscopy, nanometer.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Laser Excitation Wavelength', defaultDisplayUnit= 'nanometer'),
    )
    
    Laser_Power = Quantity(
        type=np.float64,
        unit='milliwatt',
        description='The power of the laser for Raman spectroscopy, mW.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Laser Power', defaultDisplayUnit= 'milliwatt'),
    )
    
    Ramification_Objective = Quantity(
        type=np.float64,
        unit='dimensionless',
        description='The ramification of the objective for the laser in Raman spectroscopy, dimensionless.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Ramification Objective', defaultDisplayUnit= 'dimensionless'),
    )
    
    Groove_Density = Quantity(
        type=np.float64,
        unit='1/millimeter',
        description='The number of grooves per area of a grating in Raman spectroscopy, grooves/millimeter.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Groove Density', defaultDisplayUnit= '1/millimeter'),
    )
    
    Accumulation_Time = Quantity(
        type=np.float64,
        unit='second',
        description='The time intervall to average the measurement in the accumation step in Raman spectroscopy, second.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Exposure Time per Accumulation', defaultDisplayUnit= 'second'),
    )
    
    No_of_Accumulations = Quantity(
        type=np.int32,
        unit='dimensionless',
        description='The number of accumulations for one frame during the measurement in Raman spectroscopy, dimensionless.',
        a_eln=dict(component='NumberEditQuantity', label='Raman: Number of Accumulations per Frame', defaultDisplayUnit= 'dimensionless'),
    )
    
    data_as_tvb_file = Quantity(
        type=str,
        description="A reference to an uploaded TriVista binary .tvb produced by the Raman instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity",
            "label": "Raman data as .tvb file"
        },
    )
        
    processed_data_as_zip_file = Quantity(
        type=str,
        description="A reference to an uploaded .zip archive of processed data containing plain x-y-value table as .txt files.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity",
            "label": "Processed Raman data as .zip archive"
        },
    )
    
    
    Raman_data_entries = SubSection(section_def=RamanData, repeats=True)
    
    Raman_processed_data_entries = SubSection(section_def=RamanData, repeats=True)
    
    Raman_referenced_data_entries = SubSection(section_def=ReferencedRamanData)#, repeats=True)
    
    
    def generate_plots(self) -> list[PlotlyFigure]:
        """
        Generate the plotly figures for the `MeasurementRaman` section.

        Returns:
            list[PlotlyFigure]: The plotly figures.
        """
        figures = []
        ##
        # Create the figure - messured data
        ##
        if self.Raman_data_entries:
            fig = go.Figure()
            
            #for r_d_entries in self.Raman_data_entries:
            for idx, r_d_entries in enumerate(self.Raman_data_entries):
                #print(f"Index {idx}/{(len(self.Raman_data_entries) - 1)}: {r_d_entries}")
                # Add line plots
                x = r_d_entries.Raman_shift.to('1/centimeter').magnitude
                y = r_d_entries.Intensity.to('dimensionless').magnitude
                
                
                # Get the Viridis color scale
                viridis_colors = px.colors.sequential.Viridis
                
                color_index_line = int(idx / (len(self.Raman_data_entries)-1) * (len(viridis_colors) - 1)) if len(self.Raman_data_entries) > 1 else 0
                
                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    name=f'frame: {idx}',
                    line=dict(color=viridis_colors[color_index_line]), # int(idx / (len(self.Raman_data_entries)) * (len(viridis_colors) - 1))]),
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',
                ))

            # exemply use the first entry for the units
            x_label = 'Raman shift'
            xaxis_title = f'{x_label} ({self.Raman_data_entries[0].Raman_shift.units:~})'#(1/cm)' the ':~' gives the short form
            
            y_label = 'Intensity'
            yaxis_title = f'{y_label} (a.u.)'
            
            fig.update_layout(
                title=f'{y_label} over {x_label}',
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                xaxis=dict(
                    fixedrange=False,
                ),
                yaxis=dict(
                    fixedrange=False,
                ),
                #legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
                template='plotly_white',
                showlegend=True,
                hovermode="x unified",
            )

            # figures.append(
            #     PlotlyFigure(
            #         label=f'{y_label}-{x_label} linear plot',
            #         #index=0,
            #         figure=fig.to_plotly_json(),
            #     ),
            # )
            
            figure_json = fig.to_plotly_json()
            figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
            
            figures.append(
                PlotlyFigure(
                    label=f'{y_label}-{x_label} linear plot',
                    figure=figure_json
                )
            )
        
        ##
        # Create the figure - processed data
        ##
        if self.Raman_processed_data_entries:
            figProcessedData = go.Figure()
            
            #for r_d_entries in self.Raman_data_entries:
            for idx, r_d_entries in enumerate(self.Raman_processed_data_entries):
                #print(f"Index {idx}/{(len(self.Raman_data_entries) - 1)}: {r_d_entries}")
                # Add line plots
                x = r_d_entries.Raman_shift.to(r_d_entries.Raman_shift.units).magnitude
                y = r_d_entries.Intensity.to('dimensionless').magnitude
                
                
                # Get the Viridis color scale
                viridis_colors = px.colors.sequential.Viridis
                
                color_index_line = int(idx / (len(self.Raman_processed_data_entries)-1) * (len(viridis_colors) - 1)) if len(self.Raman_processed_data_entries) > 1 else 0
                
                figProcessedData.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    name=f'frame: {idx}',
                    line=dict(color=viridis_colors[color_index_line]), # int(idx / (len(self.Raman_data_entries)) * (len(viridis_colors) - 1))]),
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',
                ))

            # exemply use the first entry for the units
            x_label = 'Raman shift'
            xaxis_title = f'{x_label} ({self.Raman_processed_data_entries[0].Raman_shift.units:~})'#(1/cm)' the ':~' gives the short form
            
            y_label = 'Intensity'
            yaxis_title = f'{y_label} (a.u.)'
            
            figProcessedData.update_layout(
                title=f'Processed: {y_label} over {x_label}',
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                xaxis=dict(
                    fixedrange=False,
                ),
                yaxis=dict(
                    fixedrange=False,
                ),
                #legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
                template='plotly_white',
                showlegend=True,
                hovermode="x unified",
            )

            # figures.append(
            #     PlotlyFigure(
            #         label=f'{y_label}-{x_label} linear plot',
            #         #index=0,
            #         figure=fig.to_plotly_json(),
            #     ),
            # )
            
            figure_json = figProcessedData.to_plotly_json()
            figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
            
            figures.append(
                PlotlyFigure(
                    label=f'Processed: {y_label}-{x_label} linear plot',
                    figure=figure_json
                )
            )
        
        ##
        # Create the figure - referenced data
        ##
        if self.Raman_referenced_data_entries:
            
            # if theres is any referenced data
            if self.Raman_referenced_data_entries.Reference_to_Raman_Data:
                
                figReferencedData = go.Figure()
                
                for idx, r_d_entries in enumerate(self.Raman_referenced_data_entries.Reference_to_Raman_Data):
                    #print(f"Index {idx}/{(len(self.Raman_data_entries) - 1)}: {r_d_entries}")
                    # Add line plots
                    x = r_d_entries.Raman_shift.to(r_d_entries.Raman_shift.units).magnitude
                    y = r_d_entries.Intensity.to('dimensionless').magnitude
                    
                    
                    # Get the Viridis color scale
                    viridis_colors = px.colors.sequential.Viridis
                    
                    color_index_line = int(idx / (len(self.Raman_referenced_data_entries.Reference_to_Raman_Data)-1) * (len(viridis_colors) - 1)) if len(self.Raman_referenced_data_entries.Reference_to_Raman_Data) > 1 else 0
                    
                    figReferencedData.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        mode='lines',
                        name=f'frame: {r_d_entries.name}',
                        line=dict(color=viridis_colors[color_index_line]), # int(idx / (len(self.Raman_data_entries)) * (len(viridis_colors) - 1))]),
                        hovertemplate='(x: %{x}, y: %{y})<extra></extra>',
                    ))

                # exemply use the first entry for the units
                x_label = 'Raman shift'
                xaxis_title = f'{x_label} (1/cm)'#(1/cm)' the ':~' gives the short form
                
                y_label = 'Intensity'
                yaxis_title = f'{y_label} (a.u.)'
                
                figReferencedData.update_layout(
                    title=f'Compare: {y_label} over {x_label}',
                    xaxis_title=xaxis_title,
                    yaxis_title=yaxis_title,
                    xaxis=dict(
                        fixedrange=False,
                    ),
                    yaxis=dict(
                        fixedrange=False,
                    ),
                    #legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
                    template='plotly_white',
                    showlegend=True,
                    hovermode="x unified",
                )

                # figures.append(
                #     PlotlyFigure(
                #         label=f'{y_label}-{x_label} linear plot',
                #         #index=0,
                #         figure=fig.to_plotly_json(),
                #     ),
                # )
                
                figure_json = figReferencedData.to_plotly_json()
                figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
                
                figures.append(
                    PlotlyFigure(
                        label=f'Compare: {y_label}-{x_label} linear plot',
                        figure=figure_json
                    )
                )
        
        
        self.figures = figures

        return figures
    
    def unpack_repeated_bytes(self, byte_data, data_type, count, littleEndianEncoding=True):
        """
        Unpack a series of bytes into a tuple of the same data type.
        'i': Integer (4 bytes)
        'I': Unsigned Int (4 bytes)
        'l': Long (4 bytes)
        'L': Long (8 bytes)
        'f': Float (4 bytes)
        'd': Double (8 bytes)
        'h': Short (2 bytes)
        'b': Signed char (1 byte)
        'B': Unsigned char (1 byte)
        'q': Long long (8 bytes)
        'Q': Unsigned long long (8 bytes)

        :param byte_data: The bytes to unpack.
        :param data_type: The format character for the data type (e.g., 'b' for signed char).
        :param count: The number of items to unpack.
        :param littleEndianEncoding: Flag to determine if the data is in little-endian format.
        :return: A tuple of unpacked values.
        """
        # Determine the endianness based on the flag
        endianness = '<' if littleEndianEncoding else '>'
        
        # Create the format string based on the data type, count, and endianness
        format_string = f'{endianness}{count}{data_type}'
        
        # Unpack the byte data using the constructed format string
        return struct.unpack(format_string, byte_data)
    
    def get_non_empty_chunks_separated_by_null(self, data_slice):
        """
        Get all non-empty chunks of data separated by NULL bytes.

        :param data_slice: The slice of data to split.
        :return: A list of bytes objects, each representing a non-empty chunk of data.
        """
        # Split the data by NULL bytes and filter out empty chunks
        return [chunk for chunk in data_slice.split(b'\x00') if chunk]
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        The normalize function of the `MeasurementRaman` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        # super().normalize(archive, logger)
        try:
            #Check if there's any TriVista binary .tvb file provided in main section
            if self.data_as_tvb_file:
                if not self.data_as_tvb_file.endswith('.tvb'):
                    raise DataFileError(f"The file '{self.data_as_tvb_file}' must have a .tvb extension.")
                
                # Otherwise parse the file
                with archive.m_context.raw_file(self.data_as_tvb_file,'rb') as tvbfile:
                    # Load the data from the file
                    contentTVBfile = tvbfile.read()
                    
                    ###
                    # File Type Version
                    ###
                    datasplice = contentTVBfile[0x0000:0x003] # this should be 'tvb'
                    # 'b': Signed char (1 byte)
                    count = len(datasplice)//1 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'b', count)
                    string_output_file_type = ''.join(chr(b) for b in unpacked_data)
                    #print(string_output_file_type)
                    
                    if string_output_file_type != 'tvb':
                        logger.error(f'This reader may not work for tvb file with header: "{string_output_file_type}"')
                    
                    ###
                    # File Info - Frames and Dataset Length
                    ###
                    datasplice = contentTVBfile[0x0004:0x0016] 
                    # 'h': short (2 byte)
                    count = len(datasplice)//2 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'h', count)
                    #print(unpacked_data)
                    
                    numDatasetLength = int(unpacked_data[1])
                    numFrames = int(unpacked_data[5])
                    #print(numDatasetLength, numFrames)
                    
                    ###
                    # LaserExcitationWavelength
                    ###
                    datasplice = contentTVBfile[0x0025:0x002D]
                    # 'd': double (8 byte)
                    count = len(datasplice)//8 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'd', count)
                    #print(unpacked_data)
                    
                    LaserExcitationWavelength = float(unpacked_data[0])
                    
                    self.Laser_Excitation_Wavelength = ureg.Quantity(LaserExcitationWavelength, 'nanometer')
                        
                    #print(LaserExcitationWavelength)
                    
                    ###
                    # Number of Raman Wavelength entries = NRWE
                    ###
                    datasplice = contentTVBfile[0x002D:0x0031] 
                    # 'I': unsigned integer (4 byte)
                    count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'I', count)
                    #print(unpacked_data)
                    
                    NRWE = int(unpacked_data[0])
                    # print(NRWE)
                    
                    ###
                    # List of Raman Wavelength [in nm] convert to Raman Shift = Raman Wavenumber [1/nm]
                    ###
                    datasplice = contentTVBfile[0x0031:0x0031+4*NRWE] 
                    # 'f': float (4 byte)
                    count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'f', count)
                    #print(unpacked_data)
                    
                    import numpy as np
                    RamanWavenumber = (1.0/LaserExcitationWavelength-1.0/np.asarray(unpacked_data, dtype=np.float64)) # in 1/nm
                    #print(RamanWavenumber)
                    
                    ###
                    # Character Length of XML section = CLXML
                    ###
                    datasplice = contentTVBfile[0x1534:0x1538] 
                    # 'I': unsigned integer (4 byte)
                    count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'I', count)
                    #print(unpacked_data)
                    
                    CLXML = int(unpacked_data[0])
                    #print(CLXML)
                    
                    ###
                    # XML part -> Date, LaserPower, Ramification Objective, Groove Density, Exposure_time, Number_Accumlations
                    ###
                    datasplice = contentTVBfile[0x1538:0x1538+1*CLXML]
                    # 'b': Signed char (1 byte)
                    count = len(datasplice)//1 # Number of bytes to unpack (1 for char)
                    #print(count)
                    unpacked_data = self.unpack_repeated_bytes(datasplice, 'b', count)
                    string_output_xml = ''.join(chr(b) for b in unpacked_data)
                    #print(string_output_xml)
                    
                    import xmltodict, json
                    dataxmlfile = xmltodict.parse(string_output_xml)
                    string_experiment_time = dataxmlfile['Info']['Groups']['Group'][0]['Items']['Item']['Value']
                    
                    
                    if dataxmlfile['Info']['Groups']['Group'][1]['Items']['Item'][2]['Name'] == 'Laser-Power':
                        laser_power_str = dataxmlfile['Info']['Groups']['Group'][1]['Items']['Item'][2]['Value'] # 1,178mW
                        
                        # Use regex to separate the number (note the comma) and the unit
                        match = re.match(r'([\d,]+)([a-zA-Z]+)', laser_power_str)
                        if match:
                            number_str, unit_str = match.groups()
                            # Remove commas and convert to float
                            number = float(number_str.replace(',', '.'))
                            #print(number, unit_str)
                            self.Laser_Power = ureg.Quantity(number, unit_str)
                            
                    if dataxmlfile['Info']['Groups']['Group'][1]['Items']['Item'][3]['Name'] == 'Used Objective':
                        objective_str = dataxmlfile['Info']['Groups']['Group'][1]['Items']['Item'][3]['Value'] # 20x
                    
                        match = re.match(r'([\d,]+)([a-zA-Z]+)', objective_str)
                        if match:
                            number_str, unit_str = match.groups()
                            # Remove commas and convert to float
                            number = float(number_str.replace(',', ''))
                            #print(number, unit_str)
                            self.Ramification_Objective = ureg.Quantity(number, 'dimensionless')
                    
                    if dataxmlfile['Info']['Groups']['Group'][3]['Groups']['Group']['Items']['Item'][6]['Name'] == 'Groove_Density':
                        groove_density_str = dataxmlfile['Info']['Groups']['Group'][3]['Groups']['Group']['Items']['Item'][6]['Value'] # 300 g/mm
                    
                        match = re.match(r'([\d\s]+)([a-zA-Z/]+)', groove_density_str)
                        if match:
                            number_str, unit_str = match.groups()
                            # Remove commas and convert to float
                            number = float(number_str.replace(',', ''))
                            #print(number, unit_str)
                            self.Groove_Density = ureg.Quantity(number, '1/millimeter')
                            
                    if dataxmlfile['Info']['Groups']['Group'][4]['Items']['Item'][4]['Name'] == 'Exposure_Time_(ms)':
                        accumulation_time_str = dataxmlfile['Info']['Groups']['Group'][4]['Items']['Item'][4]['Value'] # 10000
                    
                        match = re.match(r'([\d]+)', accumulation_time_str)
                        if match:
                            number_str = match.group(1)
                            number = float(number_str)
                            self.Accumulation_Time = ureg.Quantity(number, 'millisecond')
                            
                    if dataxmlfile['Info']['Groups']['Group'][4]['Items']['Item'][6]['Name'] == 'No_of_Accumulations':
                        accumulation_number_str = dataxmlfile['Info']['Groups']['Group'][4]['Items']['Item'][6]['Value'] # 6
                        
                        match = re.match(r'([\d]+)', accumulation_number_str)
                        if match:
                            number_str = match.group(1)
                            number = int(number_str)
                            self.No_of_Accumulations = ureg.Quantity(number, 'dimensionless')

                    
                    from datetime import datetime
                    dateExpermimentParsed = datetime.strptime(string_experiment_time,'%d.%m.%Y %H:%M')
                    self.datetime = dateExpermimentParsed
                    
                    ###
                    # List of Intensity counts for every frame in file
                    ###
                    offsetHeader = 0x1538+1*CLXML + 3*4 + 8 + 101
                    
                    # Create subsection if not existing
                    if not self.Raman_data_entries:
                        self.Raman_data_entries = []
                        # Ensure the list is long enough
                        while len(self.Raman_data_entries) < numFrames:
                            self.Raman_data_entries.append(RamanData())  # Append a placeholder value
                    
                    # Create new if not sufficient long enough - overwrites the default
                    if len(self.Raman_data_entries) < numFrames:
                        self.Raman_data_entries = []
                        while len(self.Raman_data_entries) < numFrames:
                            self.Raman_data_entries.append(RamanData())  # Append a placeholder value
                    
                    #print(len(self.Raman_data_entries))
                    
                    # Do this for every frame in file
                    for frame in range(0,numFrames,1):
                        #print(frame)
                        datasplice = contentTVBfile[offsetHeader:offsetHeader+4*NRWE] 
                        # 'f': float (4 byte)
                        count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                        #print(count)
                        unpacked_data = self.unpack_repeated_bytes(datasplice, 'f', count)
                        #print(unpacked_data)
                        
                        import numpy as np
                        IntensityCount = np.asarray(unpacked_data, dtype=np.float64)
                        #print(IntensityCount)
                        
                        # Separate the columns into two variables and copy to 
                        self.Raman_data_entries[frame].Raman_shift = ureg.Quantity(RamanWavenumber, '1/nanometer')
                        self.Raman_data_entries[frame].Intensity = ureg.Quantity(IntensityCount, 'dimensionless')
                        
                        offsetHeader += 4*NRWE + 3*4 + 8 + 101 # specific after every frame 
                    
                    
            #Check if any file is provided in any subsection for .tvb or .txt files
            for r_d_entries in self.Raman_data_entries:
                if r_d_entries.data_as_tvf_or_txt_file:
                    # Check if the file has the correct extension: TriVista tvf or plain 2-column txt
                    if not r_d_entries.data_as_tvf_or_txt_file.endswith('.tvf') and not r_d_entries.data_as_tvf_or_txt_file.endswith('.txt'):
                        #print("Expect Data File Error")
                        raise DataFileError(f"The file '{r_d_entries.data_as_tvf_or_txt_file}' must have a .tvf or .txt extension.")
                    
                    # Otherwise parse the file with *.txt
                    if r_d_entries.data_as_tvf_or_txt_file.endswith('.txt'):
                        with archive.m_context.raw_file(r_d_entries.data_as_tvf_or_txt_file) as xyfile:
                            # Load the data from the file
                            import numpy as np
                            dataxyfile = np.loadtxt(xyfile)
                            
                            # Separate the columns into two variables and copy to 
                            r_d_entries.Raman_shift = ureg.Quantity(dataxyfile[:, 0], '1/centimeter') # dataxydfile[:, 0]  # First column
                            r_d_entries.Intensity = ureg.Quantity(dataxyfile[:, 1], 'dimensionless') #dataxydfile[:, 1]  # Second column
                    
                    # Otherwise parse the file with *.tvf
                    if r_d_entries.data_as_tvf_or_txt_file.endswith('.tvf'):
                        with archive.m_context.raw_file(r_d_entries.data_as_tvf_or_txt_file) as xyfile:
                            #Load the data from the file
                            contentxyfile = xyfile.read()
                            
                            #use additional packages
                            import xmltodict, json
                            dataxyfile = xmltodict.parse(contentxyfile)
                            
                            unitWave = dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@Unit'].lower()
                            calibrationLaserWave = float(dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@LaserWave'])
                            r_d_entries.Laser_Excitation_Wavelength = ureg.Quantity(calibrationLaserWave, unitWave)
                            
                            #Read the actual Raman wavelength data
                            RamanWavelength=dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@ValueArray']
                            # first number (=int) gives the number of data entries
                            RamanWavelengthData = [int(x) if x.isdigit() else float(x) for x in RamanWavelength.split('|')]
                            
                            ### Conversion from Wavelength[nm] to Wavenumber[1/cm]
                            # $\Delta \omega [cm^{-1}] = ( \frac{1}{\lambda_{laser}} - \frac{1}{\lambda_{}}) \cdot 10⁷$
                            
                            import numpy as np
                            RamanWavenumber = (1.0/calibrationLaserWave-1.0/np.asarray(RamanWavelengthData[1:], dtype=np.float64)) # in 1/nm
                            
                            # Read-in of Intensity Counts
                            IntensityString = dataxyfile['XmlMain']['Documents']['Document']['Data']['Frame']['#text']
                            Intensity = np.asarray([float(x) for x in IntensityString.split(';')], dtype=np.float64)
                            
                            # Archive the data
                            r_d_entries.Raman_shift = ureg.Quantity(RamanWavenumber, f'1/{unitWave}') # dataxydfile[:, 0]  # First column
                            r_d_entries.Intensity = ureg.Quantity(Intensity, 'dimensionless') #dataxydfile[:, 1]  # Second column
                            
            # Check if there's any zip file
            if self.processed_data_as_zip_file:
                # Check if the file has the correct extension: zip archive with plain 2-column txt
                if not self.processed_data_as_zip_file.endswith('.zip'):
                    raise DataFileError(f"The file '{self.processed_data_as_zip_file}' must have a .zip extension.")
                
                # Otherwise parse the file
                with archive.m_context.raw_file(self.processed_data_as_zip_file,'rb') as zipf:
                    #print(zipf)
                  #= zipf.open()
                    with zipfile.ZipFile(zipf, 'r') as zipArchiveFile:
                        #print(zipArchiveFile.infolist(), " with length ", len(zipArchiveFile.infolist()))
                        
                        # Get the number of expected datasets
                        number_of_processed_frames = len(zipArchiveFile.infolist())
                        
                        # Create subsection if not existing
                        if not self.Raman_processed_data_entries:
                            self.Raman_processed_data_entries = []
                            # Ensure the list is long enough
                            while len(self.Raman_processed_data_entries) < number_of_processed_frames:
                                self.Raman_processed_data_entries.append(RamanData())  # Append a placeholder value
                        
                        # Create new if not sufficient long enough - overwrites the default
                        if len(self.Raman_processed_data_entries) < number_of_processed_frames:
                            self.Raman_processed_data_entries = []
                            while len(self.Raman_processed_data_entries) < number_of_processed_frames:
                                self.Raman_processed_data_entries.append(RamanData())  # Append a placeholder value
                        
                        for index, file_info in enumerate(zipArchiveFile.infolist()):
                            #print(zipfile.infolist())
                            # Loop over every file
                            with zipArchiveFile.open(file_info) as zipFileContent:
                                #content = zipFileContent.read()#.decode('utf-8')  # Decode bytes to string
                                import numpy as np
                                content = np.loadtxt(zipFileContent)
                                
                                self.Raman_processed_data_entries[index].Raman_shift = ureg.Quantity(content[:, 0], '1/centimeter')
                                
                                self.Raman_processed_data_entries[index].Intensity = ureg.Quantity(content[:, 1], 'dimensionless')
                                
                                if self.Raman_processed_data_entries[index].name is None:
                                    self.Raman_processed_data_entries[index].name = file_info.filename
                                #print(f'Content of {file_info.filename}:\n{content}\n')
            
            #Check if any file is provided in any subsection for .tvb or .txt files
            for r_d_entries in self.Raman_processed_data_entries:
                if r_d_entries.data_as_tvf_or_txt_file:
                    # Check if the file has the correct extension: TriVista tvf or plain 2-column txt
                    if not r_d_entries.data_as_tvf_or_txt_file.endswith('.tvf') and not r_d_entries.data_as_tvf_or_txt_file.endswith('.txt'):
                        #print("Expect Data File Error")
                        raise DataFileError(f"The file '{r_d_entries.data_as_tvf_or_txt_file}' must have a .tvf or .txt extension.")
                    
                    # Otherwise parse the file with *.txt
                    if r_d_entries.data_as_tvf_or_txt_file.endswith('.txt'):
                        with archive.m_context.raw_file(r_d_entries.data_as_tvf_or_txt_file) as xyfile:
                            # Load the data from the file
                            import numpy as np
                            dataxyfile = np.loadtxt(xyfile)
                            
                            # Separate the columns into two variables and copy to 
                            r_d_entries.Raman_shift = ureg.Quantity(dataxyfile[:, 0], '1/centimeter') # dataxydfile[:, 0]  # First column
                            r_d_entries.Intensity = ureg.Quantity(dataxyfile[:, 1], 'dimensionless') #dataxydfile[:, 1]  # Second column
                    
                    # Otherwise parse the file with *.tvf
                    if r_d_entries.data_as_tvf_or_txt_file.endswith('.tvf'):
                        with archive.m_context.raw_file(r_d_entries.data_as_tvf_or_txt_file) as xyfile:
                            #Load the data from the file
                            contentxyfile = xyfile.read()
                            
                            #use additional packages
                            import xmltodict, json
                            dataxyfile = xmltodict.parse(contentxyfile)
                            
                            unitWave = dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@Unit'].lower()
                            calibrationLaserWave = float(dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@LaserWave'])
                            r_d_entries.Laser_Excitation_Wavelength = ureg.Quantity(calibrationLaserWave, unitWave)
                            
                            #Read the actual Raman wavelength data
                            RamanWavelength=dataxyfile['XmlMain']['Documents']['Document']['xDim']['Calibration']['@ValueArray']
                            # first number (=int) gives the number of data entries
                            RamanWavelengthData = [int(x) if x.isdigit() else float(x) for x in RamanWavelength.split('|')]
                            
                            ### Conversion from Wavelength[nm] to Wavenumber[1/cm]
                            # $\Delta \omega [cm^{-1}] = ( \frac{1}{\lambda_{laser}} - \frac{1}{\lambda_{}}) \cdot 10⁷$
                            
                            import numpy as np
                            RamanWavenumber = (1.0/calibrationLaserWave-1.0/np.asarray(RamanWavelengthData[1:], dtype=np.float64)) # in 1/nm
                            
                            # Read-in of Intensity Counts
                            IntensityString = dataxyfile['XmlMain']['Documents']['Document']['Data']['Frame']['#text']
                            Intensity = np.asarray([float(x) for x in IntensityString.split(';')], dtype=np.float64)
                            
                            # Archive the data
                            r_d_entries.Raman_shift = ureg.Quantity(RamanWavenumber, f'1/{unitWave}') # dataxydfile[:, 0]  # First column
                            r_d_entries.Intensity = ureg.Quantity(Intensity, 'dimensionless') #dataxydfile[:, 1]  # Second column
                            


            
        except Exception as e:
            logger.error('Invalid file parsing error.', exc_info=e)
        
        # if self.Raman_data_entries:
        #Otherwise create plot
        self.figures = self.generate_plots()
        
        super().normalize(archive, logger)
