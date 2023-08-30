from dash import Dash, html


def create_dash_app(server):

    dash_app = Dash(
        server=server,
        url_base_pathname="/visualizer/",
    )

    # ------ Layout Logic ------ # 
    dash_app.layout = html.Div([
        html.Div(children="Application Setup...")
    ])


    return dash_app.server

