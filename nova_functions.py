from novaclient import client as novaClient


class Nova:
    def __init__(self, keystone_session):
        self.nova_client = novaClient.Client(version="2", session=keystone_session)

    def list_instances(self):
        try:
            return self.nova_client.servers.list()
        except Exception,e:
            print e

    def delete_instance(self, instance_name):
        instance = self.nova_client.servers.find(name=instance_name)
        instance.delete()