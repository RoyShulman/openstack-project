from cinderclient.v2 import client as cinderClient
import easygui

class Cinder:
    def __init__(self, keystone_session):
        self.cinder_client = cinderClient.Client(session=keystone_session)

    def create_volume(self, name):
        try:
            name = name + "Volume"
            self.cinder_client.volumes.create(size=1000, name=name)
        except Exception, e:
            easygui.msgbox("Something went wrong, please try again")
        finally:
            return

    def list_volumes(self):
        try:
            return self.cinder_client.volumes
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong, please try again")
            return


    def get_volume_id(self, volume_name):
        try:
            for volume in self.list_volumes():
                if volume.name == volume_name:
                    return volume.id
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong please try again")
            return

    def attach_volume(self, instance_id, instance_name):
        volume_id = self.get_volume_id(instance_name + "Volume")
        try:
            self.cinder_client.volumes.attach(volume_id, instance_id)
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong please try again")
            return
