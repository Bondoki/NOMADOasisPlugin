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



class MeasurementTGA(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of ThermoGravimetricAnalysis.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-TGA',
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
                    "data_as_txt_file",
                    "TGA_Sample_Mass",
                    "TGA_Temperature_Start",
                    "TGA_Temperature_End",
                    "TGA_Rate",
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
        description='Name of the section of TGA measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'TGA: Brief title of the measurement'},
    )
    
    data_as_txt_file = Quantity(
        type=str,
        description="A reference to an uploaded Quantachrome .txt produced by the TGA instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity",
            "label": "data as .txt file of TGA experiment"
        },
    )
    
    TGA_Rate= Quantity(
        type=np.float64,
        unit='kelvin/minute',
        description='The rate for temperature increase during the TGA, kelvin per minute.',
        a_eln=dict(component='NumberEditQuantity', label='TGA Rate', defaultDisplayUnit= 'kelvin/minute'),
    )
    
    TGA_Temperature_Start = Quantity(
        type=np.float64,
        unit='celsius',
        description='The starting temperature for the TGA, celsius.',
        a_eln=dict(component='NumberEditQuantity', label='TGA Temperature Start', defaultDisplayUnit= 'celsius'),
    )
    
    TGA_Temperature_End = Quantity(
        type=np.float64,
        unit='celsius',
        description='The ending temperature for the TGA, celsius.',
        a_eln=dict(component='NumberEditQuantity', label='TGA Temperature End', defaultDisplayUnit= 'celsius'),
    )
    
    
    TGA_Sample_Mass = Quantity(
        type=np.float64,
        unit='milligram',
        description='The mass of the sample in the TGA, milligram.',
        a_eln=dict(component='NumberEditQuantity', label='TGA Sample Mass', defaultDisplayUnit= 'milligram'),
    )
    
    TGA_Temperature = Quantity(
        type=np.float64,
        shape=["*"],
        unit='celsius',
        description='The temperature in the TGA, celsius.',
        a_eln=dict(defaultDisplayUnit = 'celsius'),
    )
    
    
    TGA_Mass_Subtrate = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The measured mass at temperature in the TGA, given in percent.',
        a_eln=dict(defaultDisplayUnit = 'dimensionless'),
    )
    
    
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        The normalize function of the `MeasurementTGA` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        
        try:
            # Check if any file is provided
            if self.data_as_txt_file:
                # Check if the file has the correct extension
                if not self.data_as_txt_file.endswith('.txt'):
                    raise DataFileError(f"The file '{self.data_as_txt_file}' must have a TGA .txt extension.")
            
                # Get the encoding
                # from chardet import detect # for Quantachrome ASiQwin text as the file has the 'Windows-1252' encoding
                # # but this can usally ignored as the only character is the Angstrom 
                
                # with archive.m_context.raw_file(self.data_as_txt_file, 'rb') as txtfile:
                #     rawdata = txtfile.read()
                #     get_encoding_type = detect(rawdata)['encoding']
                #     print(get_encoding_type)
                
                #with archive.m_context.raw_file(self.data_as_txt_file, 'r', errors='ignore') as txtfile:
                with archive.m_context.raw_file(self.data_as_txt_file, 'r', encoding='iso8859-15') as txtfile:
                    # parse the metadata
                    text = txtfile.read()
                    #print(text)
                    
                    mass = re.search(r'#SAMPLE MASS /(\w+):(\d+),(\d+)', text, re.IGNORECASE)
                    
                    if mass:
                        if len(mass.groups()) == 3:
                            # Combine them to form the complete number
                            mass_decimal = f"{mass.group(2)}.{mass.group(3)}"  # Convert to standard decimal format
                            self.TGA_Sample_Mass = ureg.Quantity(float(mass_decimal), mass.group(1).lower()) # decimal[comma]decimal, mg
                    
                    temp_range = re.search(r'#RANGE:(\d+)(°C)/([\d.]+)\((K/min)\)/(\d+)(°C)', text)
                    #print(temp_range)
                    #print(len(temp_range.groups()))
                    #print(temp_range.groups())
                    
                    if temp_range:
                        if len(temp_range.groups()) == 6: # start, degC, rate, K/min, stop, degC
                            
                            self.TGA_Temperature_Start = ureg.Quantity(float(temp_range.group(1)), temp_range.group(2))  # decimal, degC
                            
                            self.TGA_Rate = ureg.Quantity(float(temp_range.group(3)), temp_range.group(4).lower().replace('k/min', 'kelvin/minute'))  # decimal, K/min
                            
                            self.TGA_Temperature_End = ureg.Quantity(float(temp_range.group(5)), temp_range.group(6))  # decimal, degC
                    
                    # Use regex to extract the date and time: #DATE/TIME: DD.MM.YYYY HH:MM
                    time_exp = re.search(r'#DATE/TIME:(\d{1,2}\.\d{1,2}\.\d{4}\s+\d{1,2}:\d{1,2})', text)
                    #print(time_exp)
                    # Check if a match was found
                    if time_exp:
                        # Convert the unpacked data as a datetime object
                        from datetime import datetime
                        import pytz
                        exp_time = datetime.strptime(time_exp.group(1), "%d.%m.%Y %H:%M")
                        
                        local_tz = pytz.timezone('Europe/Berlin')
                        target_tz = pytz.timezone('UTC')
                        
                        exp_time = local_tz.localize(exp_time) # set to Berlin time
                        exp_time = target_tz.normalize(exp_time) #transfer to UTC
                        
                        self.datetime = exp_time
                        
                
                with archive.m_context.raw_file(self.data_as_txt_file, 'r', encoding='iso8859-15') as txtfile:
                    # Read-in the special encoded file
                    data_tga = np.loadtxt(txtfile, encoding='iso8859-15', delimiter=';', usecols=[0,3])
                    # Unpack the two columns into separate arrays
                    tga_temperature, tga_mass_percent = data_tga[:, 0], data_tga[:, 1]
                    
                    # note: percent as unit is available at pint v0.22 -> this here is v.17
                    self.TGA_Temperature = ureg.Quantity(tga_temperature, 'celsius')
                    self.TGA_Mass_Subtrate = ureg.Quantity(tga_mass_percent, 'dimensionless')
                    
                    # create plot
                    figures = []
                    
                    # Create a figure
                    fig = go.Figure()
                    
                    x_label = 'Temperature'
                    xaxis_title = 'Temperature [\u2103]'
                    
                    y_label = 'Sample Mass'
                    yaxis_title = 'Sample Mass [%]' #f'Adsorbed Volume [mmol/g] ({self.Analysis_Gas}, {self.Bath_Temperature.to('kelvin').magnitude} {self.Bath_Temperature.units:~})'
                    
                    # Add the first line with markers
                    fig.add_trace(go.Scatter(
                        x=np.array([temp.to('celsius').magnitude for temp in self.TGA_Temperature]), #self.TGA_Temperature.to('celsius').magnitude,
                        y=np.array([mass.to_base_units().magnitude for mass in self.TGA_Mass_Subtrate]), #self.TGA_Mass_Subtrate,
                        mode='lines+markers',  # 'lines+markers' to show both lines and markers
                        name='TGA',         # Name of the first line
                        line=dict(color='blue'),  # Line color
                        hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
                        marker=dict(size=5, symbol='circle')      # Marker size
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
                        hovermode="x unified", # provides a dashed line and finds the closest point
                    )
                    
                    # figures.append(
                    #     PlotlyFigure(
                    #         label=f'{y_label}-{x_label}',
                    #         #index=0,
                    #         figure=fig.to_plotly_json(),
                    #     ),
                    # )
                    
                    figure_json = fig.to_plotly_json()
                    figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
                    
                    figures.append(PlotlyFigure(label=f'{y_label}-{x_label} linear plot', figure=figure_json))
                    
                    self.figures = figures
        
        
        except Exception as e:
            logger.error('Invalid file extension for parsing.', exc_info=e)
        # In case something is odd here -> just return
        # if not self.results:
        #    return
        
        super().normalize(archive, logger)
