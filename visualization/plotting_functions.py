import pandas as pd
import plotly.graph_objects as go


def add_map_layer(fig1, fig2=None):
    if fig2:
        fig1.add_trace(fig2.data[0])
        return fig1
    return fig1


def show_figure(fig):
    fig.show()


def create_scattermap_figure(df, value_column_name=None, marker_size=5, colorscale='RdBu', uniform_color=None, cmin=None, cmax=None, cmid=None):
    if value_column_name:
        column_name = value_column_name
    else:
        other_columns = [col for col in df.columns if col not in ['Latitude', 'Longitude']]
        if not other_columns:
            raise ValueError("No suitable columns found in the dataframe for plotting.")

        column_name = other_columns[0]

    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=marker_size,
            color=uniform_color if uniform_color else df[column_name],
            colorscale=colorscale if not uniform_color else None,
            colorbar=dict(title=column_name) if not uniform_color else None,
            opacity=0.8,
            cmin=cmin,
            cmax=cmax,
            cmid=cmid,
        ),
        name=column_name
    ))

    return fig



def create_wind_correlation_figure(df):
    """Plot wind correlation on a map."""

    data_filepath = "data/processed/wind-farms-with-ERA5_coordinates.csv"

    try:
        # Load the operating wind farms data
        wind_farms_df = pd.read_csv(data_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {data_filepath}")
        return

    other_columns = [col for col in df.columns if col not in ['Latitude', 'Longitude']]
    if not other_columns:
        raise ValueError("No suitable columns found in the dataframe for plotting.")

    column_name = other_columns[0]

    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=7,
            color=df[column_name],
            colorscale='RdBu',
            colorbar=dict(title=column_name),
            opacity=0.8
        ),
        name=column_name
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

    return fig

