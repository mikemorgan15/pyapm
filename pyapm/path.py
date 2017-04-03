#!/usr/bin/python

import json
import datetime
import time
import sys

from base import ApmBaseService, APMException


class Path(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_path_by_id(self, path_id):
        """Get data about a specific path, by path_id"""
        response = self._get(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_paths(self, **kwargs):
        """Get data a number of paths, filtered by one or more keys"""
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        parameters['orgId'] = self.config.org_id
        response = self._get(url=self._url(path='path', query=parameters))
        if self._verify(response):
        	return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_data(self, path_id, **kwargs):
        '''Get monitoring data for a specified path, by path_id.
        Additional 'to_time', 'from_time' and 'metric' parameters can be passed for filtering purposes.
        
        - 'to_time' and 'from_time' can either be unix timestamps, or datetime objects.
        - 'metric' should be a list of the metrics you wish to retrieve. 
        '''
        parameters = {}
        if kwargs is not None:
            if kwargs.get('to_time'):
                if type(kwargs.get('to_time')) == datetime.datetime:
                    parameters['to_time'] = time.mktime(kwargs.get('to_time').timetuple())
                else:
                    parameters['to_time'] = kwargs.get('to_time')

            if kwargs.get('from_time'):
                if type(kwargs.get('from_time')) == datetime.datetime:
                    parameters['from_time'] = time.mktime(kwargs.get('from_time').timetuple())
                else:
                    parameters['from_time'] = kwargs.get('from_time')

            if kwargs.get('metric'):
                parameters['metric'] = ','.join(str(x) for x in kwargs.get('metric'))

        response = self._get(url=self._url(path='path/{}/data'.format(path_id), query=parameters))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def create_path(self, **kwargs):
        """Create a path using the given parameters"""
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        parameters['orgId'] = self.config.org_id
        response = self._post(url=self._url(path='path'), data=json.dumps(parameters))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def delete_path(self, path_id=None):
        """Delete a specific path, by path_id.
        Returns 'True' if successful.
        """
        response = self._delete(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            return True
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)