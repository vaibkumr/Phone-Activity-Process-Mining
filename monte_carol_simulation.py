import pandas as pd
import numpy as np
import tqdm
from pm import *


class MyBehaviourSimulator():
    def __init__(self, f, max_steps = 100, 
                 start_app="Screen on (unlocked)", 
                 end_app="Screen off (locked)"
                ):
        self.f = f
        self.max_steps = max_steps
        self.transitions = self.get_transitions()
        self.START = start_app
        self.END = end_app
        self.current_app = None
        self.i = None
        self.done = False

    
    def get_transitions(self):
        df = pd.read_csv(self.f)
        df = df.iloc[::-1].iloc[4:, :]
        df.columns = ["app_name", "date", "time", "duration"]
        df['next_app'] = df.app_name.shift(-1)
        transitions = {}
        for app in df.next_app.unique():
            val_counts = df[df.app_name == app].next_app.value_counts()
            transitions[app] = val_counts/val_counts.sum()        
        return transitions
    
    def reset(self):
        self.i = 0
        self.current_app = self.START
        self.done = False
        return self.current_app, self.done
    
    def next_app(self, app, rf):
        t = self.transitions[app]
        
        if rf is not None:
            flip = np.random.rand()
            if flip <= rf:
                c = np.random.choice(t.index)
            else:
                c = np.random.choice(t.index, p=t.values)
            return c
        
        return np.random.choice(t.index, p=t.values)
    
    def step(self, rf=None):
        if self.i >= self.max_steps:
            self.done = True
            return None, self.done
        
        self.current_app = self.next_app(self.current_app, rf)
        if self.current_app == self.END:
            self.done = True
        return self.current_app, self.done



def monte_carlo_sim(f, start, end, N=1000, rf=None):
    def append(path, app):
        return path + " -> " + app
    
    paths = []
    env = MyBehaviourSimulator(f, start_app=start, end_app=end)
    for _ in tqdm.tqdm(range(N)):
        cur_app, done = env.reset()
        path = cur_app
        while True:
            cur_app, done = env.step(rf)
            path = append(path, cur_app)
            if done:
                paths.append(path)
                break
    return paths

def df_to_dash(x, l=100):
    table_data = []
    for path, conf in zip(x.paths.values[:l], x.confidence.values[:l]):
        table_data.append(
            {"mc_path": path, "mc_confidence": conf}
        ) 
    return [table_data]


def update_mc_paths(paths, limit=100):
    l1 = len(paths)
    l2 = len(list(set(paths)))
    u_paths, counts = np.unique(paths, return_counts=True)
    df = pd.DataFrame({"paths": u_paths, "counts": counts})
    df = df.sort_values(by=['counts'], ascending=False)
    df["confidence"] = df.counts.apply(lambda x: x/df.counts.sum())
    return df_to_dash(df, limit) 

def get_mc_paths(f, n, irr, start, end):
    paths = monte_carlo_sim(f, start, end, n, irr)  
    return update_mc_paths(paths)    