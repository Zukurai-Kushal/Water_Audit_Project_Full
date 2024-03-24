import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

event_dir = 'eventData'

for outlet_events in os.scandir(event_dir):
    
    outlet_name = outlet_events.name.split('_',1)[0]
    maxActivity = 0
    prime_df = pd.DataFrame()

    for event in os.scandir(outlet_events):
        df = pd.read_csv(event.path, sep=' ', header=None, names=['Time (s)','Flowrate (ml/s)'])
        currActivity = len(df.index)
        if currActivity>maxActivity:
            maxActivity = currActivity
            prime_df = df
    
    ax = prime_df.plot(kind='line', use_index=True, y = 'Flowrate (ml/s)', figsize = (16, 9), style='-o')
    ax.set_xlabel("Time (s)")
    plt.show()
    fig = ax.get_figure()
    fig.savefig('../plot_figures/'+outlet_name+'.pdf')