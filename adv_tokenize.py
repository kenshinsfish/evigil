import sys
import os
import re
import glob
import pandas as pd
m_map = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05',
        'jun':'06', 'jul':'07', 'aug':'08', 'sep':'09',
        'oct':'10', 'nov':'11', 'dec':'12'}
rrex = re.compile('.*(hindu|christian|islam).*(hindu|christian|islam).*')
grex = re.compile('.*(daughter|wife).*')
drex = re.compile('.*\(native.*district:(.*)\),.*')
bdrex = re.compile('.*born[ ]*on(.*)\([ ]*native[ ]*district[ ]*:.*')
cdrex = re.compile('convert.*? on[ ]+(.*?[0-9]{4})')
for year in range(2008,2020)[::-1]:
    dflist = []
    flist = glob.glob('text/%s*.txt' % year)
    print(year, "Total : ", len(flist))
    rex = re.compile('.*(hindu|christian|christianity|islam).*?to (hindu|christianity|christian|islam).*')
    for i,f in enumerate(flist):
        pages = ""
        with open(f) as fp:
            pages+=fp.read()
        year, week = os.path.basename(f).replace('.pdf.txt','').split('_')
        if int(week) == 1:
            pages.replace(str(int(year)-1),str(year))
        lines = pages.split(str(int(year)))

        from_rel = []
        to_rel = []
        gender = []
        district = []
        bday = []
        cday = []
        for group in lines:
            if 'convert' in group:
                y = " ".join(group.split('\n')) + str(year)
                x = " ".join(group.split('\n')).lower() + str(year)
                y = y.format(CURRENTYEAR=str(year))
                x = x.format(currentyear=str(year))
                mlist = rrex.search(x)
                glist = grex.search(x)
                dlist = drex.search(x)
                bdlist = bdrex.search(x)
                cdlist = cdrex.search(x)
                from_rel.append(mlist.group(1) if mlist != None else 'UNK')
                to_rel.append(mlist.group(2) if mlist != None else 'UNK')
                gender.append('F' if glist != None else 'M')
                district.append(dlist.group(1).strip() if dlist != None else 'UNK')
                if bdlist != None:
                    bdstr = bdlist.group(1).split()
                    if len(bdstr) == 3:
                        day, month, byear = bdstr
                    elif len(bdstr) == 2:
                        rex = re.compile('.*([a-z]*)([0-9]*).*')
                        mobj = rex.search(bdstr[1])
                        day = bdstr[0]
                        month = mobj.group(1)
                        byear = mobj.group(2)
                    else:
                        print f, group
                        raise
                    day = day.strip('stndrh')
                    try:
                        bday.append("%s-%s-%s" % (day, m_map[month.lower()[:3]], byear))
                    except:
                        print month, f, group
                else:
                    bday.append('UNK')

                if cdlist != None:
                    cdstr = cdlist.group(1).strip().split()
                    if len(cdstr) == 3:
                        day, month, cyear = cdstr
                    elif len(cdstr) == 2:
                        rex = re.compile('.*([a-z]*)([0-9]*).*')
                        mobj = rex.search(cdstr[1])
                        day = cdstr[0]
                        month = mobj.group(1)
                        cyear = mobj.group(2)
                    else:
                        print group, cdstr, f
                        raise
                    day = day.strip('stndrh')
                    try:
                        cday.append("%s-%s-%s" % (day, m_map[month.lower()[:3]], cyear))
                    except Exception as e:
                        print month.lower(), f
                        print group
                        print e
                        raw_input()
                else:
                    cday.append('UNK')

        df = pd.DataFrame({'from':from_rel, 'to':to_rel,'gender':gender,
            'district':district, 'bday': bday, 'cday' : cday})
        df['year'] = year
        df['week'] = week
        dflist.append(df)


    df = pd.concat(dflist).reset_index(drop=True)
    df['wy'] = '1' + '-W' + df['week'].astype('str') + '-' + df['year'].astype('str') 
    df['regdate'] = pd.to_datetime(df['wy'],format="%w-W%W-%Y")
    df = df.drop('wy',axis=1)
    df.to_csv('%s.csv' % year, index=False)

