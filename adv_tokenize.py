import sys
import os
import re
import glob
import pandas as pd

rrex = re.compile('.*(hindu|christian|islam).*(hindu|christian|islam).*')
grex = re.compile('.*(daughter|wife).*')
drex = re.compile('.*\(native.*district:(.*)\),.*')
bdrex = re.compile('.*born on(.*)\(native district:.*')
for year in range(2008,2020)[::-1]:
    dflist = []
    flist = glob.glob('text/%s*.txt' % year)
    print(year, "Total : ", len(flist))
    rex = re.compile('.*(hindu|christian|christianity|islam).*?to (hindu|christianity|christian|islam).*')
    for i,f in enumerate(flist):
        pages = ""
        with open(f) as fp:
            pages+=fp.read()
        pages = pages.replace(str(int(year)-1), str(year))
        lines = pages.split(str(year))

        from_rel = []
        to_rel = []
        gender = []
        district = []
        bday = []
        for group in lines:
            if 'convert' in group:
                x = "".join(group.split('\n')).lower() + str(year)
                mlist = rrex.search(x)
                glist = grex.search(x)
                dlist = drex.search(x)
                bdlist = bdrex.search(x)
                from_rel.append(mlist.group(1) if mlist != None else 'UNK')
                to_rel.append(mlist.group(2) if mlist != None else 'UNK')
                gender.append('F' if glist != None else 'M')
                district.append(dlist.group(1).strip() if dlist != None else 'UNK')
                if bdlist != None:
                    bdstr = bdlist.group(1).split()
                    if len(bdstr) == 3:
                        day, month, year = bdstr
                    elif len(bdstr) == 2:
                        rex = re.compile('.*([a-z]*)([0-9]*).*')
                        mobj = rex.search(bdstr[1])
                        day = bdstr[0]
                        month = mobj.group(1)
                        year = mobj.group(2)
                    else:
                        print f, group
                        raise
                    day = day.strip('stndrh')
                    bday.append("%s-%s-%s" % (day, month, year))
                else:
                    bday.append('UNK')

        df = pd.DataFrame({'from':from_rel, 'to':to_rel,'gender':gender,
                            'district':district, 'bday': bday})
        year, week = os.path.basename(f).replace('.pdf.txt','').split('_')
        df['year'] = int(year)
        df['week'] = int(week)
        dflist.append(df)


    df = pd.concat(dflist).reset_index(drop=True)
    df.to_csv('%s.csv' % year, index=False)

