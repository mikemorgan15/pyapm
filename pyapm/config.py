#!/usr/bin/python

class ApmConfig(object):

    def __init__(self, email_address, password, server, org_id):
        self.username = email_address
        self.password = password
        self.server = server
        self.org_id = org_id

