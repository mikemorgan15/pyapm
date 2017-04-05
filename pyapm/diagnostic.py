#!/usr/bin/python

import json
import datetime
import time
import sys

from base import ApmBaseService


class Diagnostic(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_diagnostics(self, **kwargs):
        '''Get a list of diagostic tests matching the specified parameters.
        'to_time' and 'from_time' parameters can be passed for filtering within a particular time range.
        
        - 'to_time' and 'from_time' can either be unix timestamps, or datetime objects.
        '''
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if key == 'to_time':
                    if type(kwargs.get('to_time')) == datetime.datetime:
                        parameters['to'] = int(time.mktime(kwargs.get('to_time').timetuple()))
                    else:
                        parameters['to'] = kwargs.get('to_time')

                elif key == 'from_time':
                    if type(kwargs.get('from_time')) == datetime.datetime:
                        parameters['from'] = int(time.mktime(kwargs.get('from_time').timetuple()))
                    else:
                        parameters['from'] = kwargs.get('from_time')
                
                else:
                    parameters[key] = value

        parameters['orgId'] = self.config.org_id
        response = self._get(url=self._url(path='diagnostic', query=parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_diagnostic(self, test_id):
        """Get a specific diagnostic, by test_id"""
        response = self._get(url=self._url(path='diagnostic/{}'.format(test_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_diagnostic_detail(self, test_id):
        """Get a specific diagnostic, by test_id"""
        response = self._get(url=self._url(path='diagnostic/{}/detail'.format(test_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)