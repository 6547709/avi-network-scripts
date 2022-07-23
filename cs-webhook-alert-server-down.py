#!/usr/bin/python3
import os
import json
import sys
import time
import urllib3
import requests
requests.packages.urllib3.disable_warnings()
webhook_url = 'https://mattermost.corp.local/hooks/123456'
event_description = os.environ['EVENT_DESCRIPTION']
alert_dict = json.loads(sys.argv[1])
events = alert_dict.get('events', [])
obj_uuid = events[0]['obj_uuid']
obj_name = alert_dict.get('obj_name')
event_id = events[0]['event_id']
level = alert_dict.get('level')
reason = alert_dict.get('reason')
threshold = alert_dict.get('threshold')
server_ip = events[0]['event_details']['se_hm_pool_details']['server']['ip']['addr']
server_port = events[0]['event_details']['se_hm_pool_details']['server']['port']
failure_code = events[0]['event_details']['se_hm_pool_details']['server']['failure_code']
shm_profile = events[0]['event_details']['se_hm_pool_details']['server']['shm'][0]['health_monitor']
pool_name = events[0]['event_details']['se_hm_pool_details']['pool']
virtual_service_name = events[0]['event_details']['se_hm_pool_details']['virtual_service']
percent_servers_up = events[0]['event_details']['se_hm_pool_details']['percent_servers_up']
values = {"attachments":[{"color":"#ffa500","text":"此事件代表“池成员“健康检查失败","title":event_description,"fields":[{"short":"true","title":"对象名称","value":obj_name},{"short":"true","title":"事件ID","value":event_id},{"short":"true","title":"服务器IP地址","value":server_ip},{"short":"true","title":"服务器端口","value":server_port},{"short":"true","title":"主动健康检查配置","value":shm_profile},{"short":"true","title":"失败代码","value":failure_code},{"short":"true","title":"虚拟服务","value":virtual_service_name},{"short":"true","title":"服务器在线率","value":percent_servers_up}]}]}
values = json.dumps(values)
response = requests.post(webhook_url, data=values,headers={'Content-Type': 'application/json'})
if response.status_code != 200:
    raise ValueError('Request returned an error %s, the response is:\n%s'% (response.status_code, response.text))
