import pandas as pd
import hashlib

df = pd.read_csv('dns_logs.txt.gz', compression='gzip', sep="\t", header=None)
df.columns = ["times", "ip", "domain"]
df['times'] = pd.to_datetime(df['times'], unit='s')
df["tdiff"] = df.groupby(["ip","domain"])["times"].diff()
df["tdiff"] = df["tdiff"].astype("int64")
df["tdiff"] = df["tdiff"].apply(lambda x: pd.NA if x < 0 else x)
df.dropna(inplace=True)
vs = {}
for n, grp in df.groupby(["domain","ip"]):
    if len(grp) > 75:
        vs[n] = grp["tdiff"].var()
vs_df = pd.Series(vs)
vs_df = vs_df.iloc[:10]
# print(", ".join(vs_df["level_1"].sort_values().unique()))
st = "c2.robotland.org, hamma.doubutsutaikai.jp, mx.yellowjello.br, not4u.mechaworld.ru, www.tanglerootinn.in.ua, 128.61.188.8, 128.61.54.78, 130.207.106.45, 130.207.213.18, 130.207.243.14, 130.207.47.207, 143.215.0.38, 143.215.182.109, 143.215.26.32, 143.215.58.72"
hsash = hashlib.md5(st.encode('utf-8')).hexdigest()