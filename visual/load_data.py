import pandas as pd


def load_data(file_path: str) -> pd.DataFrame | None:
    """
    Load data from a csv file.
    :param file_path: (str) path to the csv file
    :return: (pd.DataFrame | None) DataFrame with the data or None if the file could not be loaded
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"File {file_path} not found.")
        raise e
    except pd.errors.ParserError as e:
        print(f"Error parsing the file {file_path}. Please check the file format.")
        raise e
    except PermissionError as e:
        print(f"Permission denied for file {file_path}.")
        raise e
