import easygui
from keystone_functions import Keystone
import constants


def main():
    title = "Openstack Virtualization Platform"
    choices = ["New project", "Existing project(add a user)"]
    button = easygui.buttonbox("Choose an option", title=title, choices=choices)
    if button == "New project":
        project_name = easygui.enterbox(msg="Enter your new project name")
        if project_name is None:
            exit(1)
        project_description = easygui.enterbox(msg="Enter your project description")
        if project_description is None:
            exit(1)
        user_name = easygui.enterbox(msg="Create a user name")
        if user_name is None:
            exit(1)
        user_password = easygui.enterbox(msg="Create a password")
        if user_password is None:
            exit(1)
        keystone_client = Keystone(auth_url=constants.ADMIN_AUTH_URL, user_name=user_name,
                                   password=user_password, project_name=project_name,
                                   project_description=project_description,
                                   type="New")
        #print keystone_client.project_id
        if keystone_client is None:
            print "here"
            print keystone_client
            easygui.msgbox("Error!\nProject with this name already exists")


if __name__ == "__main__":
    main()