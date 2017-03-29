#!/usr/bin/python

from pyapm.base import ApmBaseService, ApmConfig
from pyapm.appliance import Appliance
from pyapm.path import Path

if __name__ == '__main__':

	# create a configuration
    config = ApmConfig(
    	email_address = 'apm_user@example.com',
        password='my_password',
        server='my_server.pathviewcloud.com',
        org_id='1111')
    
    # validate that the config allows connectivity to the API
    if ApmBaseService(config).validate():
        print 'Config ok :)'
    else:
        print 'Config not ok :('

    # list appliances within the org specified in the config
    print Appliance(config).list_appliances()

    # retrieve info for a specific appliance
    print Appliance(config).get_appliance(appliance_id='9521')

    # retrieve a path by ID
    print Path(config).get_path_by_id(path_id='29592')

    # retrieve a list of paths using the given filters
    print Path(config).get_paths(importance='10', networkType='WAN')

   	# create a path using the given parameters
    print Path(config).create_path(
        sourceAppliance='DC1-appliance',
       	target='8.8.8.8',
       	groupName='Critical paths',
       	importance='10',
       	pathName='DC1-Appliance -> 8.8.8.8 (single)',
       	description='DC1 to DNS server',
       	networkType='WAN')
