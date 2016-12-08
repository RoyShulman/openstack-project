from novaclient import client as novaClient
import constants
import os
import time


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

    def get_instance(self, instance_id):
        instance = self.nova_client.servers.find(id=instance_id)
        return instance

    def create_instance(self, image_name, instance_name):
        if not self.nova_client.keypairs.findall(name="mykey"):
            with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
                self.nova_client.keypairs.create(name="mykey", public_key=fpubkey.read())
        image = self.nova_client.images.find(name=image_name)
        flavor = self.nova_client.flavors.find(name="m1.tiny")#because I am using VMs
        instance = self.nova_client.servers.create(name=instance_name, image=image_name,
                                                   flavor=flavor, key_name="mykey")

        status = instance.status
        while status == "BUILD":
            time.sleep(5)
            instance = self.nova_client.servers.get(instance.id)
            status = instance.status
            print "Building"

        print "Finished!"

    def create_security_group(self):
        #default security group
        security_group = self.nova_client.security_groups.find(name="default")
        self.nova_client.security_groups.create(security_group.id, ip_protocol="tcp",
                                                from_port=22, to_port=22)#SSH
        self.nova_client.security_groups.create(security_group.id, ip_protocol="icmp",
                                                from_port=-1, to_port=-1)#ICMP