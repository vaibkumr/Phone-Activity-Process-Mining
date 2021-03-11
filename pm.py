import pandas as pd
import numpy as np
import pm4py

def get_sessions_2(df, sleep_activity="Screen off (locked)",
                   break_span=5):
    """this uses the duration provided in the data"""
    def _hours(t):
        assert len(t) == 3, "Invalid time interval string."
        h, m, _ = t
        return (int(h)*60 + int(m)) / 60

    duration = df.Duration.apply(lambda x: _hours(x.split(":")))
    id = 0
    ids = []
    for i, d in enumerate(duration):
        ids.append(id)
        if d >= break_span and df['App name'].iloc[i] == sleep_activity:
            id += 1
    return ids

def load_data(f, break_span=5):
    df = pd.read_csv(f)
    df = df[~df.Time.isna()].iloc[::-1].iloc[3:, :] #reverse time, skip 3 rows
    df.Time = df.Date + " " + df.Time
    df.Time = pd.to_datetime(df.Time)
    df.drop("Date", axis=1, inplace=True)
    df['id'] = get_sessions_2(df, break_span=break_span)
    return df

def get_dfg(df,
            id=None,
            id_col="id",
            timestamp_col="Time",
            activity_col="App name",
            plot=False,
           ):
    if id is not None:
        _df = df[df.id==id]
    else:
        _df = df
    log = pm4py.format_dataframe(
                                 _df,
                                 case_id=id_col,
                                 activity_key=activity_col,
                                 timestamp_key=timestamp_col
                                )
    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    if plot:
        pm4py.view_dfg(dfg, start_activities, end_activities)
    return dfg

def app_name_to_id(txt):
        return "_".join(txt.split(" ")).lower()

def get_agg_time(df, id=None, app_name=None, agg="sum"):
    assert agg in ["sum", "mean"], "Invalid Argument for `agg`"
    
    if id is not None: _df = df[df.id==id]
    else: _df = df

    if app_name is not None: _df = _df[_df['App name']==app_name]    
        
    def _f(t):
        h, m, s = t.split(":")
        return int(h)*60*60 + int(m)*60 + int(s)
    
    if agg == "sum": t = _df.Duration.apply(_f).sum()
    else: t = _df.Duration.apply(_f).mean()

    try:
        hours = int(t//3600)
        mins = int((t - hours*60*60)//60)
        seconds = int((t - hours*60*60 - mins*60)%60)
    except:
        hours, mins, seconds = "NA", "NA", "NA"
    s = f"{hours} hours {mins} Minutes and {seconds} seconds"
    return s 

def get_layout_dropdown_options():
    """
    Refer: https://dash.plotly.com/cytoscape/layout
    """
    layouts = [
        'circle',
        'breadthfirst',
        'cola',
        'cose-bilkent',
        'euler',
        'spread',
        'dagre',
        'klay',
        'random',
        'grid',
        'concentric',
        'cose',
    ]
    return [{'label': l, 'value': l} for l in layouts]   


  




