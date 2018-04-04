import yaml ### install the pyyaml package
import json
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint



### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = ''

# Users you want to add to a group
user_ids = []
# Group you want to add users to
group_id =

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)

### ------- OPEN ADD USERS TO A GROUP -------

for i in user_ids:
    looker.add_users_to_group(group_id, i)
