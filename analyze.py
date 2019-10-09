import pandas as pd
import glob

files = glob.glob('*.csv')
dflist = []
for f in files:
    df = pd.read_csv(f)
    dflist.append(df)

df = pd.concat(dflist).reset_index(drop=True)
dfhi = df[(df['from'] == 'hindu') & (df['to'] == 'islam')]
print("h->i = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'hindu') & ((df['to'] == 'christianity') | (df['to'] == 'christian'))]
print("h->c = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'islam') & (df['to'] == 'hindu')]
print("i->h = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'islam') & ((df['to'] == 'christianity') | (df['to'] == 'christian'))]
print("i->c = ",dfhi.shape[0])
dfhi = df[((df['from'] == 'christianity') | (df['from'] == 'christian')) & (df['to'] == 'islam')]
print("c->i = ",dfhi.shape[0])
dfhi = df[((df['from'] == 'christianity') | (df['from'] == 'christian')) & (df['to'] == 'hindu')]
print("c->h = ",dfhi.shape[0])
