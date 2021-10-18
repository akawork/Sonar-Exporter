import os
import sys
import time
import configparser

from prometheus_client.core import REGISTRY
from sonar.sonar import SonarCollector
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

# Import configuration file
config = configparser.ConfigParser()
config.read("config.ini")
sonar_collector = SonarCollector(
    server=config['DEFAULT']['SONAR_SERVER'],
    user=config['DEFAULT']['SONAR_USERNAME'],
    passwd=config['DEFAULT']['SONAR_PASSWORD']
)
REGISTRY.register(sonar_collector)

# Create Flask app
app = Flask(__name__)
@app.route('/ready')
def ready():
    return 'To infinity and beyond!'

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})