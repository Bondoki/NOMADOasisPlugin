import re
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



class MeasurementAdsorption(ELNMeasurement, PlotSection, ArchiveSection):
    '''
    Class for handling measurement of Adsorption.
    '''
    m_def = Section(
        categories=[CRC1415CategoryMeasurement],
        label='CRC1415-Measurement-Adsorption',
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
                    "data_as_txt_file",
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
        description='Name of the section of Adsorption measurement',
        a_eln={'component': 'StringEditQuantity', 'label': 'Adsorption: Brief title of the measurement'},
    )
    
    data_as_txt_file = Quantity(
        type=str,
        description="A reference to an uploaded Quantachrome .txt produced by the adsorption instrument.",
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
    )
    
    datetime_end = Quantity(
        type=Datetime,
        description='The date and time when this activity has ended.',
        a_eln=dict(component='DateTimeEditQuantity', label='Ending Time'),
    )
    
    Analysis_Time= Quantity(
        type=np.float64,
        unit='minute',
        description='The time for performing the analysis.',
        a_eln=dict(component='NumberEditQuantity', label='Analysis Time', defaultDisplayUnit= 'minute'),
    )
    
    Sample_Weight = Quantity(
        type=np.float64,
        unit='milligram',
        description='The weight of the sample, milligram',
        a_eln=dict(component='NumberEditQuantity', label='Sample Weight', defaultDisplayUnit= 'milligram'),
    )
    
    Outgas_Time= Quantity(
        type=np.float64,
        unit='hour',
        description='The time during the outgas process.',
        a_eln=dict(component='NumberEditQuantity', label='Outgas Time', defaultDisplayUnit= 'hour'),
    )
    
    Outgas_Temperature = Quantity(
        type=np.float64,
        unit='celsius',
        description='The temperature during the outgas process.',
        a_eln=dict(component='NumberEditQuantity', label='Outgas Temperature', defaultDisplayUnit= 'celsius'),
    )
    
    Analysis_Gas  = Quantity(
        type=str,
        #unit='celsius',
        description='The gas used for the analysis.',
        a_eln=dict(component='StringEditQuantity', label='Analysis Gas'),
    )
    
    Bath_Temperature = Quantity(
        type=np.float64,
        unit='kelvin',
        description='The temperature of the bath.',
        a_eln=dict(component='NumberEditQuantity', label='Bath Temperature', defaultDisplayUnit= 'kelvin'),
    )
    
    RelativePressure = Quantity(
        type=np.float64,
        shape=["*"],
        unit='dimensionless',
        description='The relative pressure range of the spectrogram, dimensionless.',
    )
    AdsorpedVolume = Quantity(
        type=np.float64,
        shape=["*"],
        unit='millimole/gram',
        description='The measured adsorped volume at relative pressure value, normalized by ideal gas molar volume 22.4 cm**3/mol.',
    )
    
    # def generate_plots(self) -> list[PlotlyFigure]:
    #     """
    #     Generate the plotly figures for the `MeasurementAdsorption` section.
    # 
    #     Returns:
    #         list[PlotlyFigure]: The plotly figures.
    #     """
    #     # figures = []
    #     # #if self.wavelength is None:
    #     # #    return figures
    #     # 
    #     # x_label = 'Wavenumber'
    #     # xaxis_title = f'{x_label} (cm-1)'
    #     # x = self.Wavenumber.to('1/cm').magnitude
    #     # 
    #     # y_label = 'Transmittance'
    #     # yaxis_title = f'{y_label} (a.u.)'
    #     # y = self.Transmittance.to('dimensionless').magnitude
    #     # 
    #     # line_linear = px.line(x=x, y=y)
    #     # 
    #     # line_linear.update_layout(
    #     #     title=f'{y_label} over {x_label}',
    #     #     xaxis_title=xaxis_title,
    #     #     yaxis_title=yaxis_title,
    #     #     xaxis=dict(
    #     #         fixedrange=False,
    #     #     ),
    #     #     yaxis=dict(
    #     #         fixedrange=False,
    #     #     ),
    #     #     template='plotly_white',
    #     # )
    #     # 
    #     # figures.append(
    #     #     PlotlyFigure(
    #     #         label=f'{y_label} linear plot',
    #     #         index=0,
    #     #         figure=line_linear.to_plotly_json(),
    #     #     ),
    #     # )
    # 
    #     return figures
    
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
            if self.data_as_txt_file:
                # Check if the file has the correct extension
                if not self.data_as_txt_file.endswith('.txt'):
                    raise DataFileError(f"The file '{self.data_as_txt_file}' must have a Quantachrome .txt extension.")
            
                # Get the encoding
                # from chardet import detect # for Quantachrome ASiQwin text as the file has the 'Windows-1252' encoding
                # # but this can usally ignored as the only character is the Angstrom 
                
                # with archive.m_context.raw_file(self.data_as_txt_file, 'rb') as txtfile:
                #     rawdata = txtfile.read()
                #     get_encoding_type = detect(rawdata)['encoding']
                #     print(get_encoding_type)
                
                with archive.m_context.raw_file(self.data_as_txt_file, 'r', errors='ignore') as txtfile:
                    text = txtfile.read()

                # Merge all whitespaces to one
                cleaned_text = re.sub(r'\s+', ' ', text)

                # Split the text to find the section starting with "Analysis Report"
                report_start = cleaned_text.find("Analysis Report")
                if report_start == -1:
                    raise DataFileError(f"The file '{self.data_as_txt_file}' could not be parsed. Error in parsing Analysis Report section.")
                
                # Check for version
                header_text = cleaned_text[:report_start]

                match = re.search(r'version\s+([\d.]+)', header_text, re.IGNORECASE)

                # Check if the match was successful and extract the version
                if match:
                    if match.group(1) != '3.01' and match.group(1) != '3.0':
                        raise DataFileError(f"The file '{self.data_as_txt_file}' could not be parsed. Parser only for v3.0 instead {match.group(1) } found.")
                else:
                    raise DataFileError(f"The file '{self.data_as_txt_file}' could not be parsed. No version information found.")
                
                
                # Extract the relevant part of the text
                report_text = cleaned_text[report_start:]
                
                # Define a dictionary to hold the extracted fields
                report_data = {}
                
                # Use regular expressions to extract the fields
                #report_data['Operator'] = re.search(r'Operator:\s*(.*?)\s*Date:', report_text).group(1).strip()
                #report_data['Date'] = re.search(r'Date:\s*(.*?)\s*Sample ID:', report_text).group(1).strip()
                #report_data['Sample ID'] = re.search(r'Sample ID:\s*(.*?)\s*Filename:', report_text).group(1).strip()
                #report_data['Filename'] = re.search(r'Filename:\s*(.*?)\s*Sample Desc:', report_text).group(1).strip()
                #report_data['Sample Desc'] = re.search(r'Sample Desc:\s*(.*?)\s*Sample weight:', report_text).group(1).strip()
                #report_data['Sample weight'] = re.search(r'Sample weight:\s*(.*?)\s*Analysis Time:', report_text).group(1).strip()
                report_data['Sample weight'] = re.search(r'Sample weight:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(1).strip()
                report_data['Sample weight unit'] = re.search(r'Sample weight:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(2).strip()
    
                
                #report_data['Analysis Time'] = re.search(r'Analysis Time:\s*(.*?)\s*End of run:', report_text).group(1).strip()
                
                # Regex pattern to match both formats either
                # MMM.M min or HH:MM hr:min
                pattern_analysis_time = r'Analysis Time:\s*([\d.]+)\s*min|Analysis Time:\s*(\d+):(\d+)\s*hr:min'

                match_analysis_time = re.search(pattern_analysis_time, report_text, re.IGNORECASE)

                if match_analysis_time:
                    if match_analysis_time.group(1):  # format matched MMM.M min
                        report_data['Analysis Time'] = float(match_analysis_time.group(1))
                        report_data['Analysis Time unit'] = 'minutes'
                    elif match_analysis_time.group(2) and match_analysis_time.group(3):  # format matched HH:MM hr:min
                        report_data['Analysis Time'] = float(match_analysis_time.group(2))*60.0 + float(match_analysis_time.group(3)) # convert in minutes
                        report_data['Analysis Time unit'] = 'minutes'
                        #print(f"{match_analysis_time.group(2)} hr {match_analysis_time.group(3)} min")
                
                #report_data['End of run'] = re.search(r'End of run:\s*(.*?)\s*Instrument:', report_text).group(1).strip()
                
                # Regex pattern to match the date and time MM/DD/YYYY HH:MM:SS
                pattern_end_run = r'End of run:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2})'
                
                # Use regex to find the date and time
                match_end_run = re.search(pattern_end_run, report_text)
                
                # Check if the match was successful and extract the date and time
                if match_end_run:
                    #print("Parsed:", match_end_run.group(0))
                    report_data['End of run'] = match_end_run.group(1)
                
                #report_data['Instrument'] = re.search(r'Instrument:\s*(.*?)\s*Void Vol.:', report_text).group(1).strip()
                #report_data['Void Vol.'] = re.search(r'Void Vol.:\s*(.*?)\s*He Mode.Cell:', report_text).group(1).strip()
                #report_data['He Mode.Cell'] = re.search(r'He Mode.Cell:\s*(.*?)\s*Run mode', report_text).group(1).strip()
                #report_data['Run mode'] = re.search(r'Run mode(.*?)(Instrument version:)', report_text).group(1).strip()
                #report_data['Instrument version'] = re.search(r'Instrument version:\s*(.*?)\s*Thermal delay:', report_text).group(1).strip()
                #report_data['Thermal delay'] = re.search(r'Thermal delay:\s*(.*?)\s*He evac time:', report_text).group(1).strip()
                #report_data['He evac time'] = re.search(r'He evac time:\s*(.*?)\s*Outgas Time:', report_text).group(1).strip()
                #print('outgas0')
                #report_data['Outgas Time'] = re.search(r'Outgas Time:\s*(.*?)\s*OutgasTemp:', report_text).group(1).strip()
                report_data['Outgas Time'] = re.search(r'Outgas Time:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(1)
                report_data['Outgas Time unit'] = re.search(r'Outgas Time:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(2)
                
                #report_data['OutgasTemp'] = re.search(r'OutgasTemp:\s*(.*?)\s*Analysis gas:', report_text).group(1).strip()
                report_data['OutgasTemp'] = re.search(r'Outgas\s*Temp\.?:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(1)
                report_data['OutgasTemp unit'] = re.search(r'Outgas\s*Temp\.?:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(2)
                
                #report_data['Analysis gas'] = re.search(r'Analysis gas:\s*(.*?)\s*Bath Temp:', report_text).group(1).strip()
                report_data['Analysis gas'] = re.search(r'Analysis gas:\s*(.*?)\s*(\w+)', report_text, re.IGNORECASE).group(0).split()[2]
                
                #report_data['Bath Temp'] = re.search(r'Bath Temp:\s*(.*?)\s*Press. Tolerance:', report_text).group(1).strip()
                
                report_data['Bath Temp'] = re.search(r'Bath\s*Temp\.?:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(1)
                report_data['Bath Temp unit'] = re.search(r'Bath\s*Temp\.?:\s*([\d.]+)\s*(\w+)', report_text, re.IGNORECASE).group(2)
                #report_data['Press. Tolerance'] = re.search(r'Press. Tolerance:\s*(.*?)\s*Equil time:', report_text).group(1).strip()
                #report_data['Equil time'] = re.search(r'Equil time:\s*(.*?)\s*Equil timeout:', report_text).group(1).strip()
                #report_data['Equil timeout'] = re.search(r'Equil timeout:\s*(.*?)\s*Data Reduction Parameters', report_text).group(1).strip()
                
                # Extract the metadata
                self.Sample_Weight = ureg.Quantity(float(report_data['Sample weight']), report_data['Sample weight unit'])
                
                # Convert the unpacked data as a datetime object
                from datetime import timedelta

                from dateutil import parser as dataparser
                
                self.Analysis_Time = ureg.Quantity(float(report_data['Analysis Time']), report_data['Analysis Time unit'])
                #print(type(analysistime.to(ureg.minute).magnitude))
                #print(float(analysistime.to(ureg.minute).magnitude))
                
                if 'End of run' in report_data.keys():
                    import pytz
                    # End of run:    MM/DD/YYYY 5:11:04 in Berlin/Europe time zone
                    exp_time = dataparser.parse(report_data['End of run'], dayfirst=False)
                    
                    local_tz = pytz.timezone('Europe/Berlin')
                    target_tz = pytz.timezone('UTC')
                    
                    exp_time = local_tz.localize(exp_time) # set to Berlin time
                    exp_time = target_tz.normalize(exp_time) #transfer to UTC
                    
                    self.datetime_end = exp_time
                    
                    self.datetime = exp_time - timedelta(minutes=float(self.Analysis_Time.to(ureg.minute).magnitude))
                
                self.Outgas_Time = ureg.Quantity(float(report_data['Outgas Time']), 'hour' if report_data['Outgas Time unit'] == 'hrs' else 'dimensionless')
                
                self.Outgas_Temperature = ureg.Quantity(float(report_data['OutgasTemp']), 'celsius' if report_data['OutgasTemp unit'] == 'C' else 'dimensionless')
                
                self.Analysis_Gas = report_data['Analysis gas']
                
                self.Bath_Temperature = ureg.Quantity(float(report_data['Bath Temp']), 'kelvin' if report_data['Bath Temp unit'] == 'K' else 'dimensionless')
                
                
                # Splits the file into parts separated by empty lines.
                # The actual data is in the last part.
                parts = text.split('\n\n')
                
                # The first part is everything before the first empty line
                #before_section = parts[0].strip()
                #print(before_section)
                # The data part is everything after the last empty line
                # We need to check if there is a data part
                data_section = parts[len(parts)-1].strip() if len(parts) > 1 else None 
                
                if not data_section:
                    raise DataFileError(f"The file '{self.data_as_txt_file}' could not be parsed. Error in parsing data section.")
                # Convert table data to numpy array
                relativPressure_array = []
                adsorpedVolume_array = []

                # Split the section into lines
                lines = data_section.splitlines()
                
                # Iterate through each line and extract values
                for line in lines:
                    # Use regex to capture the relative pressure and volume values
                    match = re.match(r'\s*(\S+)\s+(\S+)', line)
                    
                    if match:
                        try:
                            relativPressure_array.append(float(match.group(1)))
                            adsorpedVolume_array.append(float(match.group(2)))
                        except ValueError:
                            pass
                
                relativePressure = np.array(relativPressure_array)
                adsorpedVolume = np.array(adsorpedVolume_array)
                
                # Archive the data
                self.RelativePressure = ureg.Quantity(relativePressure, 'dimensionless')
                self.AdsorpedVolume = ureg.Quantity(adsorpedVolume/22.4, 'millimole/g') # normalized by ideal gas molar volume
                
                # Find the index of the maximum value
                max_index_relativePressure = np.argmax(relativePressure)

                # Split the array into two parts for plotting
                adsorption_relativePressure = relativePressure[:max_index_relativePressure + 1]  # Include the maximum value
                desorption_relativePressure = relativePressure[max_index_relativePressure:]   # Exclude the maximum value
                
                adsorption_adsorpedVolume = adsorpedVolume[:max_index_relativePressure + 1]/22.4  # Include the maximum value
                desorption_adsorpedVolume = adsorpedVolume[max_index_relativePressure:]/22.4   # Exclude the maximum value
                
                # create plot
                figures = []
                
                # Create a figure
                config = {'displayModeBar': True}
                fig = go.Figure()
                
                x_label = 'Relative Pressure'
                xaxis_title = 'p/p0 [dimensionless]'
                x_ads = adsorption_relativePressure
                x_des = desorption_relativePressure
                
                #y_label = '\u25CF Adsorbed Volume and \u25A1 Desorbed Volume'
                y_label = 'Adsorbed Volume'
                yaxis_title = f"Adsorbed Volume [mmol/g] ({self.Analysis_Gas}, {self.Bath_Temperature.to('kelvin').magnitude} {self.Bath_Temperature.units:~})"
                y_ads = adsorption_adsorpedVolume
                y_des = desorption_adsorpedVolume
                
                #line_ads = px.line(x=x_ads, y=y_ads, markers=True, marker_symbol='circle')
                #line_des = px.line(x=x_des, y=y_des, markers=True, marker_symbol='square-open')
                
                # Add the first line with markers
                fig.add_trace(go.Scatter(
                    x=x_ads,
                    y=y_ads,
                    mode='lines+markers',  # 'lines+markers' to show both lines and markers
                    name='adsorption',         # Name of the first line
                    line=dict(color='blue'),  # Line color
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
                    marker=dict(size=10, symbol='circle')      # Marker size
                ))

                # Add the second line with markers
                fig.add_trace(go.Scatter(
                    x=x_des,
                    y=y_des,
                    mode='lines+markers',  # 'lines+markers' to show both lines and markers
                    name='desorption',         # Name of the second line
                    line=dict(color='red'),   # Line color
                    hovertemplate='(x: %{x}, y: %{y})<extra></extra>',  # Custom hovertemplate
                    marker=dict(size=10, symbol='square-open')      # Marker size
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
