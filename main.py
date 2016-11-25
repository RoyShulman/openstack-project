import easygui
from keystone_functions import Keystone
from glance_functions import Glance

#TODO: watch keystone endpoint again because of regions

def main():
    title = "Openstack Virtualization Platform"
    choices = ["New project", "Existing project"]
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
        user_password = easygui.passwordbox(msg="Create a password")
        if user_password is None:
            exit(1)
        keystone_client = Keystone(user_name=user_name,
                                   password=user_password, project_name=project_name,
                                   project_description=project_description)
        #print keystone_client.project_id
        if keystone_client is None:
            easygui.msgbox("Error!\nProject with this name already exists")
    elif button == "Existing project":
        project_name = easygui.enterbox(msg="Enter your project name")
        if project_name is None:
            exit(1)
        user_name = easygui.enterbox(msg="Enter your username")
        if user_name is None:
            exit(1)
        user_password = easygui.passwordbox(msg="Enter your password")
        if user_password is None:
            exit(1)
        keystone_client = Keystone(user_name=user_name,
                                   password=user_password,
                                   project_name=project_name)
        glance_client = Glance(keystone_client.sess)
        images = glance_client.list_images()
        for image in images:
            print image

        glance_client.delete_image("86bd758e-e814-4c8e-9cb8-c53a98f546a6")



if __name__ == "__main__":
    main()