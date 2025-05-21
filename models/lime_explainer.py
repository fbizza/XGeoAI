import pandas as pd
import joblib
from lime.lime_tabular import LimeTabularExplainer
import plotly.graph_objects as go
import re
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



def extract_and_map_features(conditions):
    feature_name_map = {
        "avg_capacity_factor": "Average Wind Capacity Factor",
        "min_distance_to_line_km": "Distance to Electrical Line",
        "mean_correlation_with_existing_farms": "Wind Correlation wit Existing Farms",
        "min_distance_nature_land_km": "Distance to Natural Land",
        "avg_solar_radiation": "Average Solar Radiation",
    }

    mapped = []
    for condition in conditions:
        for feature in feature_name_map:
            if feature in condition:
                mapped.append(feature_name_map[feature])
                break  # Preserve order by stopping at first match
    return mapped


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

    ## === LIME Explanation ===
    exp = explainer.explain_instance(
        data_row=instance.flatten(),
        predict_fn=lambda x: clf.predict_proba(pd.DataFrame(x, columns=FEATURES)),
        num_features=len(FEATURES)
    )

    explanation_data = exp.as_list()

    # Short Y-ticks like Feature 1, Feature 2, etc.
    short_labels = [f"Feature {i+1}" for i in range(len(explanation_data))]
    full_labels = [label for label, _ in explanation_data]
    contributions = [contrib for _, contrib in explanation_data]

    # === Plot LIME Contributions ===
    lime_fig = go.Figure(go.Bar(
        x=contributions,
        y=short_labels,
        orientation='h',
        marker_color=['#2ecc71' if v > 0 else '#e74c3c' for v in contributions],
        text=[f"{v:.2f}" for v in contributions],
        textposition='auto'
    ))

    lime_fig.update_layout(
        title=dict(
            text='LIME Explanation',
            x=0.5,
            xanchor='center',
            font=dict(color='#17a2b8')
        ),
        xaxis=dict(
            title='Contribution to Prediction',
            color='white',
            zeroline=True,
            zerolinecolor='white',
            zerolinewidth=2,
            showgrid=False,
            range=[-max(abs(min(contributions)), max(contributions)) * 1.2,
                   max(abs(min(contributions)), max(contributions)) * 1.2],
        ),
        yaxis=dict(
            autorange='reversed',
            color='white',
            showline=False,
            tickfont=dict(color='white')
        ),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=50, b=60),
        height=360,
        showlegend=False
    )


    # === Plot Vertical Probability Bars ===
    colors = ['#2ecc71' if cls == 'Suitable' else '#e74c3c' for cls in class_names]

    prob_fig = go.Figure(go.Bar(
        x=class_names,
        y=probs,
        marker_color=colors,
        text=[f"{p:.2f}" for p in probs],
        textposition='auto'
    ))

    prob_fig.update_layout(
        title=dict(
            text='Prediction Probabilities',
            x=0.5,
            xanchor='center',
            font=dict(color='#17a2b8')
        ),
        yaxis_title='Probability',
        xaxis=dict(color='white'),
        yaxis=dict(color='white', range=[0, 1]),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f',
        font=dict(color='white'),
        margin=dict(t=50, b=50),
        showlegend=False
    )

    return lime_fig, prob_fig, extract_and_map_features(full_labels)



#explain_with_lime(-28.25, 116.25)
