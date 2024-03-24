import pandas as pd
import numpy as np

outlet_list = ["kitchenBasin", "showerHead", "washingMachine", "washroomBasin"]

for outlet in outlet_list:
    df = pd.read_csv("flowData/"+outlet+".csv", sep=' ')
    outlet_ts = df.to_numpy()
    binVal = np.zeros([len(outlet_ts), 1])
    flow_val = outlet_ts[:,1]

    for index in range(len(outlet_ts)):
        outlet_ts[index,1] = 1 if outlet_ts[index,1] > 0 else 0

    np.savetxt('binaryData/' + outlet + '_bin.csv', outlet_ts, delimiter=' ',fmt="%d")