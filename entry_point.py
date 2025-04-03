from data.data_loader import DataLoader
from models.wind_correlation_analysis import WindAnalyzer
from visualization.plotter import Plotter

# Set paths
data_path = "data/raw"
csv_path = "data/processed/wind-farms-with-ERA5_coordinates.csv"
lat_col = "Closest ERA5 Land Latitude"
lon_col = "Closest ERA5 Land Longitude"

# Load data
loader = DataLoader(data_path)
lsmdf, lsmc, correlation_matrix = loader.load_wind_data()
csv_data = loader.load_csv(csv_path)
target_coords = list(zip(csv_data[lat_col], csv_data[lon_col]))
#target_coords = [(-37.65, 147), (-33.75, 116.75), (-15, 132)]

# Run analysis
analyzer = WindAnalyzer(lsmdf, lsmc, correlation_matrix)
correlation_values = analyzer.get_correlation_values(target_coords)

# Visualize results
if correlation_values is not None:
    Plotter.create_wind_correlation_figure(analyzer.latitude, analyzer.longitude, analyzer.land_coords, correlation_values)

Plotter.plot_user_locations(target_coords)

