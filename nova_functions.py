from novaclient import client as novaClient
from neutron_functions import  Neutron
import constants
import os
import time
import easygui



class Nova:
    def __init__(self, keystone_session):
        self.nova_client = novaClient.Client(version="2", session=keystone_session, auth_url=constants.ADMIN_AUTH_URL)
        self.neutron_client = Neutron(keystone_session=keystone_session)

    def list_servers(self):
        try:
            return self.nova_client.servers.list()
        except Exception,e:
            print e

    def delete_instance(self, instance_name):
        instance = self.nova_client.servers.find(name=instance_name)
        instance.delete()

    def get_instance(self, instance_id):
        instance = self.nova_client.servers.find(id=instance_id)
        return instance

    def create_instance(self, image_name, instance_name, security_group_name):
        if not self.nova_client.keypairs.findall(name="mykey"):
            with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
                self.nova_client.keypairs.create(name="mykey", public_key=fpubkey.read())
        image = self.nova_client.images.find(name=image_name)
        flavor = self.nova_client.flavors.find(name="m1.tiny")#because I am using VMs
        security_group_id = self.get_security_group(security_group_name)
        instance = self.nova_client.servers.create(name=instance_name, image=image_name,
                                                   flavor=flavor, key_name="mykey", security_group=security_group_id)

        status = instance.status
        while status == "BUILD":
            time.sleep(5)
            instance = self.nova_client.servers.get(instance.id)
            status = instance.status
            print "Building"

        floating_ip = self.create_floating_ip()

        instance.add_floating_ip(floating_ip)
        print "Finished!"

    def create_security_group(self):
        #default security group
        security_group = self.nova_client.security_groups.find(name="default")
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="tcp",
                                                from_port=22, to_port=22)#SSH
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="icmp",
                                                from_port=-1, to_port=-1)#ICMP
        return security_group

    def get_security_group(self, security_group_name):
        return self.nova_client.security_groups.find(name=security_group_name)

    def list_security_groups(self):
        try:
            return self.nova_client.security_groups.list()
        except Exception, e:
            easygui.msgbox("FAILED\n" + str(e))
            return

    def get_instance(self, instance_name):
        instance_id = [x.id for x in self.list_servers() if x.name == instance_name]
        if instance_id == []:
            easygui.msgbox("Instance name could not be found")
            exit(1)
        else:
            return instance_id[0]

    def create_floating_ip(self):
        return self.neutron_client.list_networks()["networks"]
        #return type(self.nova_client.floating_ips.list())

    def get_novnc_url(self, instance_name):
        instance_id = self.get_instance(instance_name=instance_name)
        return self.nova_client.servers.get_vnc_console(instance_id, 'novnc')["console"]["url"]