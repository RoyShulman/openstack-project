from neutronclient.v2_0 import client as neutronClient



class Neutron:
    def __init__(self, keystone_session):
        self.neutron_client = neutronClient.Client(session=keystone_session)

    def list_networks(self):
        """
        List all Networks
        """
        return self.neutron_client.list_networks()

    def create_network(self, network_name, is_external, network_type):
        """
        Create a network
        :param network_name: The name of the network to create
        :param is_external: Boolean for if the network is external
        :param network_type: Which network type to create
        """
        network = {'name': network_name, 'router:external': is_external, 'provider:network_type':network_type}
        self.neutron_client.create_network({'network':network})

    def delete_network(self, network_id):
        """
        Delete a network
        :param network_id: Unique ID of the network to delete
        """
        self.neutron_client.delete_network(network=network_id)