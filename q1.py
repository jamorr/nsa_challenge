import pandas as pd
from datetime import datetime

# df = pd.read_csv("login.txt", sep="\t", parse_dates=[[0,1]], header=None)
df = pd.read_csv("login.txt", sep="\t",  header=None)

df[2].unique()

df[["First Letter", "Name"]] = df[2].str.split(".", expand=True)
df[["First Letter", "Name"]] = df[2].str.split(".", expand=True)


enames = df[df["First Letter"]=="e"]
i = 0

anomalies = {}
#For every E name
for name in enames[2].unique():
    logs = enames.loc[df[2] == name]
    #For every day for that person
    for time in logs[0].unique():
        #Makes a dataframe of every action on that day
        day = logs.loc[logs[0] == time]
        #If there are more than two actions (did more than clock in/out)
        #Then name is added to dictionary
        if len(day) > 2:
            anomalies[name] = time
    if i%50 == 0:
        print(f"{i}/{len(enames[2].unique())}")
    i+=1
        
        
    #Check if length of name dataframe > 2
anomalies.keys()