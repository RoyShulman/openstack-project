from glanceclient import client as glanceClient
import urllib2
import easygui
import constants

class Glance:
    def __init__(self, keystone_session):
        self.glance_client = glanceClient.Client(version='2', session=keystone_session)

    def create_image(self):
        #add options for different images
        msgbox = easygui.msgbox(msg="Click OK to start downloading")
        if msgbox == "OK":
            vm_image = urllib2.urlopen(constants.CIRROS_VM_IMAGE)
            image = self.glance_client.images.create(name="cirros image", disk_format="qcow2",
                                                     container_format="bare")
            self.glance_client.images.upload(image.id, vm_image.read())

    def list_images(self):
        return self.glance_client.images.list()

    def delete_image(self, image_id):
        self.glance_client.images.delete(image_id)