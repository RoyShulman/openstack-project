from novaclient import client as novaClient
import constants
import os
import time
import easygui


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

    def create_instance(self, image_name, instance_name, security_group_id):
        if not self.nova_client.keypairs.findall(name="mykey"):
            with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
                self.nova_client.keypairs.create(name="mykey", public_key=fpubkey.read())
        image = self.nova_client.images.find(name=image_name)
        flavor = self.nova_client.flavors.find(name="m1.tiny")#because I am using VMs
        instance = self.nova_client.servers.create(name=instance_name, image=image_name,
                                                   flavor=flavor, key_name="mykey", security_group=security_group_id)

        status = instance.status
        while status == "BUILD":
            time.sleep(5)
            instance = self.nova_client.servers.get(instance.id)
            status = instance.status
            print "Building"

        instance.add_floating_ip()#TODO: add function to add a floating ip
        print "Finished!"

    def create_security_group(self):
        #default security group
        security_group = self.nova_client.security_groups.find(name="default")
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="tcp",
                                                from_port=22, to_port=22)#SSH
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="icmp",
                                                from_port=-1, to_port=-1)#ICMP
        return security_group

    def get_instance(self, instance_name):
        instance_id= [x.id for x in self.list_images() if x.name == instance_name]
        if instance_id == []:
            easygui.msgbox("Instance name could not be found")
            exit(1)
        else:
            return instance_id