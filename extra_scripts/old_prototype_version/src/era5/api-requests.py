import json
import cdsapi
import webbrowser

def get_era5_api_key():
    try:
        with open("../../../../api-keys", "r") as file:
            api_keys = json.load(file)

        era5_api_key = api_keys.get("ERA5_API_KEY")

        if era5_api_key:
            print(f"ERA5 API key: {era5_api_key}")
            return era5_api_key
        else:
            raise KeyError("No ERA5 key was found in the keys text file")

    except FileNotFoundError:
        print("Error: keys text file not found")
    except json.JSONDecodeError:
        print("Error: keys text file is not a valid JSON dictionary")
    except KeyError as e:
        print(e)

def era5_api_request():
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "year": ["2025"],
        "month": ["01"],
        "day": [
            "01"
        ],
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "variable": [
            "100m_u_component_of_wind",
            "100m_v_component_of_wind"
        ],
        "area": [-10, 112, -44, 155]
    }

    client = cdsapi.Client(url="https://cds.climate.copernicus.eu/api", key=get_era5_api_key())
    client.retrieve(dataset, request).download()

