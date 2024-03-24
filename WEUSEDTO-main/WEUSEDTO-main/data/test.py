import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt

appendList = ["example.csv", "example2.csv"]

list_df_households = []

for file in appendList:
  df = pd.read_csv(file, sep=' ', header=None, names=['time','flow'])
  #print(df.head(50))
  #print(df.info())
  list_df_households.append(df)

#print(list_df_households)

df_household = pd.DataFrame()

for df in list_df_households:
  df_household = (df_household.append(df, ignore_index=True))
  print(df_household)


df_household_dup = df_household[df_household['time'].duplicated() == True]

print(df_household.head())
print("duplicated rows:", df_household_dup)


#df['time'] = pd.to_datetime(df['time'], unit='s')
