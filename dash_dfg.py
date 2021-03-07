import pm
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np 
import plotly.express as px

import pm


def dfg_to_dash(dfg):
    
    def get_id(txt):
        return "_".join(txt.split(" ")).lower()
    
    def get_nodes(dfg):
        nodes = []
        for x in dfg:
            nodes.append(x[0])
            nodes.append(x[1])
        return list(set(nodes))
    
    nodes = get_nodes(dfg)
    dash_data = []
    #append nodes
    for x in nodes:
        d = {'data': {'id': get_id(x), 'label': x}}
        dash_data.append(d)

    #append edges
    for (x1, x2) in dfg:
        d = {'data': {'source': get_id(x1), 'target': get_id(x2), "label": dfg[(x1, x2)]}}
        dash_data.append(d)
    return dash_data    


def get_res_cutoff_dfg(dfg, res):
    try:
        cutoff = np.percentile(list(dfg.values()), 100-res)
    except:
        cutoff = -1
    return {k:v for (k, v) in dfg.items() if v >= cutoff}  

def update_dfg_res(df, n, res):
    if n == "All":
        dfg = pm.get_dfg(df)
    else:
        n = int(n)
        dfg = pm.get_dfg(df, n)
    dfg = get_res_cutoff_dfg(dfg, int(res))
    return dfg_to_dash(dfg)  
