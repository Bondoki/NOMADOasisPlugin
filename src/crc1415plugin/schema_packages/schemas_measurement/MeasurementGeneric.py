import plotly.express as px
import plotly.graph_objects as go

import numpy as np
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
from nomad.datamodel.metainfo.eln import ELNSubstance
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
    

#from crc1415testsample.schema_packages.ELNSample2_schema import CRC1415Category
#from crc1415testsample.schema_packages.ELNSample2_schema import CRC1415Category
#m_package = SchemaPackage(name='CRC1415 Generic ELN')



class GenericData(ArchiveSection):
    """General data section for Raman spectroscopy"""

    m_def = Section(
        label_quantity='name',
        a_eln={
            "properties": {
                "order": [
                    "name",
                    "data_as_txt_file",
                    "Generic_Data_X",
                    "Generic_Data_Y",
                ]
            }
        },
    )
    
    name = Quantity(
        type=str,
        #default='TestName',
        description='Name of the section or generic data.',
        a_eln={'component': 'StringEditQuantity'},
    )
    
    
    data_as_txt_file = Quantity(
        type=str,
        description="A reference to an uploaded generic data .txt file containing two column for x-y values.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
        
    Generic_Data_X = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The generic data on x-axis of the data set,dimensionless.',
    )
    Generic_Data_Y = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The generic data on y-axis of the data set, dimensionless.',
    )

class CRC1415CategoryReleaseCandidate(EntryDataCategory):
    """
    A category for all plugins defined in the `crc1415-plugin` plugin.
    """

    m_def = Category(label='CRC1415-ReleaseCandidate', categories=[EntryDataCategory])

class MeasurementGeneric(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of MeasurementGeneric.
    '''
    m_def = Section(
        categories=[CRC1415CategoryReleaseCandidate],
        label='CRC1415-Measurement-Generic',
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
                    "Generic_Data_as_zip_file",
                    "Generic_X_Unit",
                    "Generic_Y_Unit",
                    "Generic_Title_Label",
                    "Generic_X_Axis_Label",
                    "Generic_Y_Axis_Label",
                    "description"
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
        description='A descriptive text for naming the section.',
        a_eln=dict(component='StringEditQuantity', label='Descriptive Name'),
    )
    
    Generic_X_Unit  = Quantity(
        type=str,
        description='The unit of the generic x-values.',
        a_eln=dict(component='EnumEditQuantity', label='X Unit', suggestions=['dimensionless', 'meter', 'second', 'watt', '1/meter', '1/second', '1/watt']),
    )
    
    Generic_Y_Unit  = Quantity(
        type=str,
        description='The unit of the generic y-values.',
        a_eln=dict(component='EnumEditQuantity', label='Y Unit', suggestions=['dimensionless', 'meter', 'second', 'watt', '1/meter', '1/second', '1/watt']),
    )
    
    Generic_Title_Label  = Quantity(
        type=str,
        description='The title of the plot.',
        a_eln=dict(component='StringEditQuantity', label='Plot: Title Label'),
    )
    
    Generic_X_Axis_Label  = Quantity(
        type=str,
        description='The label of the x-axis in the plot.',
        a_eln=dict(component='StringEditQuantity', label='Plot: X Axis Label'),
    )
    
    Generic_Y_Axis_Label  = Quantity(
        type=str,
        description='The label of the y-axis in the plot.',
        a_eln=dict(component='StringEditQuantity', label='Plot: Y Axis Label'),
    )
    
    
    Generic_Data_as_zip_file = Quantity(
        type=str,
        description="A reference to an uploaded .zip archive of processed data containing plain x-y-value table as .txt files.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity",
            "label": "Processed data as zip archive"
        },
    )
    
    
    Generic_data_entries = SubSection(section_def=GenericData, repeats=True)
    
    
    def generate_plots(self) -> list[PlotlyFigure]:
        """
        Generate the plotly figures for the `MeasurementRaman` section.

        Returns:
            list[PlotlyFigure]: The plotly figures.
        """
        figures = []
        
        ##
        # Create the figure - processed data
        ##
        if self.Generic_data_entries:
            figProcessedData = go.Figure()
            
            #for r_d_entries in self.Raman_data_entries:
            for idx, r_d_entries in enumerate(self.Generic_data_entries):
                #print(f"Index {idx}/{(len(self.Raman_data_entries) - 1)}: {r_d_entries}")
                # Add line plots
                x = r_d_entries.Generic_Data_X.to('dimensionless').magnitude
                y = r_d_entries.Generic_Data_Y.to('dimensionless').magnitude
                
                
                # Get the Viridis color scale
                viridis_colors = px.colors.sequential.Viridis
                
                color_index_line = int(idx / (len(self.Generic_data_entries)-1) * (len(viridis_colors) - 1)) if len(self.Generic_data_entries) > 1 else 0
                
                figProcessedData.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines+markers',
                    name=f'frame: {r_d_entries.name}',
                    line=dict(color=viridis_colors[color_index_line]),
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',
                    marker=dict(size=5),      # Marker size
                ))

            # exemply use the first entry for the units
            x_label = self.Generic_X_Axis_Label
            xaxis_title = f'{x_label} ({self.Generic_X_Unit})'
            
            y_label = self.Generic_Y_Axis_Label
            yaxis_title = f'{y_label} ({self.Generic_Y_Unit})'
            
            figProcessedData.update_layout(
                title=f'Processed: {self.Generic_Title_Label}',
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
                hovermode="closest", #"x unified",
                hoverdistance=10,
            )
            
            figure_json = figProcessedData.to_plotly_json()
            figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
            
            figures.append(
                PlotlyFigure(
                    label=f'Processed: {y_label}-{x_label} linear plot',
                    figure=figure_json
                )
            )
        
        
        self.figures = figures

        return figures
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        The normalize function of the `MeasurementRaman` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        # super().normalize(archive, logger)
        #print('Here')
        try:
            # Check if there's any zip file
            if self.Generic_Data_as_zip_file:
                # Check if the file has the correct extension: zip archive with plain 2-column txt
                if not self.Generic_Data_as_zip_file.endswith('.zip'):
                    raise FileNotFoundError(f"The file '{self.Generic_Data_as_zip_file}' must have a .zip extension.")
                
                # Otherwise parse the file
                with archive.m_context.raw_file(self.Generic_Data_as_zip_file,'rb') as zipf:
                    #print(zipf)
                  #= zipf.open()
                    with zipfile.ZipFile(zipf, 'r') as zipArchiveFile:
                        #print(zipArchiveFile.infolist(), " with length ", len(zipArchiveFile.infolist()))
                        
                        # Get the number of expected datasets
                        number_of_processed_frames = len(zipArchiveFile.infolist())
                        
                        # Create subsection if not existing
                        if not self.Generic_data_entries:
                            self.Generic_data_entries = []
                            # Ensure the list is long enough
                            while len(self.Generic_data_entries) < number_of_processed_frames:
                                self.Generic_data_entries.append(GenericData())  # Append a placeholder value
                        
                        # Create new if not sufficient long enough - overwrites the default
                        if len(self.Generic_data_entries) < number_of_processed_frames:
                            self.Generic_data_entries = []
                            while len(self.Generic_data_entries) < number_of_processed_frames:
                                self.Generic_data_entries.append(GenericData())  # Append a placeholder value
                        
                        for index, file_info in enumerate(zipArchiveFile.infolist()):
                            #print(zipfile.infolist())
                            # Loop over every file
                            with zipArchiveFile.open(file_info) as zipFileContent:
                                #content = zipFileContent.read()#.decode('utf-8')  # Decode bytes to string
                                import numpy as np
                                content = np.loadtxt(zipFileContent)
                                
                                self.Generic_data_entries[index].Generic_Data_X = ureg.Quantity(content[:, 0], 'dimensionless')
                                
                                self.Generic_data_entries[index].Generic_Data_Y = ureg.Quantity(content[:, 1], 'dimensionless')
                                
                                if not self.Generic_data_entries[index].name:
                                  self.Generic_data_entries[index].name = file_info.filename
                                #print(f'Content of {file_info.filename}:\n{content}\n')
                                
            #Check if any file is provided in any subsection for .tvb or .txt files
            for r_d_entries in self.Generic_data_entries:
                if r_d_entries.data_as_txt_file:
                    # Check if the file has the correct extension: TriVista tvf or plain 2-column txt
                    if not r_d_entries.data_as_txt_file.endswith('.txt'):
                        #print("Expect Data File Error")
                        raise FileNotFoundError(f"The file '{r_d_entries.data_as_txt_file}' must have a .txt extension.")
                    
                    # Otherwise parse the file with *.txt
                    if r_d_entries.data_as_txt_file.endswith('.txt'):
                        with archive.m_context.raw_file(r_d_entries.data_as_txt_file) as xyfile:
                            # Load the data from the file
                            import numpy as np
                            dataxyfile = np.loadtxt(xyfile)
                            
                            # Separate the columns into two variables and copy to 
                            r_d_entries.Generic_Data_X = ureg.Quantity(dataxyfile[:, 0], 'dimensionless') # First column
                            r_d_entries.Generic_Data_Y = ureg.Quantity(dataxyfile[:, 1], 'dimensionless') # Second column
                            r_d_entries.name = r_d_entries.data_as_txt_file

            
        except Exception as e:
            logger.error('Invalid file parsing error.', exc_info=e)
        
        # if self.Raman_data_entries:
        #Otherwise create plot
        self.figures = self.generate_plots()
        
        super().normalize(archive, logger)

# m_package.__init_metainfo__()
