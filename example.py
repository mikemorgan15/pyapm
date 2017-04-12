#!/usr/bin/python

import datetime
from pyapm import ApmConfig, AlertProfile, Appliance, Diagnostic, Flow, Organization, Path, SavedList, WebApplication

if __name__ == '__main__':

    # create a configuration
    config = ApmConfig(
        email_address = 'user@example.com',
        password='correct horse battery staple',
        server='pvc-esp-1.pathviewcloud.com')
    

    ########## Organization methods ##########

    # initialize Organization class
    organization = Organization(config)
    
    # list all orgs on this server that the user has access to.
    print organization.list_organizations()

    # now I know the org id, i set it on my config object
    config.org_id = '4321'


    ########## Appliance methods ##########

    # initialize Appliance class
    appliance = Appliance(config)

    # list appliances within the org specified in the config
    print appliance.list_appliances()

    # retrieve info for a specific appliance, by appliance_id
    print appliance.get_appliance(appliance_id='1234')


    ########## Path methods ##########

    # initialize Path class
    path = Path(config)

    # retrieve a path by ID
    print path.get_path_by_id('12345')

    # retrieve a path's status by ID
    print path.get_path_status(path_id='12345')

    # retrieve a path's route by ID
    # pass the 'protocol' parameter to choose a specific protocol (icmp/udp/tcp) otherwise will default to ICMP
    print path.get_path_route(path_id='12345', protocol='icmp')

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

    # update an existing path's configuration.
    # only the new/updated parameters need to be passed to this method.
    print path.update_path(
        path_id='12345', 
        sourceAppliance='my-other-m25', 
        description='this is the updated description')

    # replaces an existing path by ID.
    # all required path config parameters need to be passed.
    # historic monitoring data for the replaced path is retained.
    print path.replace_path(
        path_id='12345',
        sourceAppliance='my-other-m25',
        target='apm.appneta.com',
        groupName='A new group',
        pathName='my-other-m25 -> apm.appneta.com (single)',
        networkType='WAN')


    ########## Diagnostic methods ##########

    # initialize Diagnostic class
    diagnostic = Diagnostic(config)

    # create some datetime objects to specify a time range...
    to_time = datetime.datetime.now()
    from_time = datetime.datetime.now() - datetime.timedelta(hours = 1)

    # ...then pass datetime objects to get_diagnostics method, to return diagnostics in that time range.
    # accepts additional parameters to filter results.
    print diagnostic.get_diagnostics(applianceName='mikes-m35', to_time=to_time, from_time=from_time)

    # retrieve a single diagnostic test, by test_id.
    print diagnostic.get_diagnostic(test_id='1234567')

    # retrieve detail from a diagnostic test, by test_id.
    print diagnostic.get_diagnostic_detail(test_id='1234567')


    ########## Alert Profile methods ##########

    # initialize Alert Profile class
    alert_profile = AlertProfile(config)

    # retrieve a list of all alert profiles from the org specified in your config
    print alert_profile.get_alert_profiles()

    # retrieve a specific alert profile, by alert_profile_id
    print alert_profile.get_alert_profile_by_id(alert_profile_id='7451')


    ########## Saved List methods ##########

    # initialize Saved List class
    saved_list = SavedList(config)

    # retrieve a list of all saved lists from the org specified in your config
    print saved_list.get_saved_lists()


    ########## Flow methods ##########

    # initialize Flow class
    flow = Flow(config)

    # retreive a list of FlowView configured appliances
    print flow.get_appliances()

    # create some datetime objects to specify a time range...
    to_time = datetime.datetime.now()
    from_time = datetime.datetime.now() - datetime.timedelta(hours = 1)

    # ...pass the datetime objects to the get_top_applications method, to return the top applications within that time range...
    print flow.get_top_applications(appliance_id='14712', interface='eth5', to_time=to_time, from_time=from_time, n='20')

    #...or to the get_top_conversations to retrieve top conversations.
    print flow.get_top_conversations(appliance_id='14712', interface='eth5', to_time=to_time, from_time=from_time, n='20')

    # retrieve a list of applications (both stock and custom)
    print flow.get_applications()


    ########## Web Application methods ##########

    # initialize the WebApplication class
    webapp = WebApplication(config)

    # retrieve a list of available web apps in the configured org
    print webapp.get_web_apps()

    # retrieve a specific web app by web_app_id
    print webapp.get_web_app(web_app_id='5678')

    # delete a web app, by web_app_id
    print webapp.delete_web_app(web_app_id='5678')

    # retrieve a list of web monitors in a chosen web app, by web_app_id
    print webapp.get_web_monitors(web_app_id='5678')

    # retrieve a specific web monitor from a web app, by web_app_id and web_monitor_id
    print webapp.get_web_monitors(web_app_id='5678', web_monitor_id='65432')

    # create some datetime objects to specify a time range, and create a list of desired metrics...
    to_time = datetime.datetime.now()
    from_time = datetime.datetime.now() - datetime.timedelta(hours = 1)
    metric = ['servertiming', 'browsertiming']
    
    # ...then pass these to the get_web_monitor_data to retrieve monitoring data from a specific web monitor over a given time range.
    print webapp.get_web_monitor_data(web_app_id='5678', web_monitor_id='76543', to_time=to_time, from_time=from_time, metric=metric)
    
