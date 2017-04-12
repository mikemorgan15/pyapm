#!/usr/bin/python

import json
import datetime
import time
import sys

from base import ApmBaseService


class Flow(ApmBaseService):

    def __init__(self, config):
        self.config = config

    def get_appliances(self):
        """Returns a list of appliances with configured capture interfaces in the configured org"""
        response = self._get(url=self._url(path='flow', query={'orgId': self.config.org_id}))
        if self._verify(response):
            return response.json()
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_top_applications(self, appliance_id, interface, **kwargs):
        '''Returns a list of the top applications for the given period.
        
        Parameters:
        appliance_id (required)
        interface (required)
        orderBy - metric by which the top N applications are ordered by. Optional. Default is bytes (optional)
        n - number of applications to return (max 100). Optional. Default is 10. (optional)
        from_time - start of desired time window, can be unix timestamp or datetime object (optional)
        to_time - end of desired time window, can be unix timestamp or datetime object (optional)
        endpoint - endpoint filter criteria as a comma separated list of "[src|dst] {IP|hostname|IP subnet|IP wildcard}". (optional)
        endpointMatch - endpoint filter match type: ANY, ALL and NOT. Optional. Default is ANY. (optional)
        application - application filter criteria as a comma separated list of application IDs. (optional)
        category - application filter criteria as a comma separated list of categories. (optional)
        classification - application filter criteria as a comma separated list of classfications. (optional)
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

        response = self._get(url=self._url(path='flow/appliance/{}/interface/{}/topn/application'.format(appliance_id, interface), query=parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_top_conversations(self, appliance_id, interface, **kwargs):
        '''Returns a list of the top conversations for the given period.
        
        Parameters:
        appliance_id (required)
        interface (required)
        orderBy - metric by which the top N applications are ordered by. Optional. Default is bytes (optional)
        n - number of applications to return (max 100). Optional. Default is 10. (optional)
        from_time - start of desired time window, can be unix timestamp or datetime object (optional)
        to_time - end of desired time window, can be unix timestamp or datetime object (optional)
        endpoint - endpoint filter criteria as a comma separated list of "[src|dst] {IP|hostname|IP subnet|IP wildcard}". (optional)
        endpointMatch - endpoint filter match type: ANY, ALL and NOT. Optional. Default is ANY. (optional)
        application - application filter criteria as a comma separated list of application IDs. (optional)
        category - application filter criteria as a comma separated list of categories. (optional)
        classification - application filter criteria as a comma separated list of classfications. (optional)
        hostnames - enable reverse DNS hostname resolution. Valid values are: private and public. (optional)
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

        response = self._get(url=self._url(path='flow/appliance/{}/interface/{}/topn/conversation'.format(appliance_id, interface), query=parameters))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_applications(self):
        """Returns a list of applications and associated metadata in the configured org"""
        response = self._get(url=self._url(path='flow/application', query={'orgId': self.config.org_id}))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)