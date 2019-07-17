import argparse
import ast
import os
import sys
import configparser

#from config.parser_config import *

config = configparser.ConfigParser()
config.read(os.environ.get('SONAR_CONFIG_FILE'))

def parse_args():
    
    parser = argparse.ArgumentParser(
        description='sonar exporter'
    )
    parser.add_argument(
        '-s', '--server',
        metavar='server',
        required=False,
        help='server url from the SONAR api',
        default=config['DEFAULT']['SONAR_SERVER']
    )
    parser.add_argument(
        '--user',
        metavar='user',
        required=False,
        help='sonar api user',
        default=config['DEFAULT']['SONAR_USERNAME']
    )
    parser.add_argument(
        '--passwd',
        metavar='passwd',
        required=False,
        help='sonar api password',
        default=config['DEFAULT']['SONAR_PASWORD']
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(config['DEFAULT']['SONAR_VIRTUAL_PORT'])
    )
    parser.add_argument(
        '-k', '--insecure',
        dest='insecure',
        required=False,
        action='store_true',
        help='Allow connection to insecure SONAR API',
        default=False
    )
    return parser.parse_args()