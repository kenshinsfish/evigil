import os
import wget
import datetime

url = 'http://www.stationeryprinting.tn.gov.in/gazette/{year}/{weekday}_VI_4.pdf'
url_old = 'http://www.stationeryprinting.tn.gov.in/gazette/{year}/{weekday}-VI-4.pdf'
outfile = '{year}_{weekday}.pdf'
for year in range(2016,2019):
    for weekday in range(1, int(datetime.datetime.now().strftime('%V')) + 1):
        if os.path.exists(outfile.format(year=year,weekday=weekday)):
            print(year + ',' + str(weekday) + ' exists... ')
            continue
        fname = wget.download(url.format(year=year, weekday=weekday), out=outfile.format(year=year,weekday=weekday))
        if os.path.exists(outfile.format(year=year,weekday=weekday)):
            print("Downloaded " + fname)
        else:
            print("Failed " + fname)

def weeks_for_year(year):
    last_week = datetime.date(year,12,28)
    return int(last_week.strftime('%V'))

for year in range(2008,2017)[::-1]:
    for weekday in range(1, weeks_for_year(int(year)) + 1):
        if os.path.exists(outfile.format(year=year,weekday=weekday)):
            print(str(year) + ',' + str(weekday) + ' exists... ')
            continue
        print("%s,%s" % (year , weekday))
        try:
            fname = wget.download(url_old.format(year=year, weekday=weekday), out=outfile.format(year=year,weekday=weekday))
        except:
            try:
                fname = wget.download(url_old.format(year=year, weekday=weekday), out=outfile.format(year=year,weekday=weekday))
            except:
                continue

        if os.path.exists(outfile.format(year=year,weekday=weekday)):
            print("Downloaded " + fname)
        else:
            print("Failed " + fname)
