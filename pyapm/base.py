#!/usr/bin/python

import requests
import urlparse
import urllib
import json
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)


class ApmBaseService(object):

    API_PATH = '/pvc-data/v2'
    API_PORT = 443
    API_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    def __init__(self):
        self = self

    def _verify(self, response):
        if response is not None:
            if type(response) == requests.models.Response:
                if response.ok:
                    return True

    def _auth(self):
        return (self.config.username, self.config.password)

    def _get(self, url=None, data=None):
        try:
            result = requests.get(url, auth=self._auth(), headers=self.API_HEADERS, verify=False, data=data)
        except Exception as e:
            if self.config.log_level == 'debug':            
                log.error('\'GET\' - Connection failed to {} - {}'.format(url, e))
            return e
        return result

    def _post(self, url=None, data=None):
        try:
            result = requests.post(url, auth=self._auth(), headers=self.API_HEADERS, verify=False, data=data)
        except Exception as e:
            if self.config.log_level == 'debug':
                log.error('\'POST\' - Connection failed to {} - {}'.format(url, e))
            return e
        return result

    def _put(self, url=None, data=None):
        try:
            result = requests.put(url, auth=self._auth(), headers=self.API_HEADERS, verify=False, data=data)
        except Exception as e:
            if self.config.log_level == 'debug':
                log.error('\'PUT\' - Connection failed to {} - {}'.format(url, e))
            return e
        return result

    def _delete(self, url=None):
        try:
            result = requests.delete(url, auth=self._auth(), headers=self.API_HEADERS, verify=False)
        except Exception as e:
            if self.config.log_level == 'debug':
                log.error('\'DELETE\' - Connection failed to {} - {}'.format(url, e))
            return e
        return result

    def _url(self, path, query=None):
        if query is None:
            query = {}
        query_string = urllib.urlencode(query)
        url = urlparse.ParseResult(
            scheme = 'https',
            netloc = '{}:{}'.format(self.config.server, self.API_PORT),
            path = '{}/{}/'.format(self.API_PATH, path),
            params = None,
            query = urllib.urlencode(query),
            fragment = None)
        return url.geturl()

    def _apm_http_error(self, api_method, response):
        if type(response) == requests.models.Response:
            if response.json().get('messages')[0]:
                message = response.json().get('messages')[0]
            else:
                message = 'Unexpected failure'
            raise APMException('{} - {}: {}'.format(api_method, response.status_code, message))
        else:
            raise APMException('{}'.format(response))

    def _get_method(method):
        return method(name=method.__name__)


class ApmConfig(object):

    def __init__(self, email_address, password, server, org_id=None, log_level=None):
        self.username = email_address
        self.password = password
        self.server = server
        self.org_id = org_id
        self.log_level = log_level

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

class APMException(Exception):
    pass

