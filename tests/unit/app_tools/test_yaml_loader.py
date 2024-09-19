import pytest
import yaml
from src.app_tools.yaml_loader import load_yaml_file, load_multiple_yaml_files_combined


@pytest.fixture
def sample_yaml_files(tmpdir):
    # Create sample YAML files for testing
    file1 = tmpdir.join("file1.yaml")
    file2 = tmpdir.join("file2.yaml")

    data1 = {"key1": "value1", "key2": "value2"}
    data2 = {"key3": "value3", "key4": "value4"}

    with open(file1, "w") as f1:
        yaml.dump(data1, f1)

    with open(file2, "w") as f2:
        yaml.dump(data2, f2)

    return str(file1), str(file2), data1, data2


def test_load_yaml_file(sample_yaml_files):
    file1, _, expected_data, _ = sample_yaml_files
    result = load_yaml_file(file1)
    assert result == expected_data


def test_load_multiple_yaml_files_combined(sample_yaml_files):
    file1, file2, data1, data2 = sample_yaml_files
    expected_combined_data = {**data1, **data2}
    result = load_multiple_yaml_files_combined([file1, file2])
    assert result == expected_combined_data
