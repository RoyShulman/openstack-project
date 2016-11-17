import easygui
from keystone_functions import 

def main():
    title = "Openstack Virtualization Platform"
    choices = ["New project", "Existing project(add a user)"]
    button = easygui.buttonbox("Choose an option", title=title, choices=choices)
    if button == "New project":
        print "a"


if __name__ == "__main__":
    main()