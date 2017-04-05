#!/usr/bin/python

import json
import sys

from base import ApmBaseService


class SavedList(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_saved_lists(self):
        """Returns a list of all alert profiles in the configured org"""
        response = self._get(url=self._url(path='savedList', query={'orgId': self.config.org_id}))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)