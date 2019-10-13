import pandas as pd
import glob

files = glob.glob('yearly_data/*.csv')
dflist = []
for f in files:
    df = pd.read_csv(f)
    dflist.append(df)

df = pd.concat(dflist).reset_index(drop=True)
df = df[df['cday'] != 'UNK']
df = df[df['regdate'] != 'UNK']
df['regdate'] =  pd.to_datetime(df['regdate'], format='%Y-%m-%d', errors='coerce')
df['cday'] =  pd.to_datetime(df['cday'], format='%Y-%m-%d', errors='coerce')
df['delay'] = df['regdate'] -  df['cday']
df = df[df['delay'] >= pd.Timedelta(0)]
df.to_csv('gazette_curated.csv')
dfhi = df[(df['from'] == 'hindu') & (df['to'] == 'islam')]
print("h->i = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
dfhi = df[(df['from'] == 'hindu') & (df['to'] == 'chris')]
print("h->c = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
dfhi = df[(df['from'] == 'islam') & (df['to'] == 'hindu')]
print("i->h = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
dfhi = df[(df['from'] == 'islam') & (df['to'] == 'chris')]
print("i->c = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
dfhi = df[(df['from'] == 'chris') & (df['to'] == 'islam')]
print("c->i = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
dfhi = df[(df['from'] == 'chris') & (df['to'] == 'hindu')]
print("c->h = ",dfhi.shape[0])
print("Mean reporting time : ", dfhi.delay.describe())
