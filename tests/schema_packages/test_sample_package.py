import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test_sample.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    print("Run Sample")

    assert entry_archive.data.molecular_formula == 'VK0.5' 
    
    entry_archive.data.molecular_formula = 'AlK7' 
    normalize_all(entry_archive)
    print("Run Sample2")

    assert entry_archive.data.molecular_formula == 'AlK7' 
