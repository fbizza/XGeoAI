from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([

        html.H1("Wind Farm Suitability Explorer", className='text-center my-4'),

        # Intro Paragraph (centered, no heading)
        html.P([
        "This application allows users to explore wind farm development potential through two complementary tools. "
        "The first is an interactive suitability mapper where users can assign custom weights to key environmental and infrastructural "
        "variables to generate and compare personalized suitability index maps. The second is a demonstration of explainable AI (XAI) techniques: "
        "a black-box classification model, trained on synthetic data, predicts site suitability and allows users to select individual points on the map "
        "to view local explanations using LIME and SHAP."
        ], className="text-center mb-4"),



        # Variables Explanation
        html.Div([
            html.H2("Variables Explanation", className="my-3", style={"color": "#17A2B8"}),

            html.P([
                "In studies of wind farm suitability, a wide variety of variables are typically considered. This tool focuses on just ",
                html.Span("5", style={"fontWeight": "bold"}),
                " key variables to illustrate the overall framework rather than provide a production-ready solution. However, the system is designed to be easily extended in the future to incorporate additional factors. Below is a more detailed explanation of these variables:"
            ]),


            # Wind correlation
            html.Div([
                html.H5("Correlation With Existing Farms", className="text-center mt-3"),
                html.P([
                    "This variable measures how much the wind profile at a given location is correlated with locations where wind farms already operate. "
                    "For each location, we compute the average correlation of its wind speed time series with those of existing wind farm sites across Australia. "
                    "The idea is that if a new wind farm is too highly correlated with existing ones, their production patterns may rise and fall together, "
                    "which can lead to more variability in the overall energy supply. Ideally, this correlation should be minimized to promote more consistent and diversified energy production across the grid."
                ], className="text-center", style={"fontSize": "0.9rem"}),

                html.Div([
                    html.Img(
                        src="/assets/images/time_series.png",
                        style={
                            "display": "block",
                            "margin": "0 auto",
                            "maxWidth": "650px",
                            "height": "auto"
                        }
                    ),
                    html.P("Example of wind speed time series correlation.",
                           className="text-center mt-2", style={"fontSize": "0.8rem", "color": "#aaa"})
                ], className="my-3"),

                html.Div([
                    html.Img(
                        src="/assets/images/correlation_matrix.png",
                        style={
                            "display": "block",
                            "margin": "0 auto",
                            "maxWidth": "650px",
                            "height": "auto"
                        }
                    ),
                    html.P("Wind correlation matrix: each entry represents the correlation between the 2 locations. (Triangular matrix)",
                           className="text-center mt-2", style={"fontSize": "0.8rem", "color": "#aaa"})
                ], className="my-3"),

                html.P([
                    "The data source for this variable is wind speed measured at 100 meters above ground level from the ",
                    html.A("ECMWF Reanalysis 5th Generation (ERA5)",
                           href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview",
                           target="_blank", style={"textDecoration": "underline"}),
                    " dataset, with 0.25° spatial and 1-hour temporal resolution. The methodology was inspired by ",
                    html.A("Gunn et al, 2023.",
                           href="https://iopscience.iop.org/article/10.1088/1748-9326/ad0253",
                           target="_blank", style={"textDecoration": "underline"}),
                ], className="text-center", style={"fontSize": "0.9rem"})
            ], style={"marginBottom": "5rem"}),

            # Wind capacity factor
            html.Div([
                html.H5("Wind Capacity Factor", className="text-center mt-3"),
                html.P([
                    "For each location in Australia, this variable represents the average capacity factor estimated over two years. "
                    "Capacity factor is a proxy related to wind speed, reflecting how effectively wind can be converted into energy. "
                    "Wind speed is mapped through a characteristic curve (shown below) that relates wind speed to power output. "
                    "Ideally, capacity factor should be maximized to improve wind farm performance."
                ], className="text-center", style={"fontSize": "0.9rem"}),

                html.Div([
                    html.Img(
                        src="/assets/images/power_curve.png",
                        style={
                            "display": "block",
                            "margin": "0 auto",
                            "maxWidth": "500px",
                            "height": "auto"
                        }
                    )
                ], className="my-3"),

                html.P([
                    "The data source for this variable is wind speed measured at 100 meters above ground level from the ",
                    html.A("ECMWF Reanalysis 5th Generation (ERA5)",
                           href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview",
                           target="_blank", style={"textDecoration": "underline"}),
                    " dataset, with 0.25° spatial and 1-hour temporal resolution."
                ], className="text-center", style={"fontSize": "0.9rem"})
            ], style={"marginBottom": "5rem"}),

            # Distances
            html.Div([
                html.H5("Distance to Electrical Grid and to Nature Land", className="text-center mt-3"),

                html.Div([
                    html.P([
                        "For the electrical grid, the goal is to minimize the distance in order to reduce connection costs and transmission losses. "
                        "Conversely, distance to natural land should be maximized."
                    ], style={"fontSize": "0.9rem", "margin": "0 auto"}),

                    html.Ul([
                        html.Li([
                            html.Span("Electrical grid data from: "),
                            html.A("Australian Digital Atlas",
                                   href="https://digital.atlas.gov.au/datasets/70f23e91102a4d6899a776d093fa08ef_2/explore",
                                   target="_blank", style={"textDecoration": "underline"})
                        ]),
                        html.Li([
                            html.Span("Protected nature land data from: "),
                            html.A("Australian Protected Areas Database",
                                   href="https://www.dcceew.gov.au/environment/land/nrs/science/capad",
                                   target="_blank", style={"textDecoration": "underline"})
                        ])
                    ], style={
                        "fontSize": "0.9rem",
                        "margin": "1rem 11rem 0 auto",
                        "maxWidth": "750px",
                        "textAlign": "left",
                        "listStylePosition": "inside"
                    })
                ], style={"textAlign": "center"})
            ], style={"marginBottom": "5rem"}),


            # Solar radiation
            html.Div([
                html.H5("Solar Radiation", className="text-center mt-3"),
                html.Div([
                    html.P([
                        "Solar radiation is calculated in terms of surface irradiance (W/m²) and is included as an example of how the same metric can act as either a benefit or a cost in the suitability index, depending on the development goals."
                    ], style={"fontSize": "0.9rem", "margin": "0 auto"}),

                    html.Ul([
                        html.Li([
                            html.Span("Cost: ", style={"color": "red", "fontWeight": "bold"}),
                            "High irradiance might indicate that a location is better suited for photovoltaic development rather than wind energy. In this case, high solar radiation is penalized."
                        ]),
                        html.Li([
                            html.Span("Benefit: ", style={"color": "green", "fontWeight": "bold"}),
                            "If the objective is to co-locate wind and solar farms, then high irradiance is a positive factor, increasing the site's overall suitability."
                        ])
                    ], style={
                        "fontSize": "0.9rem",
                        "marginTop": "1rem",
                        "marginLeft": "auto",
                        "marginRight": "auto",
                        "maxWidth": "750px",
                        "textAlign": "left",
                        "listStylePosition": "inside"
                    })
                ], style={"textAlign": "center"}),
                    html.P([
                    "In this demo this variable is treated as a cost. Meaning that locations with lower solar irradiance will have higher suitability scores. The data source used for computing mean solar irradiance is: ",
                    html.A("ECMWF Reanalysis 5th Generation (ERA5)",
                           href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview",
                           target="_blank", style={"textDecoration": "underline"}),
                    " dataset, with 0.25° spatial and 1-hour temporal resolution."
                ], className="text-center", style={"fontSize": "0.9rem"})
            ], style={"marginBottom": "5rem"}),

        ]),

        # Suitability Index
        html.Div([
            html.H2("Suitability Index", className="my-3", style={"color": "#17A2B8"}),

            html.P([
                "The Suitability Index provides a single interpretable metric that reflects how appropriate a given location is for wind farm development. "
                "It is computed as a linear combination of the five normalized variables described above, using the weights defined by the user. "
                "These weights are set via sliders or input fields and always sum to 1."
            ], style={"fontSize": "0.9rem"}),

            html.P([
                "Since the input variables differ in units, distributions, and scales, a score normalization system is used to ensure comparability and improve explainability. "
                "Each variable is converted into a score ranging from 0 to 100 using percentiles. "
                "For example, if a location is closer to the electrical grid than 76% of other locations, it will receive a score of 77/100 for the 'distance to grid' metric. "
                "This transformation allows for consistent comparison and clearer interpretations."
            ], style={"fontSize": "0.9rem",}),

            html.Div([
                html.Img(
                    src="/assets/images/percentile_scores.png",
                    style={
                        "display": "block",
                        "margin": "1.5rem auto 1rem auto",
                        "maxWidth": "750px",
                        "height": "auto"
                    }
                ),
                html.P("Percentile score normalization: each variable is transformed to a 0–100 scale. Then linearly combined with the other variables.",
                       className="text-center mt-2", style={"fontSize": "0.8rem", "color": "#aaa"})
            ], className="my-3"),

            html.P([
                "Once each variable is normalized into a percentile score, they are linearly combined using the custom user defined weights to calculate the final Suitability Index for each location. "
            ], style={"fontSize": "0.9rem"})
        ], style={"marginBottom": "5rem"}),

        # AI Model
        html.Div([
            html.H2("AI Model", className="my-3", style={"color": "#17A2B8"}),

            html.P([
                "The goal of this tool is not to deliver the most accurate model for wind farm siting, but rather to demonstrate how explainable XAI techniques can be integrated to provide local explanations of each location's suitability. "
                "To support this, the model is trained using only the five variables introduced earlier, and the training data is synthetically generated."
            ], style={"fontSize": "0.9rem"}),

            html.P([
                "The synthetic dataset is built using a suitability index computed with the following weights, plus a small random noise added to each variable (with a mean offset of 10%):"
            ], style={"fontSize": "0.9rem"}),

            html.Div([
                html.Div([
                    html.Span("Distance to electrical grid: ", style={"fontWeight": "bold"}),
                    "0.4"
                ]),
                html.Div([
                    html.Span("Wind correlation with existing farms: ", style={"fontWeight": "bold"}),
                    "0.2"
                ]),
                html.Div([
                    html.Span("Wind capacity factor: ", style={"fontWeight": "bold"}),
                    "0.2"
                ]),
                html.Div([
                    html.Span("Solar radiation: ", style={"fontWeight": "bold"}),
                    "0.05"
                ]),
                html.Div([
                    html.Span("Distance to protected nature land: ", style={"fontWeight": "bold"}),
                    "0.15"
                ])
            ], style={
                "fontSize": "0.9rem",
                "margin": "0 auto 1rem auto",
                "maxWidth": "750px",
                "textAlign": "center"
            }),
            html.P([
                "Based on this weighted suitability score, the top 20% of locations are labeled as suitable (positive examples), and the remaining 80% as not suitable (negative examples). "
                "A Random Forest classifier is then trained on this dataset, achieving precision, recall, and accuracy all above 90%."
            ], style={"fontSize": "0.9rem"}),

            html.P([
                "Of course, this is a simplification. Real-world models are typically trained on highly imbalanced datasets and involve more complex data pipelines. "
                "Here, the design is intentionally simplified to keep the focus on exploring and understanding model predictions using XAI."
            ], style={"fontSize": "0.9rem"})
        ], className="mb-4"),

        # Lime
html.Div([
            html.H2("Lime hints", className="my-3", style={"color": "#17A2B8"}),

            html.Div([
                html.Img(
                    src="/assets/images/lime.png",
                    style={
                        "display": "block",
                        "margin": "1.5rem auto 1rem auto",
                        "maxWidth": "750px",
                        "height": "auto"
                    }
                ),
            ], className="my-3"),

        ], style={"marginBottom": "5rem"}),

    ], fluid=True)
])
