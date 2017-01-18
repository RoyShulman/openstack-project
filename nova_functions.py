from novaclient import client as novaClient
from neutron_functions import  Neutron
from cinder_functions import Cinder
from novaclient.exceptions import Conflict

import constants
import os
import time
import easygui
import datetime



class Nova:
    def __init__(self, keystone_session):
        self.nova_client = novaClient.Client(version="2", session=keystone_session, auth_url=constants.ADMIN_AUTH_URL)
        self.neutron_client = Neutron(keystone_session=keystone_session)
        self.cinder_client = Cinder(keystone_session=keystone_session)

    def list_servers(self):
        """
        List all instances
        :return: all available instances
        """
        try:
            return self.nova_client.servers.list()
        except Exception,e:
            print e

    def delete_instance(self, instance_name):
        """
        Terminates an instance and deletes it
        :param instance_name: Name of the instance to be deleted
        """
        instance = self.nova_client.servers.find(name=instance_name)
        instance.delete()

    def create_instance(self, image_name, instance_name, security_group_name):
        """
        Create an instance
        :param image_name: Name of the image to boot from
        :param instance_name: The name to give to the instance
        :param security_group_name: The security group to add to the instance
        :return: Returns a Finished string
        """
        if not self.nova_client.keypairs.findall(name="mykey"):
            with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
                self.nova_client.keypairs.create(name="mykey", public_key=fpubkey.read())
        image = self.nova_client.images.find(name=image_name)
        flavor = self.nova_client.flavors.find(name="m1.tiny")#because I am using VMs
        security_group_id = self.get_security_group(security_group_name)
        instance = self.nova_client.servers.create(name=instance_name, image=image,
                                                   flavor=flavor, key_name="mykey", security_group=security_group_id)

        status = instance.status
        while status == "BUILD":
            time.sleep(5)
            instance = self.nova_client.servers.get(instance.id)
            status = instance.status
            print "Building"

        print "Finished!"
        return "Finished"

    def create_security_group(self):
        """
        Create a default security group
        :return: novaclient.v2.security_group
        """
        security_group = self.nova_client.security_groups.find(name="default")
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="tcp",
                                                from_port=22, to_port=22)#SSH
        self.nova_client.security_groups_rules.create(security_group.id, ip_protocol="icmp",
                                                from_port=-1, to_port=-1)#ICMP
        return security_group

    def get_security_group(self, security_group_name):
        """
        Return a security group object by a given name
        :param security_group_name: Name of the security group
        :return: Nova client security group object
        """
        return self.nova_client.security_groups.find(name=security_group_name)

    def list_security_groups(self):
        """
        List the security groups in a tenant
        :return: List of the available security groups
        """
        try:
            return self.nova_client.security_groups.list()
        except Exception, e:
            easygui.msgbox("FAILED\n" + str(e))
            return

    def get_instance(self, instance_name):
        """
        Returns The unique instance ID of a given instance
        :param Instance_name: the name of the instance
        :return: String of the instance ID
        """
        instance_id = [x.id for x in self.list_servers() if x.name == instance_name]
        if instance_id == []:
            easygui.msgbox("Instance name could not be found")
            return None
        else:
            return instance_id[0]

    def list_floating_ip(self):
        return self.neutron_client.list_networks()
        #return type(self.nova_client.floating_ips.list())

    def get_novnc_url(self, instance_name):
        """
        Return a URL for a NoVNC console of a given instance
        :param instance_name: Name of the instance
        :return: string of the NoVNC URL
        """
        instance_id = self.get_instance(instance_name=instance_name)
        if instance_id == None:
            return
        self.active_instance(instance_id=instance_id)
        url = self.nova_client.servers.get_vnc_console(instance_id, 'novnc')["console"]["url"]
        print url
        return str(url)

    def get_instance_IP(self, instance_name):
        """
        Returns the IP address of a given instance
        :param instance_name: the name of the instance
        :return: returns a string of the instance IP address
        """
        instance_id = self.get_instance(instance_name=instance_name)
        instance = self.nova_client.servers.get(instance_id)
        if instance_id == None:
            return
        return str(instance.networks)

    def delete_instance(self, instance_name):
        """
        Delete the instance and it's volume given by the instance name
        :param instance_name: the name of the instance to be deleted
        :return does not return a value
        """
        try:
            instance_id = self.get_instance(instance_name=instance_name)
            if instance_id is None:
                return
            self.nova_client.volumes.delete_server_volume(instance_id,
                                                          self.cinder_client.get_volume_id(instance_name + "Volume"))
            self.nova_client.servers.delete(instance_name)
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong")

    def get_usage(self, all_instances, chosen_tenant = None):
        """
        Get a dictionary containing usage for a specific tenant or all of them
        :param all_instances: Boolean if to return usage for all instances
        :param chosen_tenant: Unique ID of the tenant to return the usage of
        :return: Dictionary containing usage information
        """
        if all_instances:
            try:
                return self.nova_client.usage.list(start=datetime.datetime.min,
                                                   end=datetime.datetime.now(), detailed=True).to_dict()
            except Exception, e:
                easygui.msgbox("Something went wrong please try again")
                print e
                return None
        else:
            try:
                return self.nova_client.usage.get(start=datetime.datetime.min,
                                                  end=datetime.datetime.now(), tenant_id=chosen_tenant).to_dict()
            except Exception, e:
                print e
                easygui.msgbox("Something went wrong please try again")
                return None


    def active_instance(self, instance_id):
        """
        Start an inactive instance. If active do nothing
        :param instance_id: The unique ID of the instance to activate
        """
        instance = self.nova_client.servers.get(instance_id)
        try:
            instance.start()
        except Conflict:
            pass
