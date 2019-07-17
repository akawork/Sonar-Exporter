import requests
import json
from lib.connection.connection_request import *
from lib.metrics import project_metrics as project_metrics
from lib.metrics import quality_profile_metrics as quality_profile_metrics
from lib.metrics import administrator_metrics as administrator_metrics


# SONAR = 'http://172.27.100.218:9000'
SONAR = 'https://sonar.fsoft.com.vn'

class TestCollector(object):
    def __init__(self, server, user, passwd, insecure):
        self._server = server
        self._user = user
        self._passwd = passwd
        self._insecure = insecure

    

if __name__ == '__main__':
    collector = TestCollector(SONAR, 'devopssupport', '501project@@', True)
    req = HttpRequests(collector)
    
    
    # list_tasks, task_info, task_status = administrator_metrics.get_list_tasks(req, collector)
    
    # # for status in administrator_metrics.TASK_STATUS_LIST:
    # #     print("{}    {}".format(status,task_status[status]['total']))
        
    list_status_label = administrator_metrics.TASK_STATUS_LIST
    # print(len(list_tasks))
    # count = 0
    # for task in list_tasks:
    #     tid = task['id']
    #     detail = task_info[tid]
    #     print('{}:  {}'.format(detail['componentName'],detail['status']))
    #     count +=1

    # print(count)
    # print('-----------------')
    metrics = administrator_metrics.make_metrics(collector)
    # print(task_status)
    # for status in administrator_metrics.TASK_STATUS_LIST:
    #     x = task_status[status]
    #     value = x['total']
    #     print("{}    {}".format(status,value))
        
    print('OK')
    