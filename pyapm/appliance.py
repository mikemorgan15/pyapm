#!/usr/bin/python

import json
import sys

from base import ApmBaseService, APMException


class Appliance(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def list_appliances(self):
        """Returns data on all appliances within the specified organization"""
        response = self._get(url=self._url(path='appliance', query={'orgId':self.config.org_id}))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_appliance(self, appliance_id=None):
        """Gets data about a specific appliance, by appliance_id"""
        if appliance_id:
            response = self._get(url=self._url(path='appliance/{}'.format(appliance_id)))
            if self._verify(response):
                return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)
