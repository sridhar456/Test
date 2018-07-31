import sys
import os
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

dashboards_to_delete = 4
host = 'dev.looker.turner.com'


### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

myhost = params['hosts'][host]['host']
mysecret = params['hosts'][host ]['secret']
mytoken = params['hosts'][host]['token']

looker = LookerApi(host=myhost,
                   token=mytoken,
                   secret=mysecret)



looker.__init__(looker, mytoken, mysecret, myhost)
### ------- HANDLE ARGUMENT FILELIST OR SINGLE LOOK -------

if os.path.isfile(dashboards_to_delete):
	filelist = open(dashboards_to_delete)
	for i in filelist:
		print("deleting dashboard id: " + i)
		data = looker.delete_dashboard(i)
		pprint(data)
else:
	data = looker.all_dashboards()
	pprint(data)

### ------- Done -------

print("Done")

