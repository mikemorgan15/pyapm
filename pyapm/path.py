#!/usr/bin/python

import json
import datetime
import time
import sys

from base import ApmBaseService


class Path(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_path_by_id(self, path_id):
        """Get data about a specific path, by path_id"""
        response = self._get(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
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
        	try:
                return response.json()
            except:
                return {}
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
                    parameters['to'] = int(time.mktime(kwargs.get('to_time').timetuple()))
                else:
                    parameters['to'] = kwargs.get('to_time')

            if kwargs.get('from_time'):
                if type(kwargs.get('from_time')) == datetime.datetime:
                    parameters['from'] = int(time.mktime(kwargs.get('from_time').timetuple()))
                else:
                    parameters['from'] = kwargs.get('from_time')

            if kwargs.get('metric'):
                parameters['metric'] = ','.join(str(x) for x in kwargs.get('metric'))

        response = self._get(url=self._url(path='path/{}/data'.format(path_id), query=parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_status(self, path_id):
        """Get the status of a specific path, by path_id"""
        response = self._get(url=self._url(path='path/{}/status'.format(path_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_route(self, path_id, protocol='icmp'):
        """Get the route of a specific path, by path_id.
        Pass the protocol parameter ('icmp'/'udp'/'tcp'), or will default to ICMP
        """
        response = self._get(url=self._url(path='path/{}/traceRoute/{}'.format(path_id, protocol)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
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
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def update_path(self, path_id, **kwargs):
        """Update configuration of an existing path.
        Only the reconfigured parameters need to be passed to this method
        """
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        response = self._patch(url=self._url(path='path/{}'.format(path_id)), data=json.dumps(parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def replace_path(self, path_id, **kwargs):
        """Replaces an existing path, by path_id.
        Effectively creates a new path over an existing path ID, so all required path parameters need to be passed.
        Historic data for path prior to replacement is retained.
        """
        parameters = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                parameters[key] = value
        parameters['orgId'] = self.config.org_id
        response = self._put(url=self._url(path='path/{}'.format(path_id)), data=json.dumps(parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
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