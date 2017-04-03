#!/usr/bin/python

import datetime

from pyapm import ApmConfig, Appliance, Path, Organization


if __name__ == '__main__':

    # create a configuration
    config = ApmConfig(
        email_address = 'user@example.com',
        password='correct horse battery stable',
        server='pvc-esp-1.pathviewcloud.com')
    
    # initialize Organization class
    organization = Organization(config)
    
    # list all orgs on this server that the user has access to.
    print organization.list_organizations()

    # now I know the org id, i set it on my config object
    config.org_id = '4321'


    # initialize Appliance class
    appliance = Appliance(config)

    # list appliances within the org specified in the config
    print appliance.list_appliances()

    # retrieve info for a specific appliance
    print appliance.get_appliance(appliance_id='1234')


    # initialize Path class
    path = Path(config)

    # retrieve a path by ID
    print path.get_path_by_id('12345')

    # retrieve a list of paths using the given filters
    print path.get_paths(sourceAppliance='mike-m35', target='8.8.8.8')

    # retrieve path monitoring data.  in this case, we're passing two datetime objects
    # to the method to specify the time range required (unix time stamps are also ok).
    # to only retrieve some metrics, pass a list specifying which ones you want.
    to_time = datetime.datetime.now()
    from_time = datetime.datetime.now() - datetime.timedelta(hours = 1)
    metric = ['datajitter', 'dataloss']
    print path.get_path_data(path_id='12345', to_time=to_time, from_time=from_time, metric=metric)

    # delete a path by ID (will return True if successful)
    print path.delete_path(path_id='12345')

    # use the get_paths and delete_path methods together to mass delete
    for p in path.get_paths(sourceAppliance='mikes-m35', importance='1'):
        delete = path.delete(path_id=p['id'])
        if delete:
            print 'Path \'{}\' deleted'.format(p['pathName'])

    # create a path using the given parameters
    print path.create_path(
        sourceAppliance='mike-m35',
        target='8.8.8.8',
        groupName='API TESTING',
        importance='10',
        pathName='mike-m35 -> 8.8.8.8 (single)',
        description='A description of my path',
        networkType='WAN')
