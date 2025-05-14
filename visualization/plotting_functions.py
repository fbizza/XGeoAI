import pandas as pd
import plotly.graph_objects as go


def add_map_layer(fig1, fig2=None):
    if fig2:
        fig1.add_trace(fig2.data[0])
        return fig1
    return fig1


def show_figure(fig):
    fig.show()


def create_scattermap_figure(df, value_column_name=None, marker_size=5, colorscale='RdBu', uniform_color=None,
                             cmin=None, cmax=None, cmid=None, opacity=0.8):
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
            opacity=opacity,
            cmin=cmin,
            cmax=cmax,
            cmid=cmid,
        ),
        name=column_name,
    ))

    return fig

def create_suitability_index_scattermap_figure(df, value_column_name=None, marker_size=5, colorscale='RdBu',
                                               uniform_color=None, cmin=None, cmax=None, cmid=None,
                                               opacity=0.8, selected_point=None):
    if value_column_name:
        column_name = value_column_name
    else:
        other_columns = [col for col in df.columns if col not in ['Latitude', 'Longitude']]
        if not other_columns:
            raise ValueError("No suitable columns found in the dataframe for plotting.")
        column_name = other_columns[0]

    custom_data_columns = ["Latitude", "Longitude", "suitability_index", "score_km", "score_wind_correlation",
                           "score_wind_capacity", "score_solar_radiation", "min_distance_to_line_km",
                           "avg_capacity_factor", "Mean Correlation", "avg_solar_radiation"]
    df['custom_data_combined'] = df[custom_data_columns].values.tolist()




    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=marker_size,
            color=uniform_color if uniform_color else df[column_name],
            colorscale=colorscale if not uniform_color else None,
            colorbar=dict(title=column_name) if not uniform_color else None,
            opacity=opacity,
            cmin=cmin,
            cmax=cmax,
            cmid=cmid,
        ),
        name=column_name,
        customdata=df['custom_data_combined'],
    ))

    # Add a highlighted point if selected
    if selected_point:
        lat_sel = selected_point["lat"]
        lon_sel = selected_point["lon"]

        fig.add_trace(go.Scattermap(
            lat=[lat_sel],
            lon=[lon_sel],
            mode='markers',
            marker=dict(
                size=15,
                color='yellow',
                symbol='star',
                opacity=1,
            ),
            name="Selected Point",
            hoverinfo='skip'
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
        opacity=0.4,
        name=None
    ))
    return fig


