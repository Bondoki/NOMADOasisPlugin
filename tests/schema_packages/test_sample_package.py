import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test_sample.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Sample")

    assert entry_archive.data.data_file == 'test.xyd' 
    #assert entry_archive.data.data_file == 'test.csv' 
    
def test_IRMeasurement_package():
    test_file = os.path.join('tests', 'data', 'test_IRMeasurement.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run IRMeasurement")

    assert entry_archive.data.data_file == 'IRtest.dpt' 
    
    assert len(entry_archive.data.Transmittance) == 3525 
    
    
