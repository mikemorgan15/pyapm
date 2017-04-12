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
        """Get data about a specific path, by path_id
        
        Parameters:
        path_id (required)
        """
        response = self._get(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return {}
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_paths(self, **kwargs):
        """Get data a number of paths, filtered by one or more parameters
        
        Parameters:
        name - the descriptive name for the path (allows wildcards) (optional)
        description - a short description of the path (allows wildcards) (optional)
        instrumentation - shows whether the path is dual or single-ended (optional)
        qosName - the name of the quality of service settings associated with the path (allows wildcards) (optional)
        group - the name of the group (allows wildcards) (optional)
        importance - the importance level of the path (optional)
        sourceAppliance - the name of the source appliance (allows wildcards) (optional)
        sourceNetwork - the address of the source appliance (allows wildcards) (optional)
        target - the ip or hostname of the target (allows wildcards) (optional)
        networkType - the network type associated with the path (optional)
        page - the page of results to return (optional)
        limit - the number of results per page (optional)
        savedListId - the id of the savedlist (optional)
        """
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
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_data(self, path_id, **kwargs):
        '''Get monitoring data for a specified path, by path_id.
                
        Parameters:
        path_id (required)
        to_time - the end of the required time range. Can be unix timestamp or datetime object (optional) 
        from_time - the start of the required time range. Can be unix timestamp or datetime object (optional)
        metric - a list of the required metrics. (optional). Available options are:
            totalcapacity, 
            utilizedcapacity, 
            availablecapacity,
            latency,
            datajitter,
            dataloss,
            voicejitter,
            voiceloss,
            mos,
            rtt,
            twamprtt,
            twampjitter,
            twamploss
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
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_status(self, path_id):
        """Get the status of a specific path, by path_id
        
        Parameters:
        path_id (required)
        """
        response = self._get(url=self._url(path='path/{}/status'.format(path_id)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def get_path_route(self, path_id, protocol='icmp'):
        """Get the route of a specific path, by path_id.
        
        Parameters:
        path_id (required)
        protocol - icmp/udp/tcp (required)
        """
        response = self._get(url=self._url(path='path/{}/traceRoute/{}'.format(path_id, protocol)))
        if self._verify(response):
            try:
                return response.json()
            except:
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def create_path(self, **kwargs):
        """Create a path using the given parameters
        
        Parameters:
        sourceAppliance,
        target,
        id (optional),
        applianceInterface (optional),
        groupName (optional),
        importance (optional),
        alertProfileId (optional),
        asymmetric (optional),
        pathName (optional),
        description (optional),
        inboundName (optional),
        outboundName (optional),
        networkType (optional),
        disabled (optional),
        qosName (optional),
        tcpTracertTargetPort (optional),
        udpTracertTargetPort (optional)
        """
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
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def update_path(self, path_id, **kwargs):
        """Update configuration of an existing path.  Only the reconfigured parameters need to be passed to this method

        Parameters:
        path_id (required)
        sourceAppliance (optional),
        target (optional),
        id (optional),
        applianceInterface (optional),
        groupName (optional),
        importance (optional),
        alertProfileId (optional),
        asymmetric (optional),
        pathName (optional),
        description (optional),
        inboundName (optional),
        outboundName (optional),
        networkType (optional),
        disabled (optional),
        qosName (optional),
        tcpTracertTargetPort (optional),
        udpTracertTargetPort (optional)
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
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def replace_path(self, path_id, **kwargs):
        """Replaces an existing path, by path_id.  Effectively creates a new path over an existing path ID, so all required path parameters need to be passed.
        
        Parameters:
        sourceAppliance,
        target,
        id (optional),
        applianceInterface (optional),
        groupName (optional),
        importance (optional),
        alertProfileId (optional),
        asymmetric (optional),
        pathName (optional),
        description (optional),
        inboundName (optional),
        outboundName (optional),
        networkType (optional),
        disabled (optional),
        qosName (optional),
        tcpTracertTargetPort (optional),
        udpTracertTargetPort (optional)
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
                return None
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)

    def delete_path(self, path_id=None):
        """Delete a specific path, by path_id.  Returns 'True' if successful.

        Parameters:
        path_id (required)
        """
        response = self._delete(url=self._url(path='path/{}'.format(path_id)))
        if self._verify(response):
            return True
        else:
            return self._apm_http_error(sys._getframe().f_code.co_name, response)