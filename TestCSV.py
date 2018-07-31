import requests
from lookerapi import LookerApi



import csv

clientId = 'mZB4cy9cmpCFdb6sctdg'
clientSecret = 'dVr27XhxjqhQqNFShNNwX8rJ'
host = "https://dev.looker.turner.com:19999/api/3.1/"

looker = LookerApi(host=host,
                #host= 'https://dev.looker.turner.com:19999/api/3.1' ,
                 token= clientId,
                 secret = clientSecret)

firstRes = looker.get_look_data(6199, clientId, clientSecret, host)
print(firstRes)

secondRes = looker.get_look_data(6201, clientId, clientSecret, host)
print(secondRes)
countList = []
def findCount(res):
    totalCount = 0
    groupsCount = {}
    sortedRes = sorted(res, key=itemgetter('pdt_dfp_operative_temp.modality'))
    for key, value in itertools.groupby(sortedRes, key=itemgetter('pdt_dfp_operative_temp.modality')):
        print(key)
        keyCount = 0
        for i in value:
            totalCount += i.get('pdt_dfp_operative_temp.total_capacity')
            keyCount += i.get('pdt_dfp_operative_temp.total_capacity')
        groupsCount[key] = keyCount
    return groupsCount

countList.append(findCount(firstRes))
countList.append(findCount(secondRes))

resultsFile = open('C:\Data Files\look_id.csv', 'w', newline='')
with resultsFile as filehandle:
    for listitem in countList:
        filehandle.write('%s\n' % listitem)
