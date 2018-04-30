#import yaml
#import LookerApi as looker
import sys
#import time

for p in sys.path: print(p)
#
# f = open('config.yml')
# params = yaml.load(f)
# f.close()
#
# #params to configured
# host = 'localhost'
#
# my_host = params['hosts'][host]['host']
# my_secret = params['hosts'][host]['secret']
# my_token = params['hosts'][host]['token']
#
# unauthenticated_client = looker.ApiClient(my_host)
# unauthenticated_authApi = looker.ApiAuthApi(unauthenticated_client)
# token = unauthenticated_authApi.login(client_id=my_secret, client_secret=my_token)
# client = looker.ApiClient(my_host, 'Authorization', 'token ' + token.access_token)
# userApi = looker.UserApi(client)
#
# renderTask = looker.RenderTaskApi(api_client=client)
# height = 842
# width = 595
# output_format  = 'pdf'
# dashboard_id = 7
# body = {
#          "dashboard_style": "tiled"
#        }
#
# # fire a render task and get its ID
# task_response = renderTask.create_dashboard_render_task(dashboard_id, output_format, body, width, height)
# task_id = task_response.id
#
# #results = renderTask.render_task_results(task_id) #, _preload_content = False)
# #data = results.data
#
# for i in range(0,100,10):
#     response = renderTask.render_task(task_id)
#     print(response.status)
#     time.delay(100)
