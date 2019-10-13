import pandas as pd
import glob

files = glob.glob('yearly_data/*.csv')
dflist = []
for f in files:
    df = pd.read_csv(f)
    dflist.append(df)

df = pd.concat(dflist).reset_index(drop=True)
dfhi = df[(df['from'] == 'hindu') & (df['to'] == 'islam')]
print("h->i = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'hindu') & (df['to'] == 'chris')]
print("h->c = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'islam') & (df['to'] == 'hindu')]
print("i->h = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'islam') & (df['to'] == 'chris')]
print("i->c = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'chris') & (df['to'] == 'islam')]
print("c->i = ",dfhi.shape[0])
dfhi = df[(df['from'] == 'chris') & (df['to'] == 'hindu')]
print("c->h = ",dfhi.shape[0])
