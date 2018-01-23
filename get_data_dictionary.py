# -*- coding: UTF-8 -*-
import yaml
from lookerapi import LookerApi
from pprint import pprint as pp
import json
import csv
import requests


# ## LOOKER API CLASS [[ its in the lookerapi we are importing!]]

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

# GET /lookml_models/
    def get_models(self,fields={}):
        url = '{}{}'.format(self.host,'lookml_models')
        # print url
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


## --------- csv writing -------

def write_fields(explore, fields):

	### First, compile the fields you need for your row

	explore_fields=explore['fields']
	try:
		connection_name = str(explore['connection_name'])
	except:
		connection_name = ''
	for dimension in explore_fields[fields]:
		# print dimension

		field_type = fields
		project = str(dimension['project_name'])
		explore = str(explore_def['name'])
		view=str(dimension['view'])
		view_label=str(dimension['view_label'])
		name=str(dimension['name'])
		hidden=str(dimension['hidden'])
		label=str(dimension['label'])
		label_short=str(dimension['label_short'])
		description=str(dimension['description'])
		sql=str(dimension['sql'])
		ftype=str(dimension['type'])
		value_format=str(dimension['value_format'])
		source = str(dimension['source_file'])

	### compile the line - this is possible to combine above, but here to keep things simple
		rowout = []
		rowout.append(connection_name)
		rowout.append(field_type)
		rowout.append(project)
		rowout.append(explore)
		rowout.append(view)
		rowout.append(view_label)
		rowout.append(name)
		rowout.append(hidden)
		rowout.append(label)
		rowout.append(label_short)
		rowout.append(description)
		rowout.append(sql)
		rowout.append(ftype)
		rowout.append(value_format)
		rowout.append(source)

		w.writerow(rowout)

## --------- csv formatting -------------

csvfile= open('dictionary.csv', 'wb')

w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
header = ['connection_name',
			'field_type',
			'project',
			'explore',
			'view',
			'view_label',
			'name',
			'hidden',
			'label',
			'label_short',
			'description',
			'sql',
			'ftype',
			'value_format',
			'source']

w.writerow(header)



## --------- API Config -------------

f = open('config.yml')
params = yaml.load(f)
f.close()

hostname = 'localhost'

my_host = params['hosts'][hostname]['host']
my_secret = params['hosts'][hostname]['secret']
my_token = params['hosts'][hostname]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)



## --------- API Calls -------------

## -- Get all models --
models = looker.get_model("")
pp(models)
for model in models:
	model_name = model['name']

	## -- Get single model --
	model_def = looker.get_model(model_name)
	# pp(model_def)

	## -- Get single explore --
	for explore_def in model_def['explores']:
		explore=looker.get_explore(model_name, explore_def['name'])
		# pp(explore)
		## -- parse explore --
		
		try:
			write_fields(explore,'measures')
		except:
			print 'Problem measure fields in ', explore_def['name']
		try:
			write_fields(explore,'dimensions')
		except:
			print 'Problem dimension fields in ', explore_def['name']

