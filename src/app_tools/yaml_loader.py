import yaml


def load_yaml_file(file_path):
    """
    Loads a YAML file and returns its content as a Python dictionary.

    Parameters
    ----------
    file_path : str
        The path to the YAML file.

    Returns
    -------
    dict
        The content of the YAML file as a Python dictionary.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def load_multiple_yaml_files_combined(file_paths):
    """
    Load multiple YAML files containing medal details into a dictionary.

    Parameters
    ----------
    file_paths : list of str
        List of file paths to YAML files.

    Returns
    -------
    dict
        Dictionary combining all loaded YAML data.
    """
    combined_data = {}
    for file_path in file_paths:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            combined_data.update(data)
    return combined_data
