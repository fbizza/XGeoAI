import pandas as pd
import plotly.graph_objects as go

class Plotter:
    @staticmethod
    def create_wind_correlation_figure(latitude, longitude, land_coords, correlation_values):
        """Plot wind correlation on a map."""
        df = pd.DataFrame({
            'Latitude': latitude[land_coords[0]],
            'Longitude': longitude[land_coords[1]],
            'Mean Correlation': correlation_values
        })

        data_filepath = "data/processed/wind-farms-with-ERA5_coordinates.csv"


        try:
            # Load the operating wind farms data
            wind_farms_df = pd.read_csv(data_filepath)
        except FileNotFoundError:
            print(f"Error: File not found at {data_filepath}")
            return

        fig = go.Figure(go.Scattermap(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=dict(
                size=7,
                color=df['Mean Correlation'],
                colorscale='RdBu',
                colorbar=dict(title='Mean Correlation'),
                opacity=0.8
            ),
            name="Wind Correlation"
        ))

        fig.add_trace(go.Scattermap(
            lat=wind_farms_df['Latitude'],
            lon=wind_farms_df['Longitude'],
            mode='markers',
            marker=dict(
                size=4,
                color='teal',
                opacity=0.8,
            ),
            text=wind_farms_df['Asset'],  # Display asset name on hover
            name='Wind Farms'
        ))

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
        )

        fig.show()

    @staticmethod
    def plot_user_locations(target_coords):
        pass
        # """Plot user locations."""
        # df = pd.DataFrame(target_coords, columns=['Latitude', 'Longitude'])
        #
        # fig = go.Figure(go.Scattergeo(
        #     lat=df['Latitude'],
        #     lon=df['Longitude'],
        #     mode='markers',
        #     marker=dict(
        #         size=8,
        #         color='black',
        #         symbol='x',
        #         opacity=0.8
        #     ),
        #     name="User Locations"
        # ))
        #
        # fig.update_layout(
        #     title="User Locations on Map",
        #     geo=dict(
        #         scope='world',
        #         showland=True,
        #         landcolor="rgb(229, 229, 229)",
        #         center=dict(lat=-25, lon=135),
        #         projection_scale=5
        #     ),
        #     margin=dict(l=0, r=0, t=40, b=0)
        # )
        #
        # fig.show()