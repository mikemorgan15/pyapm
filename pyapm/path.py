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

class Path(ApmBaseService):

    def __init__(self, config):
        self.API_PATH = '/pvc-data/v2'
        self.API_PORT = 443
        self.API_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.username = config.username
        self.password = config.password
        self.server = config.server
        self.org_id = config.org_id

    def get_path_by_id(self, path_id=None):
        response = self._get(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            return response.json()
        else:
            log.error('Failed to get path: {} - {}'.format(response.json().get('httpStatusCode'), response.json().get('messages')[0]))
            return None

    def get_paths(self, **kwargs):
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        parameters['orgId'] = self.org_id
        response = self._get(url=self._url(path='path', query=parameters))
        if self._verify(response):
        	return response.json()
        else:
            log.error('Failed to get paths: {} - {}'.format(response.json().get('httpStatusCode'), response.json().get('messages')[0]))
            return None

    def create_path(self, **kwargs):
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        parameters['orgId'] = self.org_id
        response = self._post(url=self._url(path='path'), data=json.dumps(parameters))
        if self._verify(response):
            return response.json()
        else:
            log.error('Failed to create path: {} - {}'.format(response.json().get('httpStatusCode'), response.json().get('messages')[0]))
            return None