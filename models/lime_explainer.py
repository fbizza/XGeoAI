import pandas as pd
import joblib
from lime.lime_tabular import LimeTabularExplainer
import plotly.graph_objects as go
from config import get_data_path


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
        "mean_correlation_with_existing_farms": "Wind Correlation with Existing Farms",
        "min_distance_nature_land_km": "Distance to Natural Land",
        "avg_solar_radiation": "Average Solar Radiation",
    }

    mapped = []
    for condition in conditions:
        for feature in feature_name_map:
            if feature in condition:
                mapped.append(feature_name_map[feature])
                break
    return mapped


def explain_with_lime(lat, lon):

    feature_name_map = {
        "avg_capacity_factor": "Average Wind Capacity Factor",
        "min_distance_to_line_km": "Distance to Electrical Line",
        "mean_correlation_with_existing_farms": "Wind Correlation with Existing Farms",
        "min_distance_nature_land_km": "Distance to Natural Land",
        "avg_solar_radiation": "Average Solar Radiation",
    }

    def wrap_label(text, max_words=2):
        # to not use too much horizontal space
        words = text.split()
        return "<br>".join([" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)])

    row = lime_df.loc[(lime_df[LATITUDE_COL] == lat) & (lime_df[LONGITUDE_COL] == lon)]

    if row.empty:
        raise ValueError(f"No point found at coordinates ({lat}, {lon}).")
    elif len(row) > 1:
        print("Warning: Multiple rows matched. Using the first one.")

    instance = row.iloc[0][FEATURES].values.reshape(1, -1)

    probs = clf.predict_proba(instance)[0]
    class_names = ['Not Suitable', 'Suitable']

    exp = explainer.explain_instance(
        data_row=instance.flatten(),
        predict_fn=lambda x: clf.predict_proba(pd.DataFrame(x, columns=FEATURES)),
        num_features=len(FEATURES)
    )

    explanation_data = exp.as_list()
    full_labels = [label for label, _ in explanation_data]
    contributions = [contrib for _, contrib in explanation_data]

    mapped_labels = []
    for label in full_labels:
        for raw_feature, pretty in feature_name_map.items():
            if raw_feature in label:
                mapped_labels.append(wrap_label(pretty))
                break
        else:
            mapped_labels.append(label)  # fallback to raw if no match

    # LIME feature importance figure
    lime_fig = go.Figure(go.Bar(
        x=contributions,
        y=mapped_labels,
        orientation='h',
        marker_color=['#2ecc71' if v > 0 else '#e74c3c' for v in contributions],
        text=[f"{v:.2f}" for v in contributions],
        textposition='auto'
    ))

    lime_fig.update_layout(
        title=dict(
            text='<b>LIME Explanation</b>',
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
            range=[-max(abs(min(contributions)), max(contributions)) * 1.2,
                   max(abs(min(contributions)), max(contributions)) * 1.2],
        ),
        yaxis=dict(
            autorange='reversed',
            color='white',
            tickfont=dict(color='white', size=10),  # 👈 Smaller font
            showline=False
        ),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=90, b=20),
        height=360,
        showlegend=False
    )

    # classification probabilities
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
            text='<b>Prediction Probabilities</b>',
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

    return lime_fig, prob_fig, mapped_labels




#explain_with_lime(-28.25, 116.25)
