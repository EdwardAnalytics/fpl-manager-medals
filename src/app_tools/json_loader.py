import json


def load_json_file(file_path):
    """
    Load data from a JSON file.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Returns
    -------
    dict
        Data loaded from the JSON file.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data
