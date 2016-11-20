from keystoneclient.v2_0 import client
from keystoneauth1.identity import v2
from keystoneauth1 import session
import easygui
import constants

#TODO: add a login function to not repeat code

class Keystone:
    def __init__(self, auth_url, user_name, password, project_name, project_description, type):
        if type == "New":
            #User wants to create a new project
            auth = v2.Password(auth_url=constants.ADMIN_AUTH_URL, username="admin",
                               password="password", tenant_name="admin")
            sess = session.Session(auth=auth)
            self.keystone_client = client.Client(session=sess)
            project_id = [x.id for x in self.keystone_client.tenants.list() if x.name == project_name]
            if project_id:
                easygui.msgbox("Project with this name already exists!")
                exit(1)
            else:
                auth = v2.Password(auth_url=constants.ADMIN_AUTH_URL, username="admin",
                               password="password", tenant_name="admin")
                sess = session.Session(auth=auth)
                self.keystone_client = client.Client(session=sess)
                project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                                 description=project_description).id
                #create the user associated with the tenant

                self.add_user(name=user_name, password=password, project_id=project_id)
                print self.keystone_client.users.list()

    def create_project(self, project_name, project_description):
        project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                         description=project_description,
                                                         enabled=True)
        return project_id

    def add_user(self, name, password, project_id):
        """function to add a new user to a project"""
        self.keystone_client.users.create(name=name, password=password, tenant_id=project_id)


if __name__ == "__main__":
    a = Keystone("a","A","a","A", "second project")
    print a.project_id

