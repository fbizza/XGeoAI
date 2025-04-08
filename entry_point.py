from data.data_loader import DataLoader
from models.wind_correlation_analysis import WindAnalyzer
from visualization.plotting_functions import *

data_path = "data/raw"

loader = DataLoader(data_path)

#data_to_plot = "data/basetables/all_locations_mean_correlation.csv"
data_to_plot = "data/basetables/target_mean_correlation.csv"
#data_to_plot = "data/basetables/mean_wind_correlation_distance.csv"

df = loader.load_csv(data_to_plot)

windfarms_df = loader.load_csv("data/processed/wind-farms-with-ERA5_coordinates.csv")

#fig = create_wind_correlation_figure(df)
fig1 = create_scattermap_figure(df, marker_size=7, colorscale='RdBu', uniform_color=False)
fig2 = create_scattermap_figure(windfarms_df, marker_size=5, value_column_name="Asset", uniform_color="teal")

fig = add_map_layer(fig1, fig2)
fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=2,
                style='dark'
            ),
            title="Wind correlation with operating farms locations",
            margin=dict(l=0, r=0, t=40, b=0),  # Adjust margins
            legend=dict(x=0.01, y=0.99),  # Position the legend
            #gjoi=1,
        )
show_figure(fig)
#Plotter.plot_user_locations(target_coords)

