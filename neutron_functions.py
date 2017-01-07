from neutronclient.v2_0 import client as neutronClient



class Neutron:
    def __init__(self, keystone_session):
        self.neutron_client = neutronClient.Client(session=keystone_session)

    def list_networks(self):
        return self.neutron_client.list_networks()

    def create_network(self, network_name, is_external, network_type):
        network = {'name': network_name, 'router:external': is_external, 'provider:network_type':network_type}
        self.neutron_client.create_network({'network':network})

    def delete_network(self, network_id):
        self.neutron_client.delete_network(network=network_id)