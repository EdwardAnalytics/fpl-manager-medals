import pandas as pd


def load_csv_with_error_handling(file_path, default_value="Season Not Started"):
    """
    Load a CSV file with error handling if the file does not exist.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.
    default_value : any
        Value to return if the file cannot be loaded.

    Returns
    -------
    pd.DataFrame or str
        DataFrame containing the CSV data or a default value if the file is not found.
    """
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        data = default_value
    return data
