
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
    
class CRC1415CategoryMeasurement(EntryDataCategory):
    """
    A category for all plugins defined in the `crc1415-plugin` plugin.
    """

    m_def = Category(label='CRC1415-Measurement', categories=[EntryDataCategory])



class MeasurementSEM(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of SEM.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-SEM',
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
                    "name",
                    "data_as_tif_or_tiff_file",
                    "auxiliary_data_file",
                    "SEM_Accelerating_Voltage",
                    "SEM_Magnification",
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
        description='Name of the section of SEM measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'SEM: Brief title of the measurement'},
    )
    
    data_as_tif_or_tiff_file = Quantity(
        type=str,
        shape=["*"],
        description='''
        A reference to an uploaded .tif produced by the SEM instrument.
        ''',
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
        repeats=True,
    )
    
    auxiliary_data_file = Quantity(
        type=str,
        description='''
        A reference to an uploaded .tif produced by the SEM instrument.
        ''',
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity",
            "label": "SEM: Auxiliary metadata file as .txt"
        },
    )
    
    SEM_Accelerating_Voltage = Quantity(
        type=np.float64,
        unit='volt',
        description='The voltage applied in the SEM experiment, volt.',
        a_eln=dict(component='NumberEditQuantity', label='SEM: Accelerating Voltage', defaultDisplayUnit= 'volt'),
    )
    
    SEM_Magnification = Quantity(
        type=np.float64,
        unit='dimensionless',
        description='The magnification used in the SEM experiment, dimensionless.',
        a_eln=dict(component='NumberEditQuantity', label='SEM: Magnification', defaultDisplayUnit= 'dimensionless'),
    )
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        The normalize function of the `MeasurementSEM` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        
        try:
            
            # Check if any file is provided
            if self.data_as_tif_or_tiff_file:
                self.figures = []
                # Loop over all filenames
                for data_file in self.data_as_tif_or_tiff_file: #.split(" "):
                    # Check if the file has the correct extension
                    if not data_file.endswith('.tif'):
                        if not data_file.endswith('.tiff'):
                            raise DataFileError(f"The file '{data_file}' must have a .tif or .tiff extension.")
                
                    # Otherwise parse the file as binary
                    # with archive.m_context.raw_file(data_file, 'rb') as imagefile:
                    #    archive.m_context.raw_file(data_file) as xyfile:
                    with archive.m_context.raw_file(data_file, 'rb') as imagefile:
                        with Image.open(imagefile) as img:
                            # Get the size of the image
                            img_width, img_height = img.size
                            # print(f"Width: {img_width}, Height: {img_height}")
                            
                             # Convert the image to RGB (necessary for JPEG)
                            img = img.convert('RGB')
                            # Create a BytesIO object to hold the image data
                            buffered = io.BytesIO()
                            # Save the image to the BytesIO object in JPEG format
                            img.save(buffered, format="JPEG")
                            # Get the byte data
                            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                            # Create the URI image string
                            uri = f"data:image/jpeg;base64,{img_str}"
                            
                            # see https://plotly.com/python/images/#zoom-on-static-images
                            fig = go.Figure()
                            scale_factor = 0.5
                            fig.add_trace(
                                go.Scatter(
                                    x=[0, img_width * scale_factor],
                                    y=[0, img_height * scale_factor],
                                    mode="markers",
                                    marker_opacity=0
                                )
                            )
                            # Configure axes
                            fig.update_xaxes(
                                visible=False,
                                range=[0, img_width * scale_factor]
                            )

                            fig.update_yaxes(
                                visible=False,
                                range=[0, img_height * scale_factor],
                                # the scaleanchor attribute ensures that the aspect ratio stays constant
                                scaleanchor="x"
                            )
                            
                            # Add image
                            fig.add_layout_image(
                                dict(
                                    x=0,
                                    sizex=img_width * scale_factor,
                                    y=img_height * scale_factor,
                                    sizey=img_height * scale_factor,
                                    xref="x",
                                    yref="y",
                                    opacity=1.0,
                                    layer="below",
                                    sizing="stretch",
                                    source=uri)
                            )
                            # Configure other layout
                            fig.update_layout(
                                width=img_width * scale_factor,
                                height=img_height * scale_factor,
                                margin={"l": 0, "r": 0, "t": 0, "b": 0},
                            )
                            
                            figure_json = fig.to_plotly_json()
                            figure_json['config'] = {'staticPlot': True, 'displayModeBar': False, 'scrollZoom': True, 'responsive': False, 'displaylogo': False, 'dragmode': False}
                            #self.figures.append(PlotlyFigure(label='Measurement SEM', index=0, figure=figure_json))
                            # label=f'{y_label} linear plot',
                            self.figures.append(PlotlyFigure(label=f'Measurement SEM: {data_file}', figure=figure_json))
                            #self.figures = [PlotlyFigure(label=f'Measurement SEM: {data_file}', index=0, figure=figure_json)]
                
            if self.auxiliary_data_file:
                if not self.auxiliary_data_file.endswith('.txt'):
                    raise DataFileError(f"The file '{self.auxiliary_data_file}' must have a .txt extension.")
                
                # Otherwise parse the file as binary
                with archive.m_context.raw_file(self.auxiliary_data_file, 'r') as txtfile:
                    
                    text = txtfile.read()
                    
                    AV = re.search(r'(AcceleratingVoltage)=([\d.]+)\s+(\w+)', text, re.IGNORECASE)
                    
                    if AV:
                        self.SEM_Accelerating_Voltage = ureg.Quantity(float(AV.group(2)), AV.group(3).lower()) # decimal number, volt
                    
                    MG = re.search(r'(Magnification)=([\d.]+)', text, re.IGNORECASE)
                    
                    if MG:
                        self.SEM_Magnification = ureg.Quantity(float(MG.group(2)), 'dimensionless') # decimal number
                        
                    DATE = re.search(r'Date=([\d.]+)/([\d.]+)/([\d.]+)', text, re.IGNORECASE) # MM/DD/YYYY
                    TIME = re.search(r'Time=([\d.]+):([\d.]+):([\d.]+)', text, re.IGNORECASE) # HH:MM:SS
                    
                    if DATE and TIME:
                        import pytz
                        import datetime
                        # Should follow:    DD-MM-YYYY HH:MM:SS in Berlin/Europe time zone
                        exp_time = datetime.datetime(int(DATE.group(3)),
                                                     int(DATE.group(1)),
                                                     int(DATE.group(2)),
                                                     int(TIME.group(1)),
                                                     int(TIME.group(2)),
                                                     int(TIME.group(3)))
                        
                        local_tz = pytz.timezone('Europe/Berlin')
                        target_tz = pytz.timezone('UTC')
                        
                        exp_time = local_tz.localize(exp_time) # set to Berlin time
                        exp_time = target_tz.normalize(exp_time) #transfer to UTC
                        
                        self.datetime = exp_time
                
                
                
                
            
        except Exception as e:
            logger.error('Invalid file extension for parsing.', exc_info=e)
        # In case something is odd here -> just return
        # if not self.results:
        #    return
        
        # Otherwise create plot
        #self.figures = self.generate_plots()
        super().normalize(archive, logger)
