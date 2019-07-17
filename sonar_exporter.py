import requests
import argparse
import time
import ast
import os
import sys

from requests.auth import HTTPBasicAuth
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

sys.path.append(os.path.abspath('.'))

import lib.metrics.project_metrics as project_metrics 
import lib.metrics.administrator_metrics as administrator_metrics 
import lib.metrics.quality_profile_metrics as quality_profile_metrics 

from etc.parse_args import parse_args

class SonarCollector(object):

    def __init__(self, server, user, passwd, insecure):
        self._server = server
        self._user = user
        self._passwd = passwd
        self._insecure = insecure


#########################################################################################################################################
#-------------------------------------------Function collet start------------------------------------------------------------------------

    def collect(self):
        list_metrics = []
        
        list_metrics += project_metrics.make_metrics(self)
        list_metrics += quality_profile_metrics.make_metrics(self)
        list_metrics += administrator_metrics.make_metrics(self)

        for metric in list_metrics:
            yield metric

        

#-------------------------------------------Function collet end--------------------------------------------------------------------------
#########################################################################################################################################

if __name__ == "__main__":
    args = parse_args()
    port_number = int(args.port)
    print('Start run Sonar exporter at server: {}'.format(args.server))
    REGISTRY.register(SonarCollector(args.server, args.user, args.passwd, args.insecure))
    start_http_server(port_number)
    while True: 
        time.sleep(1)