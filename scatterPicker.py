import base64
import io
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("CSV Scatter Plot")
        ], width={'size': 12})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id="upload_csv",
                children=html.Div([
                    "Drag and Drop or ",
                    html.A("Select Files")
                ]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px"
                },
                multiple=False
            )
        ], width={'size': 12})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="x_dropdown", placeholder="Select X-axis")
        ], width={'size': 6}),
        dbc.Col([
            dcc.Dropdown(id="y_dropdown", placeholder="Select Y-axis")
        ], width={'size': 6}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="scatter_plot",
                config={"displayModeBar": True, "scrollZoom": True},
                style={"width": "800px", "height": "800px", "margin": "auto"},
            ),
        ], width={'size': 12})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Export CSV", id="export_button", outline=True, color="primary"),
            dcc.Download(id="download_csv")
        ], width={'size': 12})
    ]),
    dcc.Store(id="stored_selected_data")
], fluid=True)

@app.callback(
    Output("x_dropdown", "options"),
    Output("y_dropdown", "options"),
    Input("upload_csv", "contents"),
    State("upload_csv", "filename"),
    prevent_initial_call=True
)
def open_csv(contents, filename):
    if contents and filename:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        global df
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        options = [{"label": col, "value": col} for col in df.columns]
        return options, options
    return [], []

@app.callback(
    Output("scatter_plot", "figure"),
    Input("x_dropdown", "value"),
    Input("y_dropdown", "value"),
    prevent_initial_call=True
)
def create_scatter_plot(x, y):
    if x and y:
        fig = px.scatter(df, x=x, y=y, hover_data=df.columns)
        fig.update_traces(selected=dict(marker=dict(color="orange")), unselected=dict(marker=dict(opacity=0.3)))
        return fig
    return dash.no_update

@app.callback(
    Output("stored_selected_data", "data"),
    Input("scatter_plot", "selectedData"),
    prevent_initial_call=True
)
def store_selected_data(selected_data):
    if selected_data and "points" in selected_data:
        selected_indices = [point["pointIndex"] for point in selected_data["points"]]
        selected_df = df.iloc[selected_indices]
        return selected_df.to_dict("records")
    return dash.no_update

@app.callback(
    Output("download_csv", "data"),
    Input("export_button", "n_clicks"),
    State("stored_selected_data", "data"),
    prevent_initial_call=True
)
def export_data(n_clicks, stored_selected_data):
    if stored_selected_data:
        selected_df = pd.DataFrame(stored_selected_data)
        return dcc.send_data_frame(selected_df.to_csv, "selected_data.csv", index=False)
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
