import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import plotly.express as px
import json
import dash_table

DEFAULT_STYLESHEET = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65,
            'z-index': 9999,
            'label': 'data(label)',
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
            'target-arrow-shape': 'vee',
            "opacity": 0.45,
            'z-index': 5000
        }
    },
    {
        'selector': '.followerNode',
        'style': {
            'background-color': '#0074D9'
        }
    },
    {
        'selector': '.followerEdge',
        "style": {
            "mid-target-arrow-color": "blue",
            "mid-target-arrow-shape": "vee",
            "line-color": "#0074D9"
        }
    },
    {
        'selector': '.followingNode',
        'style': {
            'background-color': '#FF4136'
        }
    },
    {
        'selector': '.followingEdge',
        "style": {
            "mid-target-arrow-color": "red",
            "mid-target-arrow-shape": "vee",
            "line-color": "#FF4136",
        }
    },
    {
        "selector": '.genesis',
        "style": {
            'background-color': '#B10DC9',
            "border-width": 2,
            "border-color": "purple",
            "border-opacity": 1,
            "opacity": 1,

            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 20,
            'z-index': 9999
        }
    },
    {
        'selector': ':selected',
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "black",
            "font-size": 20,
            'z-index': 9999
        }
    }
]

STYLES = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 80px)'}
}

def get_dropdown_options(df):
    labels = df.groupby('id').apply(lambda x: f"{str(x.Time.iloc[-1])}---{str(x.Time.iloc[0])}")
    ids = df.id.unique()
    return [{'label': "All", 'value': "All"}] +\
        [{'label': labels[i], 'value': ids[i]} for i in range(len(ids))]