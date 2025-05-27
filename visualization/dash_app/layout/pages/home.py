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
            ]),



            html.H4("Solar Radiation", className="text-center mt-3"),
            html.P([
                html.Span("Solar radiation", style={"fontWeight": "bold"}),
                " is included to assess environmental conditions and potential for hybrid energy systems. "
                "It also provides insight into climate and land use characteristics."
            ]),
            html.H4("Model fittizio", className="text-center mt-3"),
            html.P([
                html.Span("Solar radiation", style={"fontWeight": "bold"}),
                " is included to assess environmental conditions and potential for hybrid energy systems. "
                "It also provides insight into climate and land use characteristics."
            ]),
            html.H4("Scoring and normalization", className="text-center mt-3"),
            html.P([
                html.Span("Solar radiation", style={"fontWeight": "bold"}),
                " is included to assess environmental conditions and potential for hybrid energy systems. "
                "It also provides insight into climate and land use characteristics."
            ])
        ]),

# Data Sources
        html.Div([
            html.H2("Data Sources", className="my-3", style={"color": "#17A2B8"}),
            html.P([
                "The predictions are based on a combination of geospatial and meteorological datasets, including:"
            ]),
            html.Ul([
                html.Li([
                    html.Span("ERA5 reanalysis data", style={"fontWeight": "bold"}),
                    " from ECMWF for wind speed and temperature"
                ]),
                html.Li([
                    html.Span("NASA POWER Project", style={"fontWeight": "bold"}),
                    " for solar radiation measurements"
                ]),
                html.Li([
                    html.Span("SRTM elevation data", style={"fontWeight": "bold"}),
                    " for terrain analysis"
                ]),
                html.Li([
                    html.Span("OpenStreetMap", style={"fontWeight": "bold"}),
                    " for land use and proximity to infrastructure"
                ]),
            ])
        ], className="mb-4"),

    ], fluid=True)
])
