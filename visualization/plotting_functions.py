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

def create_lines_figure(df, latitude_column_name, longitude_column_name):
    latitudes = df[latitude_column_name]
    longitudes = df[longitude_column_name]
    fig = go.Figure(go.Scattermap(
        mode="lines",
        lat=latitudes,
        lon=longitudes,
        line=dict(width=1, color="red"),
        name="Transmission Lines",
        opacity=0.4,
        showlegend=False
    ))
    return fig


