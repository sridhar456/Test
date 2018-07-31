import os, json, requests, errno, re, pandas as pd, csv
import yaml

f = open('config.yml')
params = yaml.load(f)
f.close()
host = 'dev.looker.turner.com'
LOOKER_KEY_SECRET = params['hosts'][host]['secret']
LOOKER_KEY = params['hosts'][host]['token']


def getLookToggleData(branch, look_id):
    key = LOOKER_KEY  # api3
    key_secret = LOOKER_KEY_SECRET

    api_url = "https://dev.looker.turner.com:19999/api/3.0/"
    auth_data = {'client_id': key, 'client_secret': key_secret}
    login_url = 'https://dev.looker.turner.com:19999/api/3.0/login'

    session = requests.Session()
    r = session.post(api_url + "/login", data=auth_data)
    # acquiring access token details
    json_auth = r.json()

    # Query to obtain look id data
    # updating workspace id for the session
    if branch == 'dev':
        session_body = {"workspace_id": "dev"}
        update = session.patch(api_url + "/session", headers={'Authorization': "token " + json_auth['access_token']},
                               data=json.dumps(session_body))

        run_look = requests.get(api_url + '/looks/' + look_id + '/run/json',
                                headers={'Authorization': "token " + json_auth['access_token']})

        devData = run_look.json()
        print(devData)
        print(len(devData))
        return devData
    else:
        master_run_look = requests.get(api_url + '/looks/' + look_id + '/run/json',
                                       headers={'Authorization': "token " + json_auth['access_token']})

        masterData = master_run_look.json()
        print(masterData)
        print(len(masterData))
        return masterData


def finalResults(masterData, devData):
    finalList = []
    # Looping through the parameters in result
    # Saving the result in finalList and finally returning the result
    for diff_param in masterData[0]:
        # if the value is a number perform sum
        # if it's a string get distinct lists in every result and return different elements in each list
        if type(devData[0][diff_param]) == float or type(devData[0][diff_param]) == int:
            print('printing' + diff_param)
            sumList = []
            masterSum = 0
            for elem in masterData:
                if diff_param in elem:
                    masterSum += elem[diff_param]
            sumList.append(masterSum)
            devSum = 0
            for elem in devData:
                if diff_param in elem:
                    devSum += elem[diff_param]
            sumList.append(devSum)
            finalList.append({'master_' + diff_param: sumList[0]})
            finalList.append({'dev_' + diff_param: sumList[1]})
        else:
            diffList = checkDiff(masterData, devData, diff_param)
            finalList.append({'master_' + diff_param: diffList[0]})
            finalList.append({'dev_' + diff_param: diffList[1]})
    return finalList


# return different elements from distinct lists of master and dev data
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


# get distinct elements from masterList and devList
# return different elements in extraList
def checkDiff(masterList, devList, diffParam):
    diffPresent = False
    distinctMasterList = get_distinct_elements(masterList, diffParam)
    print(distinctMasterList)
    distinctDevList = get_distinct_elements(devList, diffParam)
    print(distinctDevList)
    extraList = diff_elem(distinctMasterList, distinctDevList)

    for elem in extraList:
        if len(elem) != 0:
            diffPresent = True

    if diffPresent:
        print("Lists do not match")
    else:
        print("Match")
    return extraList


# return list of distinct elements
def get_distinct_elements(modalityList, parameter):
    distinctElementsList = []
    for elem in modalityList:
        # print(elem)
        if parameter in elem:
            if elem[parameter] not in distinctElementsList:
                distinctElementsList.append(elem[parameter])

    return distinctElementsList


masterData = getLookToggleData('master', '6203')
devData = getLookToggleData('dev', '6203')
finalList = finalResults(masterData, devData)
print(finalList)

resultsFile = open('C:\Data Files\Impression.csv', 'w', newline='')
with resultsFile as filehandle:
    for elem in finalList:
        filehandle.write('%s\n' % elem)

print('done')