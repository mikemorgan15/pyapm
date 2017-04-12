#!/usr/bin/python

import json
import datetime
import time
import sys

from base import ApmBaseService


class WebApplication(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_web_apps(self):
        """Retrieve a list of web applications being montiored within the configured org"""
        response = self._get(url=self._url(path='webApplication', query={'orgId': self.config.org_id}))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_web_app(self, web_app_id):
        """Retrieve a specific web application, by web_app_id

        Parameters:
        web_app_id (required)
        """
        response = self._get(url=self._url(path='webApplication/{}'.format(web_app_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def delete_web_app(self, web_app_id):
        """Delete a specific web application, by web_app_id

        Parameters:
        web_app_id (required)
        """
        response = self._delete(url=self._url(path='webApplication/{}'.format(web_app_id)))
        if self._verify(response):
            try:
                return True
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_web_monitors(self, web_app_id):
        """Retrieve a list of web monitors in a specific web application, by web_app_id

        Parameters:
        web_app_id (required)
        """
        response = self._get(url=self._url(path='webApplication/{}/monitor'.format(web_app_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_web_monitor(self, web_app_id, web_monitor_id):
        """Retrieve a web monitor by it's web_app_id and web_monitor_id

        Parameters:
        web_app_id (required)
        web_monitor_id (required)
        """
        response = self._get(url=self._url(path='webApplication/{}/monitor/{}'.format(web_app_id, web_monitor_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_web_monitor_data(self, web_app_id, web_monitor_id, **kwargs):
        '''Get monitoring data for a web app from a specific web monitor, by web_app_id and web_monitor_id.

        Parameters:
        web_app_id (required)
        web_monitor_id (required)
        to_time - end of required time range. Can be eitehr unix timestamp or datetime object. (optional) 
        from_time - start of required time range. Can be eitehr unix timestamp or datetime object. (optional)
        metric - a list of required metrics.  (optional).  Available options are:
            networktiming,
            servertiming,
            browsertiming,
            apdexscore,
            basepagesize,
            statuscode
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

        response = self._get(url=self._url(path='webApplication/{}/monitor/{}/data'.format(web_app_id, web_monitor_id), query=parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)