import pandas as pd
# read data
df = pd.read_csv("logins.txt", sep="\t", parse_dates=[[0,1]], header=None, dtype_backend="pyarrow")
# rename cols
df.columns = ["datetime", "uname", "login"]
# split names
df[["First Letter", "Name"]] = df["uname"].str.split(".", expand=True)
# convert to
# df = df.convert_dtypes(dtype_backend="pyarrow")
jdf = df.loc[df["First Letter"]=="j"]
# get just the times in string format
jdf["time"] = jdf["datetime"].dt.time
# count number of unique login times by name
jdf.groupby("Name")["time"].nunique().sort_values().tail(1)