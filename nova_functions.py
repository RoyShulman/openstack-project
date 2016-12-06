from novaclient import client as novaClient
import constants


class Nova:
    def __init__(self, keystone_session):
        self.nova_client = novaClient.Client(version="2", session=keystone_session, auth_url=constants.ADMIN_AUTH_URL)

    def list_images(self):
        try:
            return self.nova_client.images.list()
        except Exception,e:
            print e

    def delete_instance(self, instance_name):
        instance = self.nova_client.servers.find(name=instance_name)
        instance.delete()