from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

outlet_name = "washingMachine"

fig = plt.figure(figsize = (16, 9))
ax = plt.axes(projection ="3d")
   

ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.3,
        alpha = 0.2)

my_cmap = plt.get_cmap('hsv')

df = pd.read_csv("featureData/"+"all_outlets"+".csv", sep=' ')
# print(df.head(50))
# xdata = df.iloc[:,0]
# ydata = df.iloc[:,1]
# zdata = df.iloc[:,2]

# sctt = ax.scatter3D(xdata, ydata, zdata,
#                     alpha = 0.8,
#                     c = (zdata),
#                     cmap = my_cmap)

# plt.title(outlet_name+"3D scatter plot")
# ax.set_xlabel('Average Event Flowrate (ml/s)', fontweight ='bold')
# ax.set_ylabel('Total Volume of Event (ml)', fontweight ='bold')
# ax.set_zlabel('Event Duration (s)', fontweight ='bold')
# fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)
# plt.show()

fig = plt.figure(figsize=(12, 9))
ax = Axes3D(fig)

for grp_name, grp_idx in df.groupby('Outlet').groups.items():
    y = df.iloc[grp_idx,1]
    x = df.iloc[grp_idx,0]
    z = df.iloc[grp_idx,2]
    ax.scatter(x,y,z, label=grp_name)  # this way you can control color/marker/size of each group freely

ax.set_xlabel('Average Event Flowrate (ml/s)', fontweight ='bold')
ax.set_ylabel('Total Volume of Event (ml)', fontweight ='bold')
ax.set_zlabel('Event Duration (s)', fontweight ='bold')

ax.legend()
plt.show()