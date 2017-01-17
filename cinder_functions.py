from cinderclient.v2 import client as cinderClient
import easygui

class Cinder:
    def __init__(self, keystone_session):
        self.cinder_client = cinderClient.Client(session=keystone_session)

    def create_volume(self, instance_name):
        """
        Create an empty block volume for an instance. Volume will be name INSTANCE_NAME + "Volume"
        :param name: Name of the instance the volume will be added to
        """
        try:
            name = instance_name + "Volume"
            self.cinder_client.volumes.create(size=1000, name=instance_name)
        except Exception, e:
            easygui.msgbox("Something went wrong, please try again")
        finally:
            return

    def list_volumes(self):
        """
        List all available volumes
        :return: all available volumes
        """
        try:
            return self.cinder_client.volumes
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong, please try again")
            return


    def get_volume_id(self, volume_name):
        """
        Return the volume ID of a given volume name
        :param volume_name: Name of the volume
        :return: string of the unique of ID
        """
        try:
            for volume in self.list_volumes():
                if volume.name == volume_name:
                    return volume.id
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong please try again")
            return

    def attach_volume(self, instance_id, instance_name):
        """
        Attach a volume to an instance
        :param instance_id: Unique ID of the instance
        :param instance_name: Name of the instance
        """
        volume_id = self.get_volume_id(instance_name + "Volume")
        try:
            self.cinder_client.volumes.attach(volume_id, instance_id)
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong please try again")
            return
