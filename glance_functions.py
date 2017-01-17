from glanceclient import client as glanceClient
import urllib2
import easygui
import constants

#NOTE TO SELF: all images have --is-public set to True because upload time takes very long

class Glance:
    def __init__(self, keystone_session):
        self.glance_client = glanceClient.Client(version='2', session=keystone_session)

    def create_image(self):
        """
        Create a new image file
        """
        #add options for different images
        image_url = easygui.enterbox(msg="Enter the image url(Nothing for the default)")
        if image_url == "":#user wants to add the default images
            vm_image = urllib2.urlopen(constants.IMAGE_URLS["CIRROS_VM_IMAGE"])
            image_name = "CIRROS_VM_IMAGE"
        else:
            vm_image = urllib2.urlopen(image_url)
            image_name = easygui.enterbox(msg="Enter the image name")
        image = self.glance_client.images.create(name=image_name, disk_format="qcow2",
                                                 container_format="bare")
        self.glance_client.images.upload(image.id, vm_image.read())

    def get_image(self, image_id):
        """
        Return an glance image type
        :param image_id: The unique ID of the image
        :return: glance.image
        """
        return self.glance_client.images.get(image_id)

    def list_images(self):
        """
        List all available images
        :return: List of all images
        """
        return self.glance_client.images.list()

    def delete_image(self, image_id):
        """
        Delete an given image file
        :param image_id: The unique ID of the image to delete
        """
        try:
            self.glance_client.images.delete(image_id)
        except Exception, e:
            easygui.msgbox("Something went wrong please try again")
            print e
            return

    def add_default_images(self):
        """
        Add all the default images in the constants file
        """
        for image_name in constants.IMAGE_URLS:
            vm_image = urllib2.urlopen(constants.IMAGE_URLS[image_name])
            print "adding image: ", image_name
            image = self.glance_client.images.create(name=image_name, disk_format="qcow2",
                                                     container_format="bare")
            self.glance_client.images.upload(image.id, vm_image.read())