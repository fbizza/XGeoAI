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
    # Find the row for the given lat, lon
    row = df_shap.loc[np.isclose(df_shap[LATITUDE_COL], lat) & np.isclose(df_shap[LONGITUDE_COL], lon)]
    if row.empty:
        raise ValueError(f"No point found at coordinates ({lat}, {lon}).")
    if len(row) > 1:
        print("Warning: Multiple rows matched. Using the first one.")
    instance = row.iloc[0][FEATURES_SHAP].values.reshape(1, -1)

    # Get shap_values for class 1 (binary case)
    shap_values_full = shap_explainer.shap_values(instance)
    if shap_values_full.ndim == 3:
        shap_values_instance = shap_values_full[0, :, 1]
    else:
        shap_values_instance = shap_values_full[0]

    shap_values = shap_values_instance
    features = FEATURES_SHAP

    colors = ['#2ecc71' if val > 0 else '#e74c3c' for val in shap_values]

    fig = go.Figure(go.Bar(
        x=shap_values,
        y=features,
        orientation='h',
        marker_color=colors,
        text=[f"{val:+.2f}" for val in shap_values],
        textposition='auto',  # <-- Let Plotly handle placement
        insidetextanchor='start',  # Safer for small/negative bars
    ))

    # Add buffer to both ends of x-axis
    x_buffer = 0.1 * (np.max(np.abs(shap_values)) or 1)
    x_min = np.min(shap_values) - x_buffer
    x_max = np.max(shap_values) + x_buffer

    fig.update_layout(
        title=f"SHAP Values for point ({lat}, {lon})",
        xaxis=dict(
            title="SHAP Value",
            range=[x_min, x_max],
            zeroline=True,
            zerolinecolor='gray',
            zerolinewidth=1
        ),
        template='plotly_white',
        margin=dict(l=150, r=50, t=50, b=50)
    )

    fig.show()
plot_shap_bar_plotly(-23.5, 124)