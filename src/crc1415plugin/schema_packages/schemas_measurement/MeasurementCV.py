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



class CVData(ArchiveSection):
    """General data section for cyclic voltammetry"""

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
                    "data_as_txt_file",
                    "CV_Scanrate",
                ]
            }
        },
    )
    
    name = Quantity(
        type=str,
        #default='TestName',
        description='Name of the section or CV measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'CV: Title of the measurement'},
    )
    
    data_as_txt_file = Quantity(
        type=str,
        description="A reference to an uploaded .txt file produced by the cyclic voltammetry instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
    
    CV_Scanrate = Quantity(
        type=np.float64,
        unit='volt/second',
        description='The scanrate used in the CV experiment, volt/second.',
        a_eln=dict(component='NumberEditQuantity', label='CV: Scanrate', defaultDisplayUnit= 'volt/second'),
    )
    
    CV_Potential = Quantity(
        type=np.float64,
        shape=["*"],
        unit='volt',
        description='The applied potential during the cyclic voltammetry experiment, volt.',
        a_eln=dict(label='CV Potential', defaultDisplayUnit= 'volt'),
    )
    
    CV_Current = Quantity(
        type=np.float64,
        shape=["*"],
        unit='milliampere',
        description='The measured current during the cyclic voltammetry experiment, milliampere',
        a_eln=dict(label='CV Current', defaultDisplayUnit= 'milliampere'),
    )

class MeasurementCV(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of cyclic voltammetry experiment.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-CV',
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
                    "datetime_end",
                    "location",
                    "CV_Electrolyte",
                    "CV_Electrolyte_Concentration",
                    "CV_pH_Value",
                    "CV_Reference_Electrode",
                    "CV_Counter_Electrode_Material",
                    "CV_Working_Electrode_Material",
                    "data_as_ids_file",
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
        description='Name of the section of CV measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'CV: Brief title of the measurement'},
    )
    
    datetime_end = Quantity(
        type=Datetime,
        description='The date and time when this activity has ended.',
        a_eln=dict(component='DateTimeEditQuantity', label='Ending Time'),
    )
    
    CV_Electrolyte = Quantity(
        type=str,
        #default='TestName',
        description='The electrolytes in cyclic voltammetry facilitate ion transport, enabling electrochemical reaction measurements',
        a_eln=dict(component='EnumEditQuantity', label='CV: Electrolyte', suggestions=['KHCO3', 'KCl', 'Na2SO4']),
    )
    
    CV_Electrolyte_Concentration = Quantity(
        type=np.float64,
        unit='mol/l',
        description='The concentration of the electrolytes in cyclic voltammetry, mol/liter.',
        a_eln=dict(component='NumberEditQuantity', label='CV: Electrolyte Concentration', defaultDisplayUnit= 'mol/liter'),
    )
    
    CV_pH_Value = Quantity(
        type=np.float64,
        unit='dimensionless',
        description='The pH value in cyclic voltammetry experiment, dimensionless.',
        a_eln=dict(component='NumberEditQuantity', label='CV: pH Value', defaultDisplayUnit= 'dimensionless'),
    )
    
    CV_Reference_Electrode = Quantity(
        type=str,
        #default='TestName',
        description='The used reference electrode in the experiment.',
        a_eln=dict(component='EnumEditQuantity', label='CV: Reference Electrode', suggestions=['Ag|AgCl (3M)', 'Ag|AgCl (saturated)', 'Hg/Hg2Cl2 (saturated)', 'RHE (reversible hydrogen electrode)']),
    )
    
    CV_Counter_Electrode_Material = Quantity(
        type=str,
        #default='TestName',
        description='The material, which the counter electrode is made of.',
        a_eln=dict(component='EnumEditQuantity', label='CV: Counter Electrode Material', suggestions=['Platinum wire', 'Platinum mesh', 'Graphite', 'Gold']),
    )
    
    CV_Working_Electrode_Material = Quantity(
        type=str,
        #default='TestName',
        description='The material, which the working electrode is made of.',
        a_eln=dict(component='EnumEditQuantity', label='CV: Working Electrode Material', suggestions=['Graphite', 'Glassy carbon', 'Gold', 'Silver']),
    )
    
    
    data_as_ids_file = Quantity(
        type=str,
        description="A reference to an uploaded cyclic voltammetry .ids file produced by the CV instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
    
    CV_data_entries = SubSection(section_def=CVData, repeats=True)
    
    
    def generate_plots(self) -> list[PlotlyFigure]:
        """
        Generate the plotly figures for the `MeasurementCV` section.

        Returns:
            list[PlotlyFigure]: The plotly figures.
        """
        figures = []
        # Create the figure
        fig = go.Figure()
        
        #for r_d_entries in self.Raman_data_entries:
        for idx, r_d_entries in enumerate(self.CV_data_entries):
            #print(f"Index {idx}/{(len(self.Raman_data_entries) - 1)}: {r_d_entries}")
            # Add line plots
            x = r_d_entries.CV_Potential.to(r_d_entries.CV_Potential.units).magnitude
            y = r_d_entries.CV_Current.to(r_d_entries.CV_Current.units).magnitude
            
            
            # Get the Viridis color scale
            viridis_colors = px.colors.sequential.Viridis
            
            color_index_line = int(idx / (len(self.CV_data_entries)-1) * (len(viridis_colors) - 1)) if len(self.CV_data_entries) > 1 else 0
            
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',  # 'lines+markers' to show both lines and markers
                name=f'cycle: {idx}',
                line=dict(color=viridis_colors[color_index_line]), # int(idx / (len(self.Raman_data_entries)) * (len(viridis_colors) - 1))]),
                hovertemplate='(x: %{x}, y: %{y})<extra></extra>',
                marker=dict(size=5, symbol='circle')      # Marker size
            ))

        # exemply use the first entry for the units
        x_label = 'Potential'
        xaxis_title = f'{x_label} ({self.CV_data_entries[0].CV_Potential.units:~})'#(1/cm)' the ':~' gives the short form
        
        y_label = 'Current'
        yaxis_title = f'{y_label} ({self.CV_data_entries[0].CV_Current.units:~})'
        
        fig.update_layout(
            title=f'{y_label} over {x_label} - Cyclic Voltammetry',
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
        
        fig.update_xaxes(showspikes=True,)  # <-- add this line
        fig.update_yaxes(showspikes=True)  # <-- add this line
        
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
        
        self.figures = figures

        return figures
    
    def read_section(self, contentIDSlines, start_line, num_lines):
        section_lines = []
        #with open(file_path, 'r', errors='ignore') as file:
        #contentIDSlines = file_path.readlines()
        for current_line_number, line in enumerate(contentIDSlines, start=1):
            # Check if we are at the starting line
            if current_line_number >= start_line:
                #print(line)
                # Strip whitespace from the line
                stripped_line = line.strip()
                # Check if the line is empty
                if stripped_line == "":
                    break  # Stop if an empty line is encountered
                section_lines.append(stripped_line)  # Add the line to the list
                # Stop if we have read the specified number of lines
                if len(section_lines) >= num_lines:
                    break

        return section_lines
    
    
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
            #Check if there's any CV .ids file provided in main section
            if self.data_as_ids_file:
                if not self.data_as_ids_file.endswith('.ids'):
                    raise DataFileError(f"The file '{self.data_as_ids_file}' must have a .ids extension.")
                
                
                # Otherwise parse the file - ignore the iso8859-15 encoding
                with archive.m_context.raw_file(self.data_as_ids_file,'r', encoding='iso8859-15') as idsfile:
                    positions_startdate = [] # list of data entries position
                    # Load the data from the file
                    contentIDSlines = idsfile.readlines()  # Read all lines into a listidsfile.read()
                    
                    # Read the file line by line and search for 'primary_data'
                    for line_number, line in enumerate(contentIDSlines):
                        #start_index = 0
                        #while True:
                            # Find the next occurrence of the search string
                        found_data = line.find('starttime=')
                            #if found == -1:
                            #    break  # No more occurrences in this line
                            # Store the position as a tuple (line_number, character_position)
                        if found_data >= 0:
                            # first occurrence: start time and date of frame
                            # next line: end time and date of frame
                            positions_startdate.append((line_number, contentIDSlines[line_number], contentIDSlines[line_number+1]))  
                            #start_index += 1  # Move to the next character to continue searching
                            
                    #print(positions_startdate)
                    
                    # Convert Europe/Berlin to UTC
                    import pytz
                    from dateutil import parser as dataparser 
                    # dates:    DD.MM.YYYY HH:MM:SS in Berlin/Europe time zone
                    starttime = positions_startdate[1][1].strip().split("=")[1] # starttime=14.10.2022 16:42:50 -> 14.10.2022 16:42:50
                    exp_time_start = dataparser.parse(starttime, dayfirst=True)
                    
                    local_tz = pytz.timezone('Europe/Berlin')
                    target_tz = pytz.timezone('UTC')
                    
                    exp_time_start = local_tz.localize(exp_time_start) # set to Berlin time
                    exp_time_start = target_tz.normalize(exp_time_start) #transfer to UTC
                    
                    self.datetime = exp_time_start
                    
                    endtime = positions_startdate[len(positions_startdate)-1][2].strip().split("=")[1]
                    exp_time_end = dataparser.parse(endtime, dayfirst=True)
                    
                    exp_time_end = local_tz.localize(exp_time_end) # set to Berlin time
                    exp_time_end = target_tz.normalize(exp_time_end) #transfer to UTC
                    
                    self.datetime_end = exp_time_end
                
                ###
                # Find the 'Scanrate=' in .ids file
                # Find the 'Title=' in .ids file
                ###
                
                positions_scanrate_data = [] # list of data entries position of keyword 'Scanrate=' in Volt/second
                positions_title_data = [] # list of data entries position of keyword 'Title=' for every cycle
                
                # Otherwise parse the file - ignore the iso8859-15 encoding
                with archive.m_context.raw_file(self.data_as_ids_file,'r', encoding='iso8859-15') as idsfile:
                    # Load the data from the file
                    contentIDSlines = idsfile.readlines()  # Read all lines into a listidsfile.read()
                    
                    # Read the file line by line and search for 'primary_data'
                    for line_number, line in enumerate(contentIDSlines):
                        found_data_scanrate = line.find('Scanrate=')
                        found_data_title = line.find('Title=')
                        
                        # Important: the line starts (== 0) with the keyword
                        if found_data_scanrate == 0:
                            positions_scanrate_data.append((line_number, line.strip().split('=')[1]) )  
                        
                        if found_data_title == 0:
                            positions_title_data.append((line_number, line.strip().split('=')[1]) )  

                
                ###
                # Find the position of the data 
                ###
                
                positions_primary_data = [] # list of data entries position
                
                # Otherwise parse the file - ignore the iso8859-15 encoding
                with archive.m_context.raw_file(self.data_as_ids_file,'r', encoding='iso8859-15') as idsfile:
                    # Load the data from the file
                    contentIDSlines = idsfile.readlines()  # Read all lines into a listidsfile.read()
                    
                    # Read the file line by line and search for 'primary_data'
                    for line_number, line in enumerate(contentIDSlines):
                        #start_index = 0
                        #while True:
                            # Find the next occurrence of the search string
                        found_data = line.find('primary_data')
                            #if found == -1:
                            #    break  # No more occurrences in this line
                            # Store the position as a tuple (line_number, character_position)
                        if found_data >= 0:
                            positions_primary_data.append((line_number, int(contentIDSlines[line_number+1].strip('\x00')), int(contentIDSlines[line_number+2].strip()) ))  
                            #start_index += 1  # Move to the next character to continue searching
                        
                #print(positions_primary_data) # the first list is useless
                    
                with archive.m_context.raw_file(self.data_as_ids_file,'r', encoding='iso8859-15') as idsfile:
                    # Load the data from the file
                    contentIDSlines = idsfile.readlines()  # Read all lines into a listidsfile.read()
                    
                    numFrames = len(positions_primary_data)-1 # the first entry is useless
                    # Create subsection if not existing
                    if not self.CV_data_entries:
                        self.CV_data_entries = []
                        # Ensure the list is long enough
                        while len(self.CV_data_entries) < numFrames:
                            self.CV_data_entries.append(CVData())  # Append a placeholder value
                    
                    # Create new if not sufficient long enough - overwrites the default
                    if len(self.CV_data_entries) < numFrames:
                        self.CV_data_entries = []
                        while len(self.CV_data_entries) < numFrames:
                            self.CV_data_entries.append(CVData())  # Append a placeholder value

                    # Do this for every frame in file
                    for frame in range(1,numFrames+1,1): # omit the first entry and add the last
                        section_lines = self.read_section(contentIDSlines, positions_primary_data[frame][0]+4, positions_primary_data[frame][2])
                        
                        import numpy as np
                        dataxyfile = np.loadtxt(section_lines) # convert the section into data
                        
                        # Separate the columns into two variables and copy to 
                        self.CV_data_entries[frame-1].CV_Potential = ureg.Quantity(dataxyfile[:, 0], 'volt')
                        self.CV_data_entries[frame-1].CV_Current = ureg.Quantity(dataxyfile[:, 1], 'ampere')
                        
                        # Provide the Scanrate (in V/s) used in every run
                        self.CV_data_entries[frame-1].CV_Scanrate = ureg.Quantity(float(positions_scanrate_data[frame][1]), 'volt/second')
                        # Provide the Title of every measurement if not present
                        if self.CV_data_entries[frame-1].name is None:
                            self.CV_data_entries[frame-1].name = positions_title_data[frame][1]
                        
                    
            #Check if any file is provided in any subsection for .txt files
            for r_d_entries in self.CV_data_entries:
                if r_d_entries.data_as_txt_file:
                    # Check if the file has the correct extension: txt or plain 2-column txt
                    # if not r_d_entries.data_as_tvf_or_txt_file.endswith('.tvf') and not r_d_entries.data_as_tvf_or_txt_file.endswith('.txt'):
                    #     raise DataFileError(f"The file '{r_d_entries.data_as_tvf_or_txt_file}' must have a .tvf or .txt extension.")
                    
                    # Otherwise parse the file with *.txt - ignore the iso8859-15 encoding
                    #if r_d_entries.data_as_txt_file.endswith('.txt'):
                    with archive.m_context.raw_file(r_d_entries.data_as_txt_file,'r', errors='ignore') as xyfile:
                            # Load the data from the file
                            import numpy as np
                            dataxyfile = np.loadtxt(xyfile, skiprows=1)
                            
                            # Separate the columns into two variables and copy to 
                            r_d_entries.CV_Potential = ureg.Quantity(dataxyfile[:, 1], 'volt') # dataxydfile[:, 0]  # First column
                            r_d_entries.CV_Current = ureg.Quantity(dataxyfile[:, 2], 'ampere') #dataxydfile[:, 1]  # Second column
                    
                    
            
        except Exception as e:
            logger.error('Invalid file extension for parsing.', exc_info=e)
        
        if self.CV_data_entries:
            #Otherwise create plot
            self.figures = self.generate_plots()
        
        super().normalize(archive, logger)

 
