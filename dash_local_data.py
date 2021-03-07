import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_table

import pandas as pd
import numpy as np 
import plotly.express as px

import pm

def transitions_to(dfg, app_name):
    data = []
    for k in dfg:
        a1, a2 = k
        if a1 == app_name:
            data.append([a2, dfg[k]])
    return data

def transitions_from(dfg, app_name):
    data = []
    for k in dfg:
        a1, a2 = k
        if a2 == app_name:
            data.append([a1, dfg[k]])
    return data    


def transitions_to_dash_table(transitions):
    transitions.sort(key=lambda x: x[-1], reverse=True)
    table_data = []
    for app, count in transitions:
        table_data.append(
            {"app": app, "trans_freq": count}
        )  
    return table_data

def get_tables_data(dfg, app_name):
    t1 = transitions_to_dash_table(transitions_to(dfg, app_name))
    t2 = transitions_to_dash_table(transitions_from(dfg, app_name))
    return t1, t2  

def update_local_data(df, data, n):
    if data is not None:
        app_name = data['label']
    else:
        app_name = None   
        table_data_to, table_data_from = [], []
        time_strings = [
            html.H4(f"Ttl. usage: Click a Node to Continue"),
            html.H4(f"Avg. usage: Click a Node to Continue"),
        ]
        return table_data_to, table_data_from, time_strings

    if n == "All":
        dfg = pm.get_dfg(df)
        t_avg = pm.get_agg_time(df, app_name=app_name, agg="mean")
        t_tot = pm.get_agg_time(df, app_name=app_name, agg="sum")

    else:    
        n = int(n)
        dfg = pm.get_dfg(df, n)
        t_avg = pm.get_agg_time(df, n, app_name=app_name, agg="mean")
        t_tot = pm.get_agg_time(df, n, app_name=app_name, agg="sum")

    table_data_to, table_data_from = get_tables_data(dfg, app_name)    
   
    time_strings = [
        html.H2(f"{app_name}", style={'color': '#0074D9'}),
        html.H3(f"Ttl. usage: {t_tot}"),
        html.H3(f"Avg. usage: {t_avg}"),
    ]
    return table_data_to, table_data_from, time_strings


def get_app_data(df, app_name, t="minutes", fmt="range"):
    """
    fmt: Labels format (range of date or single date (first one))
    t: time in seconds, hours or minutes
    """
    assert fmt in ["date", "range"]
    assert t in ["minutes", "hours", "seconds"], "Invalid argument `t`"
    title = f"Daily {app_name} usage statistics in {t}"
    
    def _f(duration):
        h, m, s = duration.split(":")
        h, m, s = int(h), int(m), int(s)
        dur = h*60*60 + m*60 + s
        if t == "minutes":
            dur = dur/60
        elif t == "hours":
            dur = dur/3600    
        return dur
    
    _df = df[df['App name']==app_name]
    vals = _df.groupby('id').apply(
        lambda x: x.Duration.apply(
            lambda x: _f(x)
        ).sum())
    labels = _df.groupby('id').apply(
        lambda x: f"{str(x.Time.iloc[-1])}---{str(x.Time.iloc[0])}" if \
        fmt=="range" else f"{str(x.Time.iloc[0]).split(' ')[0]}"
    )
    
    return vals, labels, title  


def update_time_graph(df, data):
    if data is not None:
        app_name = data['label']
        X, Y, title = get_app_data(
            df, 
            app_name,
        )
        
        fig = px.bar(
            Y, X, title=title, 
            y=Y, orientation='h',
            # color='#1DA1F2',
            )        
    else:
        X = [1, 2]
        Y = [0, 2]
        fig = px.bar(
            Y, X, title="Click Node to Continue...", 
            y=Y, orientation='h',
            # color='#1DA1F2',
            )           
    return fig    