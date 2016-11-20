from keystoneclient.v2_0 import client
from keystoneauth1.identity import v2
from keystoneauth1 import session
import constants

class Keystone:
    def __init__(self, auth_url, user_name, password, project_name, project_description):
        #TODO: change to a real keystone check
        if project_name in constants.PROJECT_NAME_TO_ID:
            #TODO: add functions for user to do
            #The project name exists returning none
            return None
        else:
            #The user is creating a new project
            auth = v2.Password(auth_url=constants.ADMIN_AUTH_URL, password="password",
                               tenant_name="admin", username="admin")
            sess = session.Session(auth=auth)
            self.keystone_client = client.Client(session=sess)
            tenants = self.keystone_client.tenants.list()
            print tenants
            project_id = [x.id for x in tenants if x.name == 'Demo'][0]
            tenant = self.keystone_client.tenants.get(project_id)
            self.keystone_client.tenants.delete(tenant)
            print self.keystone_client.tenants.list()


    def create_project(self, project_name, project_description):
        project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                         description=project_description,
                                                         enabled=True)
        return project_id

    def add_user(self, name, password, project):
        """function to add a new user to a project"""
        self.keystone_client.users.create(name=name,project_id=project, password=password)


if __name__ == "__main__":
    a = Keystone("a","A","a","A", "second project")
    print a.project_id

