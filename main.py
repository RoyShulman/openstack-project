import easygui
from keystone_functions import Keystone
from glance_functions import Glance
from nova_functions import Nova
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
            exit(1)

        glance_client = Glance(keystone_session=keystone_client.sess)
        #glance_client.add_default_images() takes wayyyy too long
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
        glance_client = Glance(keystone_client.sess)
        images = glance_client.list_images()
        for image in images:
            print image.id
        images = glance_client.list_images()
        for image in images:
            print image.name
        image_names = create_image_choiceboxes(images=images)
        chosen_image_name = easygui.choicebox("Available images: ", choices=image_names)
        for image in images:
            print image.id
        chosen_image_id = get_image_id(images=images, image_name=chosen_image_name)
        print glance_client.get_image(image_id=chosen_image_id)




def create_image_choiceboxes(images):
    image_names = [x.name for x in images]
    return image_names

def get_image_id(images, image_name):
    for image in images:
        if image.name == image_name:
            return image.id

if __name__ == "__main__":
    main()