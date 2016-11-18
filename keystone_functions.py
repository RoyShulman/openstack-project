from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session
import constants

class Keystone:
    def __init__(self, auth_url, user_name, password, project_name, project_description):
        if project_name in constants.PROJECT_NAME_TO_ID:
            #TODO: add functions for user to do
            #The project name exists returning none
            return None
        else:
            #The user is creating a new project
            auth = v3.Token(auth_url=constants.ADMIN_AUTH_URL, token=constants.ADMIN_TOKEN)
            sess = session.Session(auth=auth)
            self.keystone_client = client.Client(session=sess)
            self.project_id = self.create_project(project_name=project_name, project_description=project_description)
            self.add_user(self, name=user_name, password=password, project=self.project_id)

    def create_project(self, project_name, project_description):
        project_id = client.projects.ProjectManager(self.keystone_client).create(name=project_name,
                                                                                 domain=constants.KEYSTONE_DOMAIN,
                                                                                 description=project_description).id
        return project_id

    def add_user(self, name, password, project):
        """function to add a new user to a project"""
        self.keystone_client.users.create(name=name,project_id=project, password=password)


if __name__ == "__main__":
    a = Keystone("a","A","a","A", "second project")
    print a.project_id

