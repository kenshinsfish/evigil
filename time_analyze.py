import pandas as pd
import glob

files = glob.glob('*.csv')
dflist = []
for f in files:
    df = pd.read_csv(f, index_col=[0])
    dflist.append(df)

df = pd.concat(dflist).reset_index(drop=True)
#df['wy'] = df['year'].astype('str') + '-W' + df['week'].astype('str') + '-1'
#df['date'] = pd.to_datetime(df['wy'],format="%Y-W%W-%w")
#df.drop('wy',axis=1)
df.to_csv('y.csv')
