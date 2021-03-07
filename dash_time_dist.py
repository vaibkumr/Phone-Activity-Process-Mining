import pandas as pd
import numpy as np 
import plotly.express as px

def get_time_dist(df):
    def _f(duration):
        h, m, s = duration.split(":")
        h, m, s = int(h), int(m), int(s)
        return h*60*60 + m*60 + s

    time_series = df.groupby('App name').apply(
            lambda x: x.Duration.apply(
                lambda x: _f(x)
            ).sum()/3600)
    
    time_df = pd.DataFrame({
    "apps": list(time_series.index),
    "time": list(time_series.values),
    })
    exclude = [
        "Screen off (locked)",
        "Screen off (unlocked)",
        "Screen off",
        "Screen on (locked)",
        "Screen on (unlocked)",
        "Screen on",
    ]
    return time_df[~time_df.apps.isin(exclude)]



def update_time_dist_graph(df, n, options):
    if n == "All":
        _df = df
    else:    
        _df = df[df.id==int(n)]
    time_df = get_time_dist(_df)  
    for option in options:
        if option['value'] == n:
            time_period = option['label']
    fig = px.pie(
        time_df, 
        values='time', 
        names='apps', 
        title=f'App Time Distribution for {time_period}'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig