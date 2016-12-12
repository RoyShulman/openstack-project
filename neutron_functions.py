from neutronclient.v2_0 import client as neutronClient



class Neutron:
    def __init__(self, keystone_session):
        self.neutron_client = neutronClient.Client(session=keystone_session)

    def list_networks(self):
        return self.neutron_client.list_networks()
