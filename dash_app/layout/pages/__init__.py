from dash import page_registry

def register_pages(app):
    for page in page_registry.values():
        app.clientside_callback(
            "function() { return ''; }",
            Output("page-content", "children"),
            Input("url", "pathname")
        )
