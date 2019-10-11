import sys
import os
import re
import pdftotext as pt
import glob
import pandas as pd
for year in range(2019,2020)[::-1]:
    dflist = []
    flist = glob.glob('text/%s*.txt' % year)
    print("Total :", len(flist))
    rex = re.compile('.*(hindu|christian|christianity|islam).*?to (hindu|christianity|christian|islam).*')
    for i,f in enumerate(flist):
        pages = ""
        with open(f) as fp:
            pages+=fp.read()
        lines = pages.split(str(year))
        for group in lines:
            if 'convert' in group:
                x = "".join(group.split('\n')).lower()
                if 'convert' in x:
                    rrex = re.compile('.*(hindu|christian|islam).*(hindu|christian|islam).*')
                    grex = re.compile('.*(daughter|wife).*')
                    mlist = rrex.search(x)
                    glist = grex.search(x)
                    from_rel.append(mlist.group(1) if mlist != None else 'UNK')
                    to_rel.append(mlist.group(1) if mlist != None else 'UNK')
                    from_gender.append('F' if glist != None else 'UNK')

                    from_gender.append('UNK')
                    if rex.search(x) != None:
                        from_gender = 'F'
                    else:
                        from_gender = 'M'

                df = pd.DataFrame({'from':from_rel, 'to':to_rel,'gender':from_gender})
                year, week = os.path.basename(f).replace('.txt','').split('_')
                df['year'] = int(year)
                df['week'] = int(week)
                dflist.append(df)


    df = pd.concat(dflist).reset_index(drop=True)
    df.to_csv('%s.csv' % year, index=False)

