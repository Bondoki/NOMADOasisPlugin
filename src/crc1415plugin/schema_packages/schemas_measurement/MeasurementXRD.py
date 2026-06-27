import struct  # for binary files
from typing import (
    TYPE_CHECKING,
)

import numpy as np
import plotly.graph_objects as go
from nomad.datamodel.data import (
    ArchiveSection,
    EntryDataCategory,
)

#from nomad.parsing.tabular import TableData
from nomad.datamodel.metainfo.eln import ELNMeasurement
from nomad.datamodel.metainfo.plot import (
    PlotlyFigure,
    PlotSection,
)
from nomad.metainfo import (
    Datetime,
    Quantity,
    Section,
    SubSection,
)
from nomad.metainfo.metainfo import (
    Category,
)
from nomad.units import ureg

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

class XRD_Data_Entry(ArchiveSection):
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
                    "XRD_Datetime_Start",
                    "XRD_Datetime_End",
                    "XRD_Wavelength",
                    #"data_as_tvf_or_txt_file",
                ]
            }
        },
    )
    
    name = Quantity(
        type=str,
        description='Name of the section or XRD measurement',
        a_eln={'component': 'StringEditQuantity'},
    )
    
    XRD_Datetime_Start = Quantity(
        type=Datetime,
        description='The date and time when this activity has started.',
        a_eln=dict(component='DateTimeEditQuantity', label='Experiment Starting Time'),
    )
    
    XRD_Datetime_End = Quantity(
        type=Datetime,
        description='The date and time when this activity has ended.',
        a_eln=dict(component='DateTimeEditQuantity', label='Experiment Ending Time'),
    )
    
    XRD_Wavelength = Quantity(
        type=np.float64,
        unit='nanometer',
        description='The wavelength of Cu K alpha (1.5406 Angstrom) used for XRD experiment.',
    )
    
    XRD_Deg2Theta = Quantity(
        type=np.float64,
        a_tabular={
            "name": "Deg2Theta"
        },
        shape=["*"],
        unit='deg',
        description='The 2-theta range of the diffractogram',
    )
    XRD_Intensity = Quantity(
        type=np.float64,
        a_tabular={
            "name": "Counts"
        },
        shape=["*"],
        unit='dimensionless',
        description='The count at each 2-theta value, dimensionless',
    )
    


#class XRDMeasurement(ELNMeasurement, TableData, PlotSection, ArchiveSection):
class MeasurementXRD(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of XRD.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-XRD',
        a_eln={
            "overview": True,
            "hide": [
                #"name",
                "lab_id",
                "method",
                "samples",
                "measurement_identifiers",
                "datetime",
            ],
            "properties": {
                "order": [
                    "tags",
                    "name",
                    #"datetime",
                    #"datetime_end",
                    "location",
                    "data_as_raw_or_xyd_file",
                    "data_as_xye_file",
                    "description",
                    "XRD_Data_Entries_Experiment",
                    "XRD_Data_Entries_Simulation",
                ]
            }
        },
        # a_plotly_graph_object=[
        #     {
        #         "data": [
        #             {
        #                 "x": "#Deg2Theta",
        #                 "y": "#Counts"
        #             }
        #         ],
        #         "layout": {
        #             "title": {
        #                 "text": "Counts over Degree 2Theta"
        #             }
        #         }
        #     }
        # ],
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
        description='Name of the section of XRD measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'XRD: Brief title of the measurement'},
    )
    
    data_as_raw_or_xyd_file = Quantity(
        type=str,
        shape=["*"],
        description='''
        A reference to an uploaded .raw or .xyd produced by the XRD instrument.
        ''',
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
        repeats=True,
    )
    
    data_as_xye_file = Quantity(
        type=str,
        shape=["*"],
        description='''
        A reference to an uploaded .xye produced by XRD simulation.
        ''',
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
        repeats=True,
    )
    
    # Experiment_Wavelength = Quantity(
    #     type=np.float64,
    #     unit='nanometer',
    #     description='The wavelength of Cu K alpha (1.5406 Angstrom) used for XRD experiment.',
    # )
    
    # Simulation_Wavelength = Quantity(
    #     type=np.float64,
    #     unit='nanometer',
    #     description='The wavelength of Cu K alpha used for XRD simulations.',
    # )
    
    # Deg2Theta = Quantity(
    #     type=np.float64,
    #     a_tabular={
    #         "name": "Deg2Theta"
    #     },
    #     shape=["*"],
    #     unit='deg',
    #     description='The 2-theta range of the diffractogram',
    # )
    
    # Intensity = Quantity(
    #     type=np.float64,
    #     a_tabular={
    #         "name": "Counts"
    #     },
    #     shape=["*"],
    #     unit='dimensionless',
    #     description='The count at each 2-theta value, dimensionless',
    # )
    
    # Simulated_Deg2Theta = Quantity(
    #     type=np.float64,
    #     shape=["*"],
    #     unit='deg',
    #     description='The 2-theta range of the simulated diffractogram',
    # )
    # Simulated_Intensity = Quantity(
    #     type=np.float64,
    #     shape=["*"],
    #     unit='dimensionless',
    #     description='The simulated count at each 2-theta value, dimensionless',
    # )
    
    XRD_Data_Entries_Experiment = SubSection(section_def=XRD_Data_Entry, repeats=True)
    
    XRD_Data_Entries_Simulation = SubSection(section_def=XRD_Data_Entry, repeats=True)
    
    def generate_plots(self) -> list[PlotlyFigure]:
        """
        Generate the plotly figures for the `MeasurementXRD` section.

        Returns:
            list[PlotlyFigure]: The plotly figures.
        """
        figures = []

        x_label = '2Theta'
        xaxis_title = f'{x_label} (°)'
        
        y_label = 'Normalized Intensity'
        yaxis_title = f'{y_label} (a.u.)'
        
        # line_linear = px.line(x=x, y=y/np.max(y))
        # 
        # line_linear.update_layout(
        #     title=f'{y_label} over {x_label}',
        #     xaxis_title=xaxis_title,
        #     yaxis_title=yaxis_title,
        #     xaxis=dict(
        #         fixedrange=False,
        #     ),
        #     yaxis=dict(
        #         fixedrange=False,
        #     ),
        #     template='plotly_white',
        # )
        # 
        # figures.append(
        #     PlotlyFigure(
        #         label=f'{y_label}-{x_label} linear plot',
        #         index=0,
        #         figure=line_linear.to_plotly_json(),
        #     ),
        # )
        
        config = {'displayModeBar': True}
        
        # Create the figure (for the moment: a blank graph)
        fig = go.Figure()

        # Add the scatter trace
        if self.XRD_Data_Entries_Experiment:
            for idx, xrd_data_entry in enumerate(self.XRD_Data_Entries_Experiment):
                xExp = xrd_data_entry.XRD_Deg2Theta.to('degree').magnitude
                yExp = xrd_data_entry.XRD_Intensity.to('dimensionless').magnitude
                
                short_str = lambda s, k=5: (
                    (lambda t: t[:k] + "..." + t[-k:])(
                    s[:s.rfind(".")] if (i := s.rfind(".")) != -1 and i + 1 < len(s) else s
                    )
                )
                
                fig.add_trace(go.Scatter( 
                    x=xExp, # Variable in the x-axis
                    y=yExp/np.max(yExp), # Variable in the y-axis
                    mode='lines', # This explicitly states that we want our observations to be represented by lines or use 'lines+markers'
                    name= short_str(xrd_data_entry.name) , #'Experiment',
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
                    # Properties associated with points 
                    # marker=dict(
                    #     size=12, # Size
                    #     color='#cb1dd1', # Color
                    #     opacity=0.8, # Point transparency 
                    #     line=dict(width=1, color='black') # Properties of the edges
                    # ),
                ))
            
        if self.XRD_Data_Entries_Simulation:
            for idx, xrd_data_entry in enumerate(self.XRD_Data_Entries_Simulation):
                xSim = xrd_data_entry.XRD_Deg2Theta.to('degree').magnitude
                ySim = xrd_data_entry.XRD_Intensity.to('dimensionless').magnitude
                
                short_str = lambda s, k=5: (
                    (lambda t: t[:k] + "..." + t[-k:])(
                    s[:s.rfind(".")] if (i := s.rfind(".")) != -1 and i + 1 < len(s) else s
                    )
                )
                
                fig.add_trace(go.Scatter( 
                    x=xSim, # Variable in the x-axis
                    y=ySim/np.max(ySim), # Variable in the y-axis
                    mode='lines', # This explicitly states that we want our observations to be represented by lines or use 'lines+markers'
                    name=short_str(xrd_data_entry.name) , #'Simulation',
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
                    # Properties associated with points 
                    # marker=dict(
                    #     size=12, # Size
                    #     color='#cb1dd1', # Color
                    #     opacity=0.8, # Point transparency 
                    #     line=dict(width=1, color='black') # Properties of the edges
                    # ),
                ))
        

        # Customize the layout
        fig.update_layout(
            title=f'{y_label} over {x_label}',
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            showlegend=True,
            xaxis=dict(
                fixedrange=False,
            ),
            yaxis=dict(
                fixedrange=False,
            ),
            template='plotly_white',
            hovermode="x unified", # provides a dashed line and finds the closest point
            
        )
        
        figure_json = fig.to_plotly_json()
        figure_json['config'] = {'staticPlot': False, 'displayModeBar': True, 'scrollZoom': True, 'responsive': True, 'displaylogo': True, 'dragmode': True}
        
        figures.append(PlotlyFigure(label=f'{y_label}-{x_label} linear plot', figure=figure_json))

        return figures
    
    def unpack_repeated_bytes(self, byte_data, data_type, count):
        """
        Unpack a series of bytes into a tuple of the same data type.

        :param byte_data: The bytes to unpack.
        :param data_type: The format character for the data type (e.g., 'b' for signed char).
        :param count: The number of items to unpack.
        :return: A tuple of unpacked values.
        """
        # Create the format string based on the data type and count
        format_string = f'{count}{data_type}'
        
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
        The normalize function of the `MeasurementXRD` section.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        # super().normalize(archive, logger)
        
        try:
            # Check if any file is provided
            
            # Check if any experimental (raw/xyd) or simulation (xye) file is provided
            if self.data_as_raw_or_xyd_file:
                
                num_raw_or_xyd_file = len(self.data_as_raw_or_xyd_file)
                
                # Create subsection if not existing
                if not self.XRD_Data_Entries_Experiment:
                    self.XRD_Data_Entries_Experiment = []
                    # Ensure the list is long enough
                    while len(self.XRD_Data_Entries_Experiment) < num_raw_or_xyd_file:
                        self.XRD_Data_Entries_Experiment.append(XRD_Data_Entry())  # Append a placeholder value
                    
                # Create new if not sufficient long enough - overwrites the default
                if len(self.XRD_Data_Entries_Experiment) < num_raw_or_xyd_file:
                    self.XRD_Data_Entries_Experiment = []
                    while len(self.XRD_Data_Entries_Experiment) < num_raw_or_xyd_file:
                        self.XRD_Data_Entries_Experiment.append(XRD_Data_Entry())  # Append a placeholder value
                
                # Loop over all filenames
                for index, data_file in enumerate(self.data_as_raw_or_xyd_file):
                    # Check if the file has the correct extension
                    if not data_file.endswith('.xyd') and not data_file.endswith('.raw'):
                        raise DataFileError(f"The file '{data_file}' must have a .raw or .xyd extension.")
                    
                    if getattr(self.XRD_Data_Entries_Experiment[index], "name", None) is None:
                        self.XRD_Data_Entries_Experiment[index].name = data_file
                    
                    if data_file.endswith('.xyd'):
                        # Otherwise parse the file
                        with archive.m_context.raw_file(data_file) as xydfile:
                            # Load the data from the file
                            dataxydfile = np.loadtxt(xydfile)
                            
                            # Separate the columns into two variables and copy to 
                            self.XRD_Data_Entries_Experiment[index].XRD_Deg2Theta = ureg.Quantity(dataxydfile[:, 0], 'degree') # dataxydfile[:, 0]  # First column
                            self.XRD_Data_Entries_Experiment[index].XRD_Intensity = ureg.Quantity(dataxydfile[:, 1], 'dimensionless') #dataxydfile[:, 1]  # Second column
                            
                            # Otherwise create plot
                            # self.figures = self.generate_plots()
                            
                    if data_file.endswith('.raw'):
                        # Otherwise parse the file
                        with archive.m_context.raw_file(data_file,'rb') as rawfile:
                            # Load the data from the file
                            contentrawfile = rawfile.read()
                            
                            ###
                            # File Type Version
                            ###
                            count = len(contentrawfile[0x00:0x0D + 1])//1 # Number of bytes to unpack
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(contentrawfile[0x00:0x0D + 1], 'b', count)
                                
                            # Convert unpacked data to a string
                            string_output_file_type = ''.join(chr(b) for b in unpacked_data)
                            
                            if string_output_file_type != 'RAW_1.06Powdat':
                                logger.warn(f'This reader may not work for raw file with header: "{string_output_file_type}"')
                            
                            ###
                            # Date of Experiment
                            ###
    
                            datasplice = contentrawfile[0x0010:0x001F + 1]
                            count = len(datasplice)//1 # Number of bytes to unpack
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(datasplice, 'b', count)
                                
                            # Convert unpacked data to a string
                            string_output_day = ''.join(chr(b) for b in unpacked_data)
                            
                            # Convert the unpacked data as a datetime object
                            from dateutil import parser as dataparser
                            dt = dataparser.parse(string_output_day)
                            
                            import pytz
                            
                            local_tz = pytz.timezone('Europe/Berlin')
                            target_tz = pytz.timezone('UTC')
                            
                            dt = local_tz.localize(dt) # set to Berlin time
                            dt = target_tz.normalize(dt) #transfer to UTC
                            
                            self.datetime = dt
                            self.XRD_Data_Entries_Experiment[index].XRD_Datetime_Start = dt
                            
                            ###
                            # File Name And Comments?
                            ###
                            datasplice = contentrawfile[0x0020:0x012F + 1]
                            
                            # Get all chunks separated by NULL bytes in the data slice
                            chunks = self.get_non_empty_chunks_separated_by_null(datasplice)
                            
                            # Only add description if nothing is there
                            if not self.description:
                                self.description = ''
                                
                                # Print the result chunks
                                for i, chunk in enumerate(chunks):
                                    #print(f'Chunk {i}: {chunk}')
                                    count = len(chunk)//1 # Number of bytes to unpack (1 for char)
                                    unpacked_data = self.unpack_repeated_bytes(chunk, 'b', count)
                                    string_output_description = ''.join(chr(b) for b in unpacked_data)
                                    # Print the unpacked data as a string
                                    # The comments in the file is not needed - uncomment if necessary
                                    # self.description += '<p>'+string_output_description + '</p>\n'
                                    
                                    
                            ###
                            # Experimental setup
                            # Copper K Alpha x-ray wavelength of 1.5406 Angstrom used by the experiment.
                            ###
                            datasplice = contentrawfile[0x0142:0x0146]
                            #'i': Integer (4 bytes)
                            #'f': Float (4 bytes)
                            #'d': Double (8 bytes)
                            #'h': Short (2 bytes)
                            count = len(datasplice)//4 # Number of bytes to unpack (4 for float)
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(datasplice, 'f', count)
                            #print(unpacked_data)
                            
                            # self.Experiment_Wavelength = ureg.Quantity(float(unpacked_data[0]), 'angstrom')
                            self.XRD_Data_Entries_Experiment[index].XRD_Wavelength = ureg.Quantity(float(unpacked_data[0]), 'angstrom')
                            
                            ###
                            # Start and End Time
                            ###
                            datasplice = contentrawfile[4*0x10000+0x0600:4*0x10000+0x0620]
                            #print(datasplice)
                            # Get all chunks separated by NULL bytes in the data slice
                            chunks = self.get_non_empty_chunks_separated_by_null(datasplice)
                                
                            # Print the result chunks
                            # for i, chunk in enumerate(chunks):
                            #     print(f'Chunk {i}: {chunk}')
                            #     count = len(chunk)//1 # Number of bytes to unpack (1 for char)
                            #     unpacked_data = self.unpack_repeated_bytes(chunk, 'b', count)
                            #     string_output_time = ''.join(chr(b) for b in unpacked_data)
                            #     # Print the unpacked data as a string
                            #     print(string_output_time)
                            #
                            # print(len(chunks), chunks[1])
                            
                            
                            if len(chunks) > 1:
                                count = len(chunks[1])//1 # Number of bytes to unpack (1 for char)
                                unpacked_data = self.unpack_repeated_bytes(chunks[1], 'b', count)
                                string_output_time = ''.join(chr(b) for b in unpacked_data)
                                
                                from dateutil import parser as dataparser
                                dt = dataparser.parse(string_output_time)
                                
                                import pytz
                            
                                local_tz = pytz.timezone('Europe/Berlin')
                                target_tz = pytz.timezone('UTC')
                                
                                dt = local_tz.localize(dt) # set to Berlin time
                                dt = target_tz.normalize(dt) #transfer to UTC
                                
                                #self.datetime_end = dt
                                self.XRD_Data_Entries_Experiment[index].XRD_Datetime_End = dt
                            
                            ###
                            # Number of Data Entries
                            ###
                            datasplice = contentrawfile[4*0x10000+0x0622:4*0x10000+0x0624]
                            # 'i': Integer (4 bytes)
                            # 'f': Float (4 bytes)
                            # 'd': Double (8 bytes)
                            # 'h': Short (2 bytes)
                            count = len(datasplice)//2 # Number of bytes to unpack (1 for char)
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(datasplice, 'h', count)
                            countDataEntries=int(unpacked_data[0])
                            # print(countDataEntries)
                            
                            ###
                            # x-range
                            ###
                            datasplice = contentrawfile[4*0x10000+0x062C:4*0x10000+0x0638]
                            
                            #'i': Integer (4 bytes)
                            #'f': Float (4 bytes)
                            #'d': Double (8 bytes)
                            #'h': Short (2 bytes)
                            count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(datasplice, 'f', count)
                            #print(unpacked_data)
                            
                            x_start = unpacked_data[0]
                            x_end = unpacked_data[2]
    
                            x_range = np.linspace(x_start, x_end, countDataEntries, True)
                            #print(type(x_range))
                            #print(x_range)
                            #print(len(x_range))
                            
                            # self.Deg2Theta = ureg.Quantity(x_range, 'degree') # dataxydfile[:, 0]  # First column
                            self.XRD_Data_Entries_Experiment[index].XRD_Deg2Theta = self.Deg2Theta = ureg.Quantity(x_range, 'degree')
                            
                            ###
                            # Data
                            ###
    
                            datasplice = contentrawfile[0x40800:0x40800+4*countDataEntries]
                            #'i': Integer (4 bytes)
                            #'f': Float (4 bytes)
                            #'d': Double (8 bytes)
                            count = len(datasplice)//4 # Number of bytes to unpack (1 for char)
                            #print(count)
                            unpacked_data = self.unpack_repeated_bytes(datasplice, 'i', count)
    
                            #print(unpacked_data)
                            #type(unpacked_data)
                            y_data = np.array(unpacked_data, dtype=np.int64)
                            #print(y_data)
                            #print(len(y_data))
                            
                            #self.Intensity = ureg.Quantity(y_data, 'dimensionless') #dataxydfile[:, 1]  # Second column
                            self.XRD_Data_Entries_Experiment[index].XRD_Intensity = ureg.Quantity(y_data, 'dimensionless')
                            
                            # Sanity check
                            if len(x_range) != len(y_data):
                                raise DataFileError(f"The data in file '{data_file}' could not parsed. '{countDataEntries}' expected, but {len(y_data)} found!")
                            
                            # Create plot
                            #self.figures = self.generate_plots()
                
            # Check if any experimental (raw/xyd) or simulation (xye) file is provided
            if self.data_as_xye_file:
                
                num_xye_file = len(self.data_as_xye_file)
                
                # Create subsection if not existing
                if not self.XRD_Data_Entries_Simulation:
                    self.XRD_Data_Entries_Simulation = []
                    # Ensure the list is long enough
                    while len(self.XRD_Data_Entries_Simulation) < num_xye_file:
                        self.XRD_Data_Entries_Simulation.append(XRD_Data_Entry())  # Append a placeholder value
                    
                # Create new if not sufficient long enough - overwrites the default
                if len(self.XRD_Data_Entries_Simulation) < num_xye_file:
                    self.XRD_Data_Entries_Simulation = []
                    while len(self.XRD_Data_Entries_Simulation) < num_xye_file:
                        self.XRD_Data_Entries_Simulation.append(XRD_Data_Entry())  # Append a placeholder value
                
                # Loop over all filenames
                for index, data_file in enumerate(self.data_as_xye_file):
                    # Check if the file has the correct extension
                    if not data_file.endswith('.xye'):
                        raise DataFileError(f"The file '{data_file}' must have a .xye extension.")
                    
                    if getattr(self.XRD_Data_Entries_Simulation[index], "name", None) is None:
                        self.XRD_Data_Entries_Simulation[index].name = data_file

                    if data_file.endswith('.xye'):
                        # Otherwise parse the file
                        with archive.m_context.raw_file(data_file) as xyefile:
                            # The first line is the Cu K alpha wavelength
                            first_line = xyefile.readline().strip()

                            if isinstance(first_line, (bytes, bytearray)):
                                first_line = first_line.decode("utf-8", errors="replace").strip()
                            
                            parts = first_line.split(',')
                            delimiter = ',' if len(parts) >= 2 else None
                            
                            first_val = parts[0]
                            
                            #self.Simulation_Wavelength = ureg.Quantity(float(first_line), 'angstrom')
                            self.XRD_Data_Entries_Simulation[index].XRD_Wavelength = ureg.Quantity(float(first_val), 'angstrom')
                            
                            # Load the data from the file, skipping the first line
                            dataxyefile = np.loadtxt(xyefile, skiprows=1, delimiter=delimiter)
                                
                            # Split the data into three distinct arrays
                            Sim_TwoTheta = dataxyefile[:, 0]  # 2Theta
                            Sim_Intensity = dataxyefile[:, 1]  # Simulated Intensity
                            
                            #self.Simulated_Deg2Theta = ureg.Quantity(Sim_TwoTheta, 'degree')
                            #self.Simulated_Intensity = ureg.Quantity(Sim_Intensity, 'dimensionless')

                            # Separate the columns into two variables and copy to 
                            self.XRD_Data_Entries_Simulation[index].XRD_Deg2Theta = ureg.Quantity(Sim_TwoTheta, 'degree') # dataxydfile[:, 0]  # First column
                            self.XRD_Data_Entries_Simulation[index].XRD_Intensity = ureg.Quantity(Sim_Intensity, 'dimensionless') #dataxydfile[:, 1]  # Second column
                            
             # Check if any experimental (raw/xyd) or simulation (xye) file is provided
            if self.data_as_raw_or_xyd_file or self.data_as_xye_file:
                # Create plot
                self.figures = self.generate_plots()
            
        except Exception as e:
            logger.error('Invalid file parsing error.', exc_info=e)
            #logger.error('Invalid file extension for parsing.', exc_info=e)
        # In case something is odd here -> just return
        # if not self.results:
        #    return
        
        super().normalize(archive, logger)
        
 
