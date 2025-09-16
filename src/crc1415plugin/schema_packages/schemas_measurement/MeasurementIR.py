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

class DataFileError(Exception):
    """Custom exception for data file errors."""
    pass

class CRC1415CategoryMeasurement(EntryDataCategory):
    """
    A category for all plugins defined in the `crc1415-plugin` plugin.
    """

    m_def = Category(label='CRC1415-Measurement', categories=[EntryDataCategory])



class MeasurementIR(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of IR.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-IR',
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
                    "data_as_dpt_file",
                    "IR_Substance_Type",
                    "IR_Solvent",
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
        #default='TestName',
        description='Name of the section of IR measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'IR: Brief title of the measurement'},
    )
    
    data_as_dpt_file = Quantity(
        type=str,
        description="A reference to an uploaded .dpt produced by the IR instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
    
    IR_Substance_Type = Quantity(
        type=MEnum(['in solution', 'powder', 'KBr pellet', 'other']),
        description='The preparation condition of the sample in the IR experiment.',
        a_eln={
            "component": "RadioEnumEditQuantity",
            "label": "IR substance type"
        },
    )
    
    IR_Solvent  = Quantity(
        type=str,
        description='The solvent used for solving the sample in the IR experiment.',
        a_eln=dict(component='EnumEditQuantity', label='IR Solvent', suggestions=['Acetone', 'Acetonitrile (MeCN)', 'DMF (Dimethylformamide)', 'Ethanol', 'Isopropyl alcohol', 'Water']),
    )
    
    Wavenumber = Quantity(
        type=np.float64,
        shape=["*"],
        unit='1/cm',
        description='The wavenumber range of the spectrogram',
        a_eln={
            "defaultDisplayUnit": "1/cm",
        },
    )
    Transmittance = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The transmittance at each wavenumber value, dimensionless',
    )
    
    def generate_plots(self) -> list[PlotlyFigure]:
        """
        Generate the plotly figures for the `MeasurementIR` section.

        Returns:
            list[PlotlyFigure]: The plotly figures.
        """
        figures = []
        #if self.wavelength is None:
        #    return figures

        x_label = 'Wavenumber'
        xaxis_title = f'{x_label} [{self.Wavenumber.units:~}]'
        #x = self.Wavenumber.to('1/cm').magnitude
        x = self.Wavenumber.to(self.Wavenumber.units).magnitude
        
        y_label = 'Transmittance'
        yaxis_title = f'{y_label} (a.u.)'
        y = self.Transmittance.to('dimensionless').magnitude
        
        fig = go.Figure()
        
        # Add the first line with markers
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',  # 'lines+markers' to show both lines and markers
            name='IR',         # Name of the first line
            line=dict(color='blue'),  # Line color
            hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
            marker=dict(size=10, symbol='circle')      # Marker size
        ))
        
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
            template='plotly_white',
            showlegend=True,
            hovermode="x unified",
        )
        
        figure_json = fig.to_plotly_json()
        
        figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
        
        figures.append(PlotlyFigure(label=f'{y_label}-{x_label} linear plot', figure=figure_json))
        
        self.figures = figures
        
        return figures
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        The normalize function of the `MeasurementIR` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        
        try:
            # Check if any file is provided
            if self.data_as_dpt_file:
                # Check if the file has the correct extension
                if not self.data_as_dpt_file.endswith('.dpt'):
                    raise DataFileError(f"The file '{self.data_as_dpt_file}' must have a .dpt extension.")
            
                # Otherwise parse the file
                with archive.m_context.raw_file(self.data_as_dpt_file) as xyfile:
                    # Load the data from the file
                    dataxyfile = np.loadtxt(xyfile)
                    
                    # Separate the columns into two variables and copy to 
                    self.Wavenumber = ureg.Quantity(dataxyfile[:, 0], '1/cm') # dataxydfile[:, 0]  # First column
                    self.Transmittance = ureg.Quantity(dataxyfile[:, 1], 'dimensionless') #dataxydfile[:, 1]  # Second column
                    
                    # Otherwise create plot
                    self.figures = self.generate_plots()
        
        except Exception as e:
            logger.error('Invalid file extension for parsing.', exc_info=e)
        # In case something is odd here -> just return
        # if not self.results:
        #    return
        
        super().normalize(archive, logger)
 
