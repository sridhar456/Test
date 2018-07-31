import os, json, requests, errno, re, pandas as pd, csv
from lookerapi import LookerApi
import fields

LOOKER_KEY = 'mZB4cy9cmpCFdb6sctdg'
LOOKER_KEY_SECRET = 'dVr27XhxjqhQqNFShNNwX8rJ'


def getLookToggleData(look_id, diff_param):
    key = LOOKER_KEY  # api3
    key_secret = LOOKER_KEY_SECRET


    api_url = "https://dev.looker.turner.com:19999/api/3.1/"
    auth_data = {'client_id': key, 'client_secret': key_secret}
    login_url = 'https://dev.looker.turner.com:19999/api/3.1/login'
    lookURL = 'https://dev.looker.turner.com:19999/api/3.1/looks/' + look_id + '/run/json'

    #if branch != 'dev':
    #   api_url = "https://looker.turner.com:19999/api/3.1/"
    #   login_url = 'https://looker.turner.com:19999/api/3.1/login'
    #    lookURL = 'https://looker.turner.com:19999/api/3.1/looks/' + look_id + '/run/json'

    session = requests.Session()
    r = session.post(api_url + "/login", data=auth_data)
    json_auth = r.json()

    master_run_look = requests.get(api_url + '/looks/' + look_id + '/run/json',
                                   headers={'Authorization': "token " + json_auth['access_token']})

    masterData = master_run_look.json()
    print(masterData)
    print(len(masterData))

    session_body = {"workspace_id": "dev"}
    update = session.patch(api_url + "/session", headers={'Authorization': "token " + json_auth['access_token']},
                           data=json.dumps(session_body))

    run_look = requests.get(api_url + '/looks/' + look_id + '/run/json',
                            headers={'Authorization': "token " + json_auth['access_token']})

    devData = run_look.json()
    print(devData)
    print(len(devData))
    diffList = checkDiff(masterData, devData, diff_param)
    return diffList


def diff_elem(masterList, devList):
    extraMasterList = []
    extraDevList = []
    extraList = []
    for elem in masterList:
        if elem not in devList:
            extraMasterList.append(elem)
        else:
            devList.remove(elem)

    extraDevList = devList
    extraList.append(extraMasterList)
    extraList.append(extraDevList)
    return extraList


def checkDiff(masterList, devList, diffParam):
    diffPresent = False
    distinctMasterList = fields.get_distinct_elements(masterList,diffParam)
    print(distinctMasterList)
    distinctDevList = fields.get_distinct_elements(devList, diffParam)
    print(distinctDevList)
    extraList = fields.diff_elem(distinctMasterList, distinctDevList)

    for elem in extraList:
        if len(elem) != 0:
            diffPresent = True

    if diffPresent:
        print("Lists do not match")
    else:
        print("Match")


masterData = getLookToggleData('6203', 'master')
# resultsFile = open('C:\Data Files\master_look_id.csv', 'w', newline='')
# with resultsFile as filehandle:
#     writer = csv.writer(filehandle)
#     for elem in masterData:
#         writer.writerow(elem)
devData = getLookToggleData('6203', 'dev')
print(masterData)
print(devData)
# print(fields.get_distinct_elements(devData, 'staq_advertiser_analysis_t.product2'))
#
checkDiff(masterData, devData, 'staq_advertiser_analysis_t.turner_site')

print('done')

