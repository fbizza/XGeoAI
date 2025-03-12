import json
import os
import pandas as pd

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file at '{path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at '{path}' contains invalid JSON.")
        return None
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file at '{path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def line_coords(path):
    # to handle geojson lines in a dash friendly way
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df['lat'].values, df['lon'].values, df['name'].values
    else:
        raise FileNotFoundError(f"{path} not found")