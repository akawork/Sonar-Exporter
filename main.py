import os
import sys
import time
import configparser

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from sonar.sonar import SonarCollector

if __name__ == "__main__":
    # Import configuration file
    config = configparser.ConfigParser()
    config.read("config.ini")
    sonar_collector = SonarCollector(
        server=config['DEFAULT']['SONAR_SERVER'],
        user=config['DEFAULT']['SONAR_USERNAME'],
        passwd=config['DEFAULT']['SONAR_PASSWORD']
    )

    REGISTRY.register(sonar_collector)
    start_http_server(9119)
    print('OK')

    while True:
        time.sleep(1)
