import pandas as pd
import numpy as np

outlet_list = ["kitchenBasin", "showerHead", "washingMachine", "washroomBasin"]
waterMeter_df = pd.DataFrame({"time":[], "flow":[]})

for outlet in outlet_list:
    curr_df = pd.read_csv("outletData/flowData/"+outlet+".csv", sep=' ', names=["time","flow"])
    waterMeter_df = waterMeter_df.append(curr_df, ignore_index=True)

waterMeter_df.sort_values("time", inplace=True)
bool_series = waterMeter_df["time"].duplicated()

print(waterMeter_df.head(50))
print(waterMeter_df[bool_series])