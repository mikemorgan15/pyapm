#!/usr/bin/python

import json
import sys

from base import ApmBaseService


class AlertProfile(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_alert_profiles(self):
        """Returns a list of all alert profiles in the configured org"""
        response = self._get(url=self._url(path='alertProfile', query={'orgId': self.config.org_id}))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_alert_profile_by_id(self, alert_profile_id):
        """Returns a specific alert profile by alert_profile_id

        Parameters:
        alert_profile_id (required)
        """
        response = self._get(url=self._url(path='alertProfile/{}'.format(alert_profile_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)