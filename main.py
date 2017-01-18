import easygui
import constants

from keystone_functions import Keystone
from glance_functions import Glance
from nova_functions import Nova
from swift_functions import Swift
from cinder_functions import Cinder

#TODO: add floating ip to instances

def main():
    while True:
        Exit = False
        title = "Openstack Virtualization Platform"
        choices = ["New project", "Existing project", "System Admin", "Exit"]
        button = easygui.buttonbox("Choose an option", title=title, choices=choices)
        if button == "Exit":
            exit(1)
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
            if keystone_client == "Name Exists":
                easygui.msgbox("Project with this name is already taken, try a different name")
                continue
            if keystone_client == "Username exists":
                continue
            glance_client = Glance(keystone_session=keystone_client.sess)
            swift_client = Swift()
            #print keystone_client.project_id

            while not Exit:
                choices = ["Create A Virtual Machine", "Access Virtual Machine", "Delete VM","Upload A File",
                           "List Files", "Download A File", "Upload Image File","Delete File", "Exit"]
                button = easygui.buttonbox(msg="What do you want to do?", choices=choices)
                if button == "Exit":
                    Exit = True
                    break
                if button == "Create A Virtual Machine":
                    instance_name = create_virtual_machine(glance_client, nova_client)
                    if instance_name is None:
                        easygui.msgbox("Failed to create virtual machine")
                        continue
                    answer = easygui.buttonbox("Would you like to add a hard drive to your machine?",
                                      choices=["Yes", "No"])
                    if answer == "Yes":
                        cinder_client.create_volume(name=instance_name + "Volume")
                        cinder_client.attach_volume(nova_client.get_instance(instance_name), instance_name)
                elif button == "Access Virtual Machine":
                    instance = choose_instance(nova_client)
                    url = nova_client.get_novnc_url(instance_name=instance)
                    if url == None:
                        continue
                    easygui.msgbox(title="Instance URL and IP", msg=url + "\n" + nova_client.get_instance_IP(instance))
                    continue
                elif button == "Upload A File":
                    file_path = easygui.enterbox("Please enter the full file path")
                    if file_path is None:
                        easygui.msgbox("Enter enter a file path next time")
                        continue
                    swift_client.upload_file(file_path)
                    continue
                elif button == "List Files":
                    swift_client.list_files()
                    continue
                elif button == "Delete File":
                    file_to_deleted = easygui.enterbox("Please the name for file to delete")
                    if file_to_deleted is None:
                        easygui.msgbox("Enter a file next time please")
                        continue
                    swift_client.delete_file(file_to_deleted)
                    continue
                elif button == "Download A File":
                    file_name = easygui.enterbox("Please enter the file name you want to download")
                    if file_name is None:
                        easygui.msgbox("Please enter a file name next time")
                        continue
                    swift_client.get_file(file_name)
                    continue
                elif button == "Delete VM":
                    instance_name = easygui.enterbox("Enter Instance Name")
                    if instance_name is None:
                        easygui.msgbox("Input a name next time please")
                        continue
                    nova_client.delete_instance(instance_name)
        if Exit:
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
            if keystone_client == "Wrong User":
                continue
            glance_client = Glance(keystone_session=keystone_client.sess)
            nova_client = Nova(keystone_session=keystone_client.sess)
            swift_client = Swift()
            cinder_client = Cinder(keystone_session=keystone_client.sess)
            while not Exit:
                choices = ["Create A Virtual Machine", "Access Virtual Machine", "Delete VM","Upload A File",
                           "List Files", "Download A File", "Upload Image File","Delete File", "Exit"]
                button = easygui.buttonbox(msg="What do you want to do?", choices=choices)
                if button == "Exit":
                    Exit = True
                    break
                if button == "Create A Virtual Machine":
                    instance_name = create_virtual_machine(glance_client, nova_client)
                    if instance_name is None:
                        easygui.msgbox("Failed to create virtual machine")
                        continue
                    answer = easygui.buttonbox("Would you like to add a hard drive to your machine?",
                                      choices=["Yes", "No"])
                    if answer == "Yes":
                        cinder_client.create_volume(name=instance_name + "Volume")
                        cinder_client.attach_volume(nova_client.get_instance(instance_name), instance_name)
                elif button == "Access Virtual Machine":
                    instance = choose_instance(nova_client)
                    url = nova_client.get_novnc_url(instance_name=instance)
                    if url == None:
                        continue
                    easygui.msgbox(title="Instance URL and IP", msg=url + "\n" + nova_client.get_instance_IP(instance))
                    continue
                elif button == "Upload A File":
                    file_path = easygui.enterbox("Please enter the full file path")
                    if file_path is None:
                        easygui.msgbox("Enter enter a file path next time")
                        continue
                    swift_client.upload_file(file_path)
                    continue
                elif button == "List Files":
                    swift_client.list_files()
                    continue
                elif button == "Delete File":
                    file_to_deleted = easygui.enterbox("Please the name for file to delete")
                    if file_to_deleted is None:
                        easygui.msgbox("Enter a file next time please")
                        continue
                    swift_client.delete_file(file_to_deleted)
                    continue
                elif button == "Download A File":
                    file_name = easygui.enterbox("Please enter the file name you want to download")
                    if file_name is None:
                        easygui.msgbox("Please enter a file name next time")
                        continue
                    swift_client.get_file(file_name)
                    continue
                elif button == "Delete VM":
                    instance_name = easygui.enterbox("Enter Instance Name")
                    if instance_name is None:
                        easygui.msgbox("Input a name next time please")
                        continue
                    nova_client.delete_instance(instance_name)
        elif button == "System Admin":
            Exit = False
            username = easygui.enterbox("Enter your username")
            if username is None:
                easygui.msgbox("Enter a username next time")
                continue
            password = easygui.enterbox("Enter your password")
            if password is None:
                easygui.msgbox("Please enter your password next time please")

            if username == constants.SYSTEM_ADMIN_USERNAME and password == constants.SYSTEM_ADMIN_PASSWORD:
                while not Exit:
                    Exit = handle_system_admin()
            else:
                easygui.msgbox("Username or password incorrect please try again")
                continue


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
    security_groups = [x.name for x in nova_client.list_security_groups()]
    chosen_security_group = easygui.choicebox("Available security groups: ", choices=security_groups)
    instance_name = easygui.enterbox("Please input your instance name")
    if instance_name == None:
        easygui.msgbox("Please enter an instance name next time")
        return None
    nova_client.create_instance(image_name=chosen_image_name, instance_name=instance_name,
                                security_group_name=chosen_security_group)
    return chosen_image_name


def choose_instance(nova_client):
    instances = [x.name for x in nova_client.list_servers()]
    instance_name = easygui.choicebox(msg="Select the instance you want", choices=instances)
    return instance_name


def handle_system_admin():
    keystone_client = Keystone(system_admin=True)
    nova_client = Nova(keystone_session=keystone_client.sess)
    choices = ["Show logs for all instances", "Show logs for a tenant", "Exit"]
    button = easygui.buttonbox("Choose an option", choices=choices)
    if button == "Show logs for all instances":
        show_all_instances_log(nova_client)
    elif button == "Show logs for a tenant":
        show_tenant_log(nova_client=nova_client, keystone_client=keystone_client)
    elif button == "Exit":
        return True


def show_all_instances_log(nova_client):
    usage = nova_client.get_usage(all_instances=True)
    print usage
    if usage is not None:
        easygui.msgbox(usage)


def show_tenant_log(nova_client, keystone_client):
        tenant_chosen = choose_tenant(keystone_client=keystone_client)
        usage = nova_client.get_usage(all_instances=False, chosen_tenant=tenant_chosen)
        easygui.msgbox(usage)


def choose_tenant(keystone_client):
    tenants = [x.name for x in keystone_client.list_projects()]
    tenant_name = easygui.choicebox(msg="Select the tenant you want", choices=tenants)
    return tenant_name

if __name__ == "__main__":
    main()