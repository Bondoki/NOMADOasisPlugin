import os.path

from nomad.client import normalize_all, parse
#from crc1415plugin.schema_packages.ELNSampleOverviewSchema import CRC1415SampleOverview

def test_schema_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_sample.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Sample")

    #assert entry_archive.data.data_file == 'test.xyd' 
    assert entry_archive.data.data_as_tif_or_tiff_file == ['testSEM.tif', 'testSEM3.tiff'] #'testSEM.tif' 
    #assert entry_archive.data.data_file == 'test.csv' 
    #assert entry_archive.data.data_file == 'testSEM.jpg' 
    
def test_MeasurementIR_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementIR.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run IRMeasurement")

    assert entry_archive.data.data_as_dpt_file == 'test_file_IR.dpt' 
    
    assert len(entry_archive.data.Transmittance) == 3525 

def test_MeasurementSEM_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementSEM.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Measurement SEM")

    assert entry_archive.data.data_as_tif_or_tiff_file == ['test_file_SEM_01.tif', 'test_file_SEM_03.tiff'] #'testSEM.tif' 

def test_MeasurementSEM_Auxiliary_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementSEM_Auxiliary.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Measurement SEM Auxiliary")

    assert entry_archive.data.data_as_tif_or_tiff_file == ['test_file_SEM_02.tiff', 'test_file_SEM_03.tif'] #'testSEM.tif' 

def test_MeasurementTEM_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementTEM.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Measurement TEM")

    assert entry_archive.data.data_as_tif_or_tiff_file == ['test_file_TEM_01.tif', 'test_file_TEM_02.tiff'] 
    

def test_MeasurementXRD_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementXRD_XYD.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run XRDMeasurement XYD file")

    #assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    #assert len(entry_archive.data.Transmittance) == 3525 
    
def test_MeasurementXRD_RAW_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementXRD_RAW.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run XRDMeasurement RAW file")

    #assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    #assert len(entry_archive.data.Transmittance) == 3525 

def test_MeasurementXRD_XYE_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementXRD_XYE.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run MeasurementXRD XYE file")



def test_MeasurementRaman__package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementRaman.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run RamanMeasurement")
    
    # #print(entry_archive.data.Raman_data_entries)
    # rd = RamanData()
    # rd.name = "John Doe"
    # rd.data_as_tvf_or_txt_file = 'test.txt'
    # #print(rd)
    # entry_archive.data.Raman_data_entries.append(rd)
    
    normalize_all(entry_archive)
    
    print("Length Raman-Entries:", len(entry_archive.data.Raman_data_entries))
    #print(entry_archive.data.Raman_data_entries.RamanData.name)
    #assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    #assert len(entry_archive.data.Transmittance) == 3525 
    
def test_MeasurementRaman_1TVF_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementRaman_1TVF.archive.yaml')
    entry_archive = parse(test_file)[0]
    
    print("Run RamanMeasurement 1TVF")
    
    normalize_all(entry_archive)
    
    print("Length Raman-Entries:", len(entry_archive.data.Raman_data_entries))

def test_MeasurementRaman_TVB_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementRaman_TVB.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run RamanMeasurement TVB")
    
    normalize_all(entry_archive)
    
    assert entry_archive.data.data_as_tvb_file == 'test_file_Raman_TVB_10Frames.tvb'
    
def test_MeasurementRaman_TVB2_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementRaman_TVB_02.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run RamanMeasurement TVB02")
    
    normalize_all(entry_archive)
    
    assert entry_archive.data.data_as_tvb_file == 'test_file_Raman_TVB_1Frame.tvb'
    
    
def test_MeasurementRaman_ZIP_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementRaman_ZIP.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run RamanMeasurement ZIP")
    
    normalize_all(entry_archive)



def test_MeasurementAdsorption_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementAdsorption.archive.yaml')
    entry_archive = parse(test_file)[0]
    print("Run Adsorption")
    
    normalize_all(entry_archive)
    
    #assert entry_archive.data.data_as_txt_file == 'test_QuantachromeAdsorption.txt'

def test_MeasurementTGA_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementTGA.archive.yaml')
    entry_archive = parse(test_file)[0]
    print("Run TGA")
    
    normalize_all(entry_archive)

def test_MeasurementCV_TXT_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementCV_TXT.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run Measurement CV TXT - 1File")
    
    normalize_all(entry_archive)
    
    #print("Length CV-Entries:", len(entry_archive.data.CV_data_entries))

def test_MeasurementCV_TXT2_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementCV_TXT2.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run Measurement CV TXT - 2Files")
    
    normalize_all(entry_archive)
    
    #print("Length CV-Entries:", len(entry_archive.data.CV_data_entries))

def test_MeasurementCV_IDS_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementCV_IDS.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run Measurement CV IDS")
    
    normalize_all(entry_archive)

def test_MeasurementGeneric_ZIP_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementGeneric_ZIP.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run Measurement Generic zip")
    
    normalize_all(entry_archive)
    
def test_MeasurementGeneric_TXT_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_MeasurementGeneric_TXT.archive.yaml')
    entry_archive = parse(test_file)[0]
    #normalize_all(entry_archive)
    print("Run Measurement Generic txt")
    
    normalize_all(entry_archive)
    

    
    
def test_Overview_package():
    test_file = os.path.join('tests', 'datacrc1415plugin', 'test_overview.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Overview")

    #assert entry_archive.data.data_file == 'test.xyd' 
    #assert entry_archive.data.data_as_tif_or_tiff_file == ['testSEM.tif', 'testSEM3.tiff'] #'testSEM.tif' 
    #assert entry_archive.data.data_file == 'test.csv' 
    #assert entry_archive.data.data_file == 'testSEM.jpg' 
