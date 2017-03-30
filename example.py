#!/usr/bin/python

from pyapm.base import ApmBaseService, ApmConfig
from pyapm.appliance import Appliance
from pyapm.path import Path

if __name__ == '__main__':

    # create a configuration
    #
    # you can specify an org_id here or, if you do not know your org id, then you 
    # can omit one and use the Organisation().list_organizations() method to show
    # all orgs your user has permissions to access.
    config = ApmConfig(
        email_address = 'apm_user@example.com',
        password='my_password',
        server='my_server.pathviewcloud.com')
    
    # list all orgs on this server that the user has access to.
    print Organization(config).list_organizations()

    # now I know the org id, i set it on my config object
    config.org_id = '1234'

    # validate that the config allows connectivity to the desired organisation
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
