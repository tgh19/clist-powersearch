"""Common code used by other files"""

import os
import sys
import json
import yaml

import contextlib 
from urllib.parse import urlencode           
from urllib.request import urlopen 

# Globals
CONFIG_DIR = '/app/config/'
CONFIG_PATH = CONFIG_DIR + 'config.yml'
BLACKLIST_PATH = CONFIG_DIR + 'blacklist.txt'

# Load in config yaml
try:
    with open(CONFIG_PATH) as config_file:
        CONFIG = yaml.load(config_file, yaml.Loader)
except FileNotFoundError:
    print('no config.yml found')
    sys.exit(0)

# Create blacklist file if it doesn't exist
if not os.path.exists(BLACKLIST_PATH):
    open(BLACKLIST_PATH, 'w+')


def get_default(param, config=CONFIG):
    """Get default params from config yaml by name"""
    return config.get('default params').get(param)


def load_blacklist():
    """Loads in blacklisted posts"""
    with open(BLACKLIST_PATH) as bl_file:
        blacklist = []
        for url in bl_file:
            blacklist.append(url[:-1])
        return blacklist


def get_queries():
    """Return queries section of loaded yaml file"""
    return CONFIG.get('queries')


def blacklist_result(url):
    """Adds result to the blacklist"""
    with open(BLACKLIST_PATH, 'a+') as bl_file:
        bl_file.write(f'{url}\n')


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')
