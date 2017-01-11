import easygui
from keystone_functions import Keystone
from glance_functions import Glance
from nova_functions import Nova
from swift_functions import Swift



def main():
    while True:
        title = "Openstack Virtualization Platform"
        choices = ["New project", "Existing project"]
        button = easygui.buttonbox("Choose an option", title=title, choices=choices)
        if button == "New project":
            project_name = easygui.enterbox(msg="Enter your new project name")
            if project_name is None:
                easygui.msgbox("Please Enter project Name")
                continue
            project_description = easygui.enterbox(msg="Enter your project description")
            if project_description is None:
                easygui.msgbox("Please enter a project description next time")
                continue
            user_name = easygui.enterbox(msg="Create a user name")
            if user_name is None:
                easygui.msgbox("Please enter a username next time")
                continue
            user_password = easygui.passwordbox(msg="Create a password")
            if user_password is None:
                easygui.msgbox("Please enter a password next time")
                continue
            confirm_password = easygui.passwordbox(msg="Please enter your password again")
            if not user_password == confirm_password:
                easygui.msgbox("Passwords do not match, try again")
                continue




            keystone_client = Keystone(user_name=user_name,
                                       password=user_password, project_name=project_name,
                                       project_description=project_description)
            glance_client = Glance(keystone_session=keystone_client.sess)
            #print keystone_client.project_id
            exit = False
            while not exit:
                choices = ["Create A Virtual Machine" "Access Virtual Machine" ,"Upload A File",
                           "List Files", "Download A File"]
                easygui.buttonbox(msg="What do you want to do?", choices=choices)
                if button == "Create A Virtual Machine":
                    if create_virtual_machine(glance_client, nova_client) is None:
                        easygui.msgbox("Failed to create virtual machine")
                        continue
                elif button == "Access Virtual Machine":
                    instance = choose_instance(nova_client)
                    easygui.msgbox(title="Instance URL", msg=nova_client.get_novnc_url(instance_name=instance))
            glance_client.create_image()
            if glance_client.list_images() is None:
                easygui.msgbox("Error!\nInstalling images unsuccessful")
                continue




        elif button == "Existing project":
            project_name = easygui.enterbox(msg="Enter your project name")
            if project_name is None:
                easygui.msgbox("Please enter a project name")
                continue
            user_name = easygui.enterbox(msg="Enter your username")
            if user_name is None:
                easygui.msgbox("Please enter a username next time")
                continue
            user_password = easygui.passwordbox(msg="Enter your password")
            if user_password is None:
                easygui.msgbox("Please enter your password next time")
                continue
            keystone_client = Keystone(user_name=user_name,
                                       password=user_password,
                                       project_name=project_name)
            glance_client = Glance(keystone_session=keystone_client.sess)
            nova_client = Nova(keystone_session=keystone_client.sess)
            easygui.msgbox(nova_client.create_floating_ip())
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

def create_virtual_machine(glance_client, nova_client):
    image_names = create_image_choiceboxes(glance_client.list_images())
    chosen_image_name = easygui.choicebox("Available images: ", choices=image_names)
    security_groups = nova_client.list_security_groups()
    chosen_security_group = easygui.choicebox("Available security groups: ", choices=security_groups)
    instance_name = easygui.enterbox("Please input your instance name")
    if instance_name == None:
        easygui.msgbox("Please enter an instance name next time")
        return None
    nova_client.create_instance(image_name=chosen_image_name, instance_name=instance_name,
                                security_group_name=chosen_security_group)

def choose_instance(nova_client):
    instances = [x.name for x in nova_client.list_servers()]
    instance_name = easygui.choicebox(msg="Select the instance you want", choices=instances)
    return instance_name



if __name__ == "__main__":
    main()