# -*- coding: UTF-8 -*-
my_host = 'YOUR HOST'
my_secret = 'YOUR SECRET'
my_token = 'YOUR ID'

from pprint import pprint as pp
import json
import csv
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ## LOOKER API CLASS [[ its in the lookerapi object you may be importing! - uncomment the 3rd Line!]]

class LookerApi(object):

    def __init__(self, token, secret, host):

        self.token = token
        self.secret = secret
        self.host = host

        self.session = requests.Session()
        self.session.verify = False
        self.auth()

    def auth(self):
        url = '{}{}'.format(self.host,'login')
        params = {'client_id':self.token,
                  'client_secret':self.secret
                  }
        r = self.session.post(url,params=params)
        access_token = r.json().get('access_token')
        # print access_token
        self.session.headers.update({'Authorization': 'token {}'.format(access_token)})

# GET /lookml_models/{{NAME}}
    def get_model(self,model_name="",fields={}):
        url = '{}{}/{}'.format(self.host,'lookml_models', model_name)
        print url
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
# GET /lookml_models/{{NAME}}
    def get_model(self,model_name=None,fields={}):
        url = '{}{}/{}'.format(self.host,'lookml_models', model_name)
        # print url
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /lookml_models/{{NAME}}/explores/{{NAME}}
    def get_explore(self,model_name=None,explore_name=None,fields={}):
        url = '{}{}/{}/{}/{}'.format(self.host,'lookml_models', model_name, 'explores', explore_name)
        print url
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#GET      queries/run/
    def run_inline_query(self,body={}):
            url = '{}{}/run/json'.format(self.host,'queries')
            # print url
            params = json.dumps(body)
            # print " --- running query --- "
            r = self.session.post(url,data=params)
            # print url
            # print r.status_code
            # print r
            if r.status_code == requests.codes.ok:
                return r.json()

## --------- csv writing -------

def write_fields(explore,value):
	model,exp= explore.split(',')

	# ### compile the line - this is possible to combine above, but here to keep things simple
	rowout = []
	rowout.append(model)
	rowout.append(exp)
	rowout.append(value)


	w.writerow(rowout)

## --------- csv formatting -------------

csvfile= open('explore_analysis.csv', 'wb')

w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
header = ['model',
			'explore',
			'count_queries']

w.writerow(header)



## --------- API Config -------------

f = open('config.yml')
params = yaml.load(f)
f.close()


looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)

lis = {}

## --------- API Calls -------------

## -- Get all models --
models = looker.get_model("")
for model in models:
	model_name = model['name']

	## -- Get single model --
	model_def = looker.get_model(model_name)
	# pp(model_def)

	## -- Get single explore --
	for explore_def in model_def['explores']:
		# print model_name, explore_def['name']
		explore_name = model_name+','+explore_def['name']
		lis[explore_name]=0

body = {
  "model":"i__looker",
  "view":"history",
  "fields":["query.view","query.model","history.query_run_count"],
  "filters":{"history.most_recent_run_at_date":"90 days"},
  # "sorts":["products.count desc 0"],
  "limit":"500",
  "query_timezone":"America/Los_Angeles"
}
		
res = looker.run_inline_query(body)
for exp in res:
	explore_name =  exp['query.model']+','+exp['query.view']
	lis[explore_name]=exp['history.query_run_count']

for i in list(lis.keys()):
	write_fields(i, lis[i])
