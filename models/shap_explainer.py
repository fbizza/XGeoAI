import pandas as pd
import joblib
import shap
import numpy as np
import plotly.graph_objects as go
from config import get_data_path
import plotly.graph_objects as go


CSV_PATH_SHAP = get_data_path('basetables', 'suitability_index_basetable_v6.csv')
MODEL_PATH = get_data_path('models', 'random_forest_model.pkl')

FEATURES_SHAP = [
    'min_distance_to_line_km',
    'mean_correlation_with_existing_farms',
    'avg_capacity_factor',
    'avg_solar_radiation',
    'min_distance_nature_land_km',
]

LATITUDE_COL = 'Latitude'
LONGITUDE_COL = 'Longitude'

# Load model and data
clf_shap = joblib.load(MODEL_PATH)
df_shap = pd.read_csv(CSV_PATH_SHAP)
df_shap.rename(columns={'Mean Correlation': 'mean_correlation_with_existing_farms'}, inplace=True)

X_SHAP = df_shap[FEATURES_SHAP]


shap_explainer = shap.TreeExplainer(clf_shap)


def plot_shap_bar_plotly(lat, lon):
    feature_name_map = {
        "avg_capacity_factor": "Average Wind Capacity Factor",
        "min_distance_to_line_km": "Distance to Electrical Line",
        "mean_correlation_with_existing_farms": "Wind Correlation with Existing Farms",
        "min_distance_nature_land_km": "Distance to Natural Land",
        "avg_solar_radiation": "Average Solar Radiation",
    }

    def wrap_label(text, max_words=2):
        """Insert <br> every `max_words` to wrap long labels."""
        words = text.split()
        return "<br>".join([" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)])

    row = df_shap.loc[np.isclose(df_shap[LATITUDE_COL], lat) & np.isclose(df_shap[LONGITUDE_COL], lon)]
    if row.empty:
        raise ValueError(f"No point found at coordinates ({lat}, {lon}).")
    if len(row) > 1:
        print("Warning: Multiple rows matched. Using the first one.")
    instance = row.iloc[0][FEATURES_SHAP].values.reshape(1, -1)

    shap_values_full = shap_explainer.shap_values(instance)
    if shap_values_full.ndim == 3:
        shap_values_instance = shap_values_full[0, :, 1]
    else:
        shap_values_instance = shap_values_full[0]

    shap_values = shap_values_instance
    features = FEATURES_SHAP

    wrapped_features = [wrap_label(feature_name_map.get(f, f)) for f in features]
    colors = ['#2ecc71' if val > 0 else '#e74c3c' for val in shap_values]
    texts = [f"{val:+.2f}" for val in shap_values]

    sorted_indices = np.argsort(-np.abs(shap_values))
    shap_values_sorted = [shap_values[i] for i in sorted_indices]
    wrapped_features_sorted = [wrapped_features[i] for i in sorted_indices]
    colors_sorted = [colors[i] for i in sorted_indices]
    texts_sorted = [texts[i] for i in sorted_indices]

    fig = go.Figure(go.Bar(
        x=shap_values_sorted,
        y=wrapped_features_sorted,
        orientation='h',
        marker_color=colors_sorted,
        text=texts_sorted,
        textposition='auto',
        insidetextanchor='start',
    ))

    max_val = max(abs(np.min(shap_values)), abs(np.max(shap_values)))
    x_range = [-max_val * 1.2, max_val * 1.2]

    fig.update_layout(
        title=dict(
            text=f"<b>SHAP Explanation</b>",
            x=0.5,
            xanchor='center',
            font=dict(color='#17a2b8')
        ),
        xaxis=dict(
            color='white',
            zeroline=True,
            zerolinecolor='white',
            zerolinewidth=2,
            showgrid=False,
            range=x_range
        ),
        yaxis=dict(
            autorange='reversed',
            color='white',
            tickfont=dict(color='white', size=10),  # Smaller font
            showline=False
        ),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=90, b=20),
        height=360,
        showlegend=False
    )
    return fig

#plot_shap_bar_plotly(-23.5, 124)