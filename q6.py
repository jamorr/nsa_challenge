
from collections import defaultdict
import pandas as pd
import math

# read data
df = pd.read_csv("logins.txt", sep="\t", parse_dates=[[0,1]], header=None, dtype_backend="pyarrow")
# rename cols
df.columns = ["datetime", "uname", "login"]
# split names
df[["First Letter", "Name"]] = df["uname"].str.split(".", expand=True)
# limit to relevant time frame
df = df.set_index("datetime")
df = df["2021-06-01":"2021-08-30"]
# get rid of leading out and trailing in
cdf = df.groupby('uname').apply(lambda x: x.iloc[1:] if x['login'].iloc[0] == 'OUT' else x)
cdf = cdf.drop("uname", axis=1).reset_index()
cdf = cdf.groupby('uname').apply(lambda x: x.iloc[:-1] if x['login'].iloc[-1] == 'IN' else x)
cdf = cdf.drop("uname", axis=1).reset_index()


# get difference in login and logout times
results = {}
for n, group in cdf.groupby('uname'):
    ins = group[group['login'] == 'IN']['datetime'].astype("int64").values
    outs = group[group['login'] == 'OUT']['datetime'].astype("int64").values
    diff = []
    for in_time, out_time in zip(ins, outs):
        time_diff = out_time - in_time
        diff.append(math.log(max(1,time_diff)))
    ldiff = (len(diff)-len(group[group['login'] == 'IN']['datetime']))
    # pad diff
    if ldiff < 0:
        diff.append(0)

    results[n] = {"diff":diff, "ins":group[group['login'] == 'IN']['datetime']}

time_variance = {}
for name, data in results.items():
    res_df = pd.DataFrame(data)
    res_df["month"] = res_df["ins"].dt.month
    june = res_df[res_df["month"]==6]
    aug = res_df[res_df["month"]==8]
    time_variance[name] = (aug["diff"].var(), june["diff"].var())


v_by_name_df = pd.DataFrame(time_variance).T
v_by_name_df.nsmallest(5, 0)

largest = v_by_name_df.nlargest(5, 0).index
for name in largest:
    print(name)
    res_df = pd.DataFrame(results[name])
    res_df.plot(x="ins", y="diff")


# find people with largest mean in time logged in august and june
# and the variance difference between aug and june
time_mean = {}
for name, data in results.items():
    res_df = pd.DataFrame(data)
    res_df["month"] = res_df["ins"].dt.month
    june = res_df[res_df["month"]==6]["diff"].mean()
    aug = res_df[res_df["month"]==8]["diff"].mean()
    time_mean[name] = (aug, june, (june-aug)**2)

mean_by_name_df = pd.DataFrame(time_mean).T
mean_by_name_df.nlargest(5,0)

largest = mean_by_name_df.nlargest(5, 2).index
for name in largest:
    print(name)
    res_df = pd.DataFrame(results[name])
    res_df.plot(x="ins", y="diff")