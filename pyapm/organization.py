#!/usr/bin/python

import json
import sys

from base import ApmBaseService, APMException


class Organization(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def list_organizations(self):
        """List all organizations on the specified server that the given user account has access to"""
    	response = self._get(url=self._url(path='organization'))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)
