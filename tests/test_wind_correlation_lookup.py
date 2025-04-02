import pytest
import pandas as pd
import numpy as np
from src.logic.wind_correlation_lookup import WindCorrelationLookup


@pytest.fixture
def lookup():
    return WindCorrelationLookup(data_folder='../data/raw/')

def test_mean_correlation_exact_vs_approx(lookup):
    """Test that 'exact' and 'approx' modes return the same result for manually defined locations,
    ensuring that the 'approx' mode uses a maximum random offset of 0.125° from the ERA5 grid location
    (to ensure it remains the closest point)"""

    TEST_LOCATIONS = [
        (-31.5, 125.5), (-13.25, 142.25), (-17.25, 126.25), (-30.5, 129.75), (-28.75, 132.5),
        (-26.0, 135.0), (-24.75, 130.0), (-29.5, 128.0), (-27.0, 124.0), (-42.25, 147.0),
        (-31.0, 136.5), (-25.5, 131.75), (-33.0, 134.0), (-30.0, 152.5), (-30.25, 125.75),
        (-43.5, 146.25), (-34.75, 117.0), (-32.0, 123.5), (-27.75, 136.0), (-25.0, 127.25)
    ]

    print(f"\nRunning tests for {len(TEST_LOCATIONS)} manually selected locations...\n")

    for lat, lon in TEST_LOCATIONS:

        delta_lat = np.random.uniform(-0.125, 0.125)
        delta_lon = np.random.uniform(-0.125, 0.125)

        approx_lat = lat + delta_lat
        approx_lon = lon + delta_lon

        try:
            exact_correlation = lookup.get_mean_correlation(lat, lon, mode="exact")
            approx_correlation = lookup.get_mean_correlation(approx_lat, approx_lon, mode="approx")

            lat_rounded = round(lat, 3)
            lon_rounded = round(lon, 3)
            approx_lat_rounded = round(approx_lat, 3)
            approx_lon_rounded = round(approx_lon, 3)
            exact_corr_rounded = round(exact_correlation, 3)
            approx_corr_rounded = round(approx_correlation, 3)

            print(f"({lat_rounded}, {lon_rounded}) -> Exact: {exact_corr_rounded}, Approx ({approx_lat_rounded}, {approx_lon_rounded}): {approx_corr_rounded}")

            assert exact_corr_rounded == approx_corr_rounded, (
                f"Mismatch at ({lat_rounded}, {lon_rounded}) vs approx ({approx_lat_rounded}, {approx_lon_rounded}): "
                f"{exact_corr_rounded} != {approx_corr_rounded}"
            )
        except ValueError as e:
            pytest.fail(f"Unexpected missing data at ({lat_rounded}, {lon_rounded}): {e}")

def test_plot_correlation_map(lookup):
    """Plot the correlation map"""
    land_indices = np.argwhere(~np.isnan(lookup.mean_correlation_map))
    latitudes = lookup.latitude[land_indices[:, 0]]
    longitudes = lookup.longitude[land_indices[:, 1]]
    values = lookup.mean_correlation_map[land_indices[:, 0], land_indices[:, 1]]

    df = pd.DataFrame({
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Correlation": values
    })

    try:
        lookup.plot_scatter_map(df, value_column="Correlation")
        print("\nCorrelation Map plotted successfully, open browser to see it!")
    except Exception as e:
        pytest.fail(f"Plotting failed: {e}")


if __name__ == "__main__":
    pytest.main()