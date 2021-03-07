import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import plotly.express as px
import json
import dash_table

from pm import *
import dash_time_dist
import dash_local_data
import dash_dfg
import dash_utils
import configparser


# Load Log data
config = configparser.ConfigParser()
config.read('config.ini')
f = config['DEFAULT']['log_file']
break_span = int(config['DEFAULT']['break_span'])
df = load_data(f, break_span)

# Initialize Dash
asset_path = "assets"
app = dash.Dash(__name__, assets_folder=asset_path)
dropdown_options = dash_utils.get_dropdown_options(df)
dash_data = dash_dfg.dfg_to_dash(get_dfg(df))


################################## APP LAYOUT ################################
cyto.load_extra_layouts() #Load more graph layouts
default_stylesheet = dash_utils.DEFAULT_STYLESHEET
styles = dash_utils.STYLES


app.layout = html.Div([
    html.Div(className='eight columns', children=[
        #Left Side
        html.H3("Process Mining | Directly Follows Graph:"),
        html.Div(children=[
            dcc.Dropdown(
                    id='number-dropdown',
                    options=dropdown_options,
                    value='All',
                    style={'width': '560px', 'margin-left':'5px'},
                ),
            dcc.Dropdown(
                    id='layout-dropdown',
                    options=get_layout_dropdown_options(),
                    value='cola',
                    style={'width': '200px', 'margin-left':'30px'},
                ),                

            html.P(
                "Graph Resolution Slider:", 
                style={'margin-left':'60px', "color": "#0074D9"}
                ),
            html.Div(children=[
                dcc.Slider(
                    id='res-slider',
                    min=0,
                    max=100,
                    step=5,
                    value=60,
                )], 
                style={'width': '300px', 'margin-top': '5px'}
            ),
        ], style=dict(display='flex')),

        cyto.Cytoscape(
            id='cytoscape',
            elements=dash_data,
            layout={'name': 'cola'},
            style={'width': '100%', 'height': '95vh'},
            stylesheet = default_stylesheet,    
        ),
    ]),
    #Right Side
    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='App Transition and Time Information', children=[
            
                html.Div(id='local_avg_time', children=[
                    html.H1("Average App Usage Time: NO NODE SELECTED")
                ]),
            
                dcc.Graph(
                    id="time-graph-chart",
                ),

                html.H3(
                        "Directly Previous Apps Transitions:",
                        # style={'color': '#0074D9'}
                ),

                dash_table.DataTable(
                    id='local_transition_from_table',
                    columns=[
                        {'name': 'Directly Previous App','id': 'app',},
                        {'name': 'Transition Frequency','id': 'trans_freq',}
                    ],
                    data=[{"app": "Select a node from the dfg", "trans_freq": 1}],
                    style_cell=dict(textAlign='left'),
                    style_header=dict(color="#fff", backgroundColor="#1DA1F2"),
                ),    
                
                html.H3(
                        "Directly Next Apps Transitions:",
                        # style={'color': '#0074D9'}
                ),
                dash_table.DataTable(
                    id='local_transition_to_table',
                    columns=[
                        {'name': 'Directly Next App','id': 'app',},
                        {'name': 'Transition Frequency','id': 'trans_freq',}
                    ],
                    data=[{"app": "Select a node from the dfg", "trans_freq": 1}],
                    style_cell=dict(textAlign='left'),
                    style_header=dict(color="#fff", backgroundColor="#1DA1F2"),
                )
            ]),
            dcc.Tab(label='Time Distribution', children=[
                dcc.Graph(
                    id="apps-time-chart",
                ),
            ]),            
        ]),
    ])
])

############################# DASH CALLBACKS #############################

@app.callback(Output('cytoscape', 'layout'),
              Input('layout-dropdown', 'value'))
def update_layout(layout):
    return {'name': layout}


@app.callback(Output('cytoscape', 'elements'),
              [Input('number-dropdown', 'value'),
              Input('res-slider', 'value')])
def update_dfg_res(n, res):
    return dash_dfg.update_dfg_res(df, n, res)    
     

@app.callback(Output('time-graph-chart', 'figure'),
              [Input('cytoscape', 'tapNodeData')])
def update_time_graph(data):
    return dash_local_data.update_time_graph(df, data)


@app.callback(Output('apps-time-chart', 'figure'),
              [Input('number-dropdown', 'value'),
              Input('number-dropdown', 'options')])
def update_time_dist_graph(n, options):
    return dash_time_dist.update_time_dist_graph(df, n, options)


@app.callback([
        Output('local_transition_to_table', 'data'),
        Output('local_transition_from_table', 'data'),
        Output('local_avg_time', 'children')
    ],
    [
        Input('cytoscape', 'tapNodeData'),
        Input('number-dropdown', 'value')
    ])
def update_local_data(data, n):
    return dash_local_data.update_local_data(df, data, n)

if __name__ == "__main__":
    app.run_server()