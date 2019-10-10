import sys
import os
import re
import PyPDF2 as pf
import glob
import pandas as pd

for year in range(2008,2019)[::-1]:
    dflist = []
    flist = glob.glob('data/%s*.pdf' % year)
    print("Total :", len(flist))
    rex = re.compile('.*(hindu|christian|islam).*?to (hindu|christianity|islam).*')
    for i,f in enumerate(flist):
        print('DEBUG : %s %s' % (i,f))
        fp = open(f, 'rb')
        pdf = pf.PdfFileReader(fp)
        info = pdf.getDocumentInfo()
        p_num = pdf.getNumPages()
        pm_list = []
        for i in range(p_num):
            text = pdf.getPage(i).extractText()
            text = " ".join(re.findall('[a-zA-Z]+', text))
            mlist = rex.findall(text.lower())
            pm_list += mlist
        if pm_list != []:
            df = pd.DataFrame(pm_list, columns=['from','to'])
            year, week = os.path.basename(f).replace('.pdf','').split('_')
            df['year'] = int(year)
            df['week'] = int(week)
            dflist.append(df)


    df = pd.concat(dflist).reset_index(drop=True)
    df.to_csv('%s.csv' % year, index=False)

