from data.data_loader import DataLoader
from models.wind_correlation_analysis import WindAnalyzer
from visualization.plotter import Plotter

data_path = "data/raw"

loader = DataLoader(data_path)

#correlation_to_plot = "data/basetables/all_locations_mean_correlation.csv"
correlation_to_plot = "data/basetables/target_mean_correlation.csv"

df = loader.load_csv(correlation_to_plot)

Plotter.create_wind_correlation_figure(df)

#Plotter.plot_user_locations(target_coords)

