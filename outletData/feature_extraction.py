import os
import pandas as pd
import numpy as np

event_dir = 'eventData'

if os.path.isdir("featureData") == False:
    os.mkdir("featureData")

total_average_flow = []
total_volume = []
total_duration = []
total_outlet = []

for outlet_events in os.scandir(event_dir):
    
    outlet_name = outlet_events.name.split('_',1)[0]+"_feature"

    event_average_flow = []
    event_volume = []
    event_duration = []
    event_outlet = []
    for event in os.scandir(outlet_events):
        df = pd.read_csv(event.path, sep=' ', header=None)
        event_average_flow.append(df.loc[:,1].mean())
        event_volume.append(df.loc[:,1].sum())
        event_duration.append(df.iloc[-1,0] - df.iloc[0,0] + 1)
        event_outlet.append(outlet_events.name.split('_',1)[0])
        
    data = {
    "AverageFlow": event_average_flow,
    "Volume": event_volume,
    "Duration": event_duration,
    "Outlet": event_outlet
    }
    df = pd.DataFrame(data)
    df.to_csv("featureData"+'/'+outlet_name+".csv", sep=' ', index=False)

    total_average_flow.extend(event_average_flow)
    total_volume.extend(event_volume)
    total_duration.extend(event_duration)
    total_outlet.extend(event_outlet)

data = {
    "AverageFlow": total_average_flow,
    "Volume": total_volume,
    "Duration": total_duration,
    "Outlet": total_outlet
    }

df = pd.DataFrame(data)
df.to_csv("featureData"+'/'+"all_outlets"+".csv", sep=' ', index=False)
    