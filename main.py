import easygui
from keystone_functions import Keystone
from glance_functions import Glance
from nova_functions import Nova
from swift_functions import Swift



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
        exit = False
        while not exit:
            choices = ["Create a Virtual Machine" ,"Upload A File", "List Files", ]
        glance_client = Glance(keystone_session=keystone_client.sess)
        glance_client.create_image()
        if glance_client.list_images() is None:
            easygui.msgbox("Error!\nInstalling images unsuccessful")
            exit(1)

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
        glance_client = Glance(keystone_session=keystone_client.sess)
        nova_client = Nova(keystone_session=keystone_client.sess)
        easygui.msgbox(str(nova_client.get_novnc_url("demo-instanc")) + "\n\n\nIF YOU SEE CONTROLLER REPLACE WITH 10.10.10.51")
        image_names = create_image_choiceboxes(images=glance_client.list_images())
        chosen_image_name = easygui.choicebox("Available images: ", choices=image_names)


def create_image_choiceboxes(images):
    image_names = [x.name for x in images]
    return image_names


def get_image_id(glance_client, image_name):
    images = glance_client.list_images()
    for image in images:
        if image.name == image_name:
            return image.id


if __name__ == "__main__":
    main()