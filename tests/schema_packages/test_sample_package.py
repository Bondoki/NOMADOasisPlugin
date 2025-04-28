import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test_sample.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Sample")

    #assert entry_archive.data.data_file == 'test.xyd' 
    assert entry_archive.data.data_as_tif_or_tiff_file == ['testSEM.tif', 'testSEM3.tiff'] #'testSEM.tif' 
    #assert entry_archive.data.data_file == 'test.csv' 
    #assert entry_archive.data.data_file == 'testSEM.jpg' 
    
def test_IRMeasurement_package():
    test_file = os.path.join('tests', 'data', 'test_IRMeasurement.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run IRMeasurement")

    assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    assert len(entry_archive.data.Transmittance) == 3525 
    
    
def test_Overview_package():
    test_file = os.path.join('tests', 'data', 'test_overview.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Overview")

    #assert entry_archive.data.data_file == 'test.xyd' 
    #assert entry_archive.data.data_as_tif_or_tiff_file == ['testSEM.tif', 'testSEM3.tiff'] #'testSEM.tif' 
    #assert entry_archive.data.data_file == 'test.csv' 
    #assert entry_archive.data.data_file == 'testSEM.jpg' 

from crc1415testsample.schema_packages.ELNSample2_schema import RamanData

def test_RamanMeasurement_package():
    test_file = os.path.join('tests', 'data', 'test_RamanMeasurement.archive.yaml')
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

def test_XRDMeasurement_package():
    test_file = os.path.join('tests', 'data', 'test_XRDMeasurementXYD.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run XRDMeasurement XYD file")

    #assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    #assert len(entry_archive.data.Transmittance) == 3525 
    
def test_XRDMeasurementRAW_package():
    test_file = os.path.join('tests', 'data', 'test_XRDMeasurementRAW.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run XRDMeasurement RAW file")

    #assert entry_archive.data.data_as_dpt_file == 'IRtest.dpt' 
    
    #assert len(entry_archive.data.Transmittance) == 3525 
    
