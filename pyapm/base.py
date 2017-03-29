#!/usr/bin/python

import requests
import urlparse
import urllib
import json
import datetime
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)


class ApmConfig(object):

    def __init__(self, email_address, password, server, org_id):
        self.username = email_address
        self.password = password
        self.server = server
        self.org_id = org_id


class ApmBaseService(object):

    def __init__(self, config):
        self.API_PATH = '/pvc-data/v2'
        self.API_PORT = 443
        self.API_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.username = config.username
        self.password = config.password
        self.server = config.server
        self.org_id = config.org_id

    def _verify(self, response):
        if response is not None:
            if response.ok:
                return True
        else:
            return False

    def _auth(self):
        return (self.username, self.password)

    def _get(self, url=None, data=None):
        try:
            result = requests.get(url, auth=self._auth(), headers=self.API_HEADERS, verify=False, data=data)
        except Exception as e:
            log.error('GET - Connection failed to {} - {}'.format(url, e))
            return None
        return result

    def _post(self, url=None, data=None):
        try:
            result = requests.post(url, auth=self._auth(), headers=self.API_HEADERS, verify=False, data=data)
        except Exception as e:
            log.error('POST - Connection failed to {} - {}'.format(url, e))
            return None
        return result

    def _url(self, path, query=None):
        if query is None:
            query = {}
        query_string = urllib.urlencode(query)
        url = urlparse.ParseResult(
            scheme = 'https',
            netloc = '{}:{}'.format(self.server, self.API_PORT),
            path = '{}/{}/'.format(self.API_PATH, path),
            params = None,
            query = urllib.urlencode(query),
            fragment = None)
        return url.geturl()

    def validate(self):
        response = self._get(
            url=self._url(path='organization'))
        if self._verify(response):
            ok = None
            for org in response.json():
                if org['id'] == int(self.org_id):
                    ok = True
            if ok:
                return True
            else:
                return None