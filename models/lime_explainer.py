import pandas as pd
import joblib
from lime.lime_tabular import LimeTabularExplainer
import plotly.graph_objects as go
from config import get_data_path

# Constants and loading model/data done once
CSV_PATH = get_data_path('basetables', 'suitability_index_basetable_v6.csv')
MODEL_PATH = get_data_path('models', 'random_forest_model.pkl')

FEATURES = [
    'min_distance_to_line_km',
    'mean_correlation_with_existing_farms',
    'avg_capacity_factor',
    'avg_solar_radiation',
    'min_distance_nature_land_km',
]
LATITUDE_COL = 'Latitude'
LONGITUDE_COL = 'Longitude'

# Load model and data once, keep global
clf = joblib.load(MODEL_PATH)
lime_df = pd.read_csv(CSV_PATH)
lime_df.rename(columns={'Mean Correlation': 'mean_correlation_with_existing_farms'}, inplace=True)
X = lime_df[FEATURES]

explainer = LimeTabularExplainer(
    training_data=X.values,
    feature_names=FEATURES,
    class_names=['Not Suitable', 'Suitable'],
    mode='classification',
    random_state=29
)


def explain_with_lime(lat, lon):
    """
    Explain prediction at given lat, lon and show LIME + prediction probability.
    """
    row = lime_df.loc[(lime_df[LATITUDE_COL] == lat) & (lime_df[LONGITUDE_COL] == lon)]

    if row.empty:
        raise ValueError(f"No point found at coordinates ({lat}, {lon}).")
    elif len(row) > 1:
        print("Warning: Multiple rows matched. Using the first one.")

    instance = row.iloc[0][FEATURES].values.reshape(1, -1)

    # Predict probabilities
    probs = clf.predict_proba(instance)[0]
    predicted_class = clf.predict(instance)[0]
    class_names = ['Not Suitable', 'Suitable']


    # === LIME Explanation ===
    exp = explainer.explain_instance(
        data_row=instance.flatten(),
        predict_fn=lambda x: clf.predict_proba(pd.DataFrame(x, columns=FEATURES)),
        num_features=len(FEATURES)
    )

    explanation_data = exp.as_list()
    labels, contributions = zip(*explanation_data)

    # === Plot LIME Contributions ===
    lime_fig = go.Figure(go.Bar(
        x=contributions,
        y=labels,
        orientation='h',
        marker_color=['green' if v > 0 else 'red' for v in contributions],
        text=[f"{v:.2f}" for v in contributions],
        textposition='outside'
    ))

    lime_fig.update_layout(
        title=f'LIME Explanation for Point @ ({lat}, {lon})',
        xaxis_title='Contribution to Prediction',
        yaxis={'autorange': 'reversed'},
        template='plotly_white',
        margin=dict(l=150, r=40, t=50, b=40)
    )


    # === Plot Probability Bar ===
    prob_fig = go.Figure(go.Bar(
        x=probs,
        y=class_names,
        orientation='h',
        marker_color='steelblue',
        text=[f"{p:.2f}" for p in probs],
        textposition='outside'
    ))

    prob_fig.update_layout(
        title=f'Prediction Probabilities @ ({lat}, {lon})',
        xaxis_title='Probability',
        yaxis={'autorange': 'reversed'},
        template='plotly_white',
        margin=dict(l=150, r=40, t=50, b=40)
    )


    return lime_fig, prob_fig


#explain_with_lime(-28.25, 116.25)
