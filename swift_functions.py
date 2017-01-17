from swiftclient import client as SwiftClient
from swiftclient import ClientException
import easygui
from exceptions import IOError
import os
from keystone_functions import Keystone
import constants

class Swift:
    def __init__(self):
        self.swift_client = SwiftClient.Connection(session=Keystone(constants.ADMIN_USERNAME, constants.ADMIN_PASSWORD,
                                                                    constants.ADMIN_TENANT).sess)
        self.account = self.swift_client.get_account()
        self.container = self.account[1][0]

    def upload_file(self, file):
        """
        Upload a file to the swift admin container
        :param file: Path to the file
        """
        try:
            with open(file, 'r') as file_to_upload:
                    file_name = file.split("/")[-1]
                    self.swift_client.put_object(container=self.container['name'],
                                                 obj=file_name,
                                                 contents=file_to_upload.read(),
                                                 content_type='text/plain')
        except IOError as error:
                if error.errno == 2:
                    easygui.msgbox("Error!\nFile not found")
        except ClientException:
            easygui.msgbox("Error!\nCannot upload file")
        finally:
            return

    def list_files(self):
        """
        Show a message box with the list of files
        """
        return_files = []
        try:
            files = self.swift_client.get_container(self.container['name'])[1]
            for file in files:
                return_files.append(file["name"] + " |")

            s = " ".join(return_files)
            easygui.msgbox(str(s))
        except ClientException:
            easygui.msgbox("Error!\nFailed to complete request")
        finally:
            return

    def get_file(self, file_name):
        """
        Download a file from the container and create it in the users home directory
        :param file_name: The name of the file to download
        """
        try:
            file = self.swift_client.get_object(self.container['name'], file_name)[1]
        except ClientException:
            easygui.msgbox("Error!\nFailed to complete request")
            return
        with open(os.path.expanduser("~") + "/" + file_name, 'w') as new_file:
            new_file.write(file)

    def delete_file(self, file_name):
        """
        Delete a file from the container
        :param file_name: Name of the file to delete
        """
        try:
            self.swift_client.delete_object(self.container['name'], file_name)
        except ClientException:
            easygui.msgbox('Error!\n Failed to complete request')