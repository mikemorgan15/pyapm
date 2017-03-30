#!/usr/bin/python

import requests
import urlparse
import urllib
import json
import datetime
import logging

from base import ApmBaseService
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

class Organization(ApmBaseService):

    def __init__(self, config):
        self.API_PATH = '/pvc-data/v2'
        self.API_PORT = 443
        self.API_HEADERS = {'Content-Type': 'application/json'}
        self.username = config.username
        self.password = config.password
        self.server = config.server
        self.org_id = config.org_id

    def list_organizations(self):
    	response = self._get(url=self._url(path='organization'))
        if self._verify(response):
            return response.json()
        else:
            log.error('Failed to list organizations: {} - {}'.format(response.json().get('httpStatusCode'), response.json().get('messages')[0]))
            return None