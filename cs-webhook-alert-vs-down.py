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
values = {"attachments":[{"color":"#FF0000","text":"此事件代表“虚拟服务“异常停止无法正常对外提供服务，请相关管理员进行排查。","title":event_description,"fields":[{"short":"false","title":"对象名称","value":obj_name},{"short":"false","title":"事件ID","value":event_id},{"short":"false","title":"10分钟内发生次数","value":threshold}]}]}
values = json.dumps(values)
print(values)
response = requests.post(webhook_url, data=values,headers={'Content-Type': 'application/json'})
if response.status_code != 200:
    raise ValueError('Request returned an error %s, the response is:\n%s'% (response.status_code, response.text))
