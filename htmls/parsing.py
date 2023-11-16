from bs4 import BeautifulSoup
import pandas as pd

schoolNames = 'names.txt'
readNames = open(schoolNames, 'r')
i = 0
schools = []
schoolsString = ''
for x in readNames:
    schoolsString = x

schoolsString = schoolsString.replace("'",'').replace("]",'').replace("[",'')

schools = schoolsString.split(',')
schoolsHTML = []
for x in schools:
    schoolsHTML.append(x+'.html')
    i += 1

if len(schoolsHTML) == len(set(schoolsHTML)):
    print('no duplicate')
#print(i)
#print(schoolsHTML)
numDicts = 0
list = []
tempSeason1 = ''
tempSeason2 = ''


for file in schoolsHTML:
    print(file)
    soup = BeautifulSoup(open(file), features='lxml')

    data = soup.find_all('td')
    rowDict = {}
    for row in data:
        line = str(row)
        if 'data-stat=' in line:
            #gets header
            statKey = line.split('data-stat="')[-1].split('"')[0]
            #Fills the dictionary with data
            if statKey == 'season' or statKey == 'coaches' or statKey == 'conf_abbr':
                try:
                    stat = line.split('data-stat="')[1].split('">')[2].split('<')[0]
                except:
                    stat = line.split('data-stat="')[1].split('">')[1].split('<')[0]
            else:
                stat = line.split('data-stat="')[1].split('">')[1].split('<')[0]
            if 'school' not in rowDict.keys():
                rowDict['school'] = file[:-5]
            rowDict[statKey] = stat
            
            #Need to only record seasons finishing after 1938
            if statKey == 'season':
                tempSeason = stat.split('-')[0]
                
            if statKey == 'coaches':
                if tempSeason != 'nm':
                    if int(tempSeason) > 1938:
                        list.append(rowDict)
                        numDicts += 1
                rowDict = {}
                
            #print(statKey + stat)
            #print(schoolsHTML[0][:-5])
            #print(stat)
#print(list)
print(numDicts)
df = pd.DataFrame.from_dict(list,orient='columns')

print(df)
df.to_csv('combinedCBBStats.csv')


