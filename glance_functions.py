from glanceclient import client as glanceClient
import urllib2
import easygui
import constants


class Glance:
    def __init__(self, keystone_session):
        self.glance_client = glanceClient.Client(version='2', session=keystone_session)

    def create_image(self):
        #add options for different images
        image_url = easygui.enterbox(msg="Enter the image url")
        vm_image = urllib2.urlopen(image_url)
        image_name = easygui.enterbox(msg="Enter the image name")
        image = self.glance_client.images.create(name=image_name, disk_format="qcow2",
                                                 container_format="bare")
        self.glance_client.images.upload(image.id, vm_image.read())

    def list_images(self):
        return self.glance_client.images.list()

    def delete_image(self, image_id):
        self.glance_client.images.delete(image_id)

    def add_default_images(self):
        for image_name in constants.IMAGE_URLS:
            vm_image = urllib2.urlopen(constants.IMAGE_URLS[image_name])
            image = self.glance_client.images.create(name=image_name, disk_format="qcow2",
                                                     container_format="bare")
            self.glance_client.images.upload(image.id, vm_image.read())