from datetime import timedelta, datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from pprint import pprint
import yaml
import json

def put_device_in_maintenance(dev):
 requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 authuser = 'admin'
 authpwd = 'Embe1mpls'
 headers = { 'content-type' : 'application/json'}
 url = 'https://10.49.124.229:8443/oauth2/token'
 data_to_get_token = {"grant_type":"password","username":authuser,"password":authpwd}
 r = requests.post(url, data=json.dumps(data_to_get_token), auth=(authuser, authpwd), headers=headers, verify=False)
 headers = {'Authorization':str('Bearer ' + r.json()['access_token']), 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
 url_base = 'http://10.49.124.229:8091/NorthStar/API/v2/tenant/'
 url = url_base + '1/topology/1/nodes'
 r = requests.get(url, headers=headers, verify=False)
 for i in r.json():
   if i['hostName'] == dev:
    node_index = i['nodeIndex']
 maintenance_url = url_base + '1/topology/1/maintenances'
 maintenance_data = {
     "topoObjectType": "maintenance",
     "topologyIndex": 1,
     "user": "admin",
     "name": "event1",
     "startTime": datetime.now().isoformat(),
     "endTime": (datetime.now() + timedelta(minutes=60)).isoformat(),
     "elements": [{"topoObjectType": "node", "index": node_index}]
     }
 m_res = requests.post(maintenance_url, data=json.dumps(maintenance_data), headers=headers, verify=False)
 return "done"

