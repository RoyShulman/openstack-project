from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.base import Manager, CrudManager
import constants

class Keystone:
    def __init__(self, auth_url, user_id, password, project_name, description=""):
        if project_name in constants.PROJECT_NAME_TO_ID:
            auth = v3.Password(auth_url=auth_url,
                               user_id=user_id,
                               password=password,
                               project_id=constants.PROJECT_NAME_TO_ID[project_name])
            self.project_id = constants.PROJECT_NAME_TO_ID[project_name]
            sess = session.Session(auth=auth)
            self.keystone_client = client.Client(session=sess)


    def add_user(self, name, password, email, description,  project=None):
        """function to add a new user to a project.
        If no project is specified the default project is the project which was assigned with the
        keystone client called"""
        if project is None:
            self.keystone_client.users.create(name=name, project=self.project_id, password=password, email=email,
                                              description=description)
        self.keystone_client.users.create(name=name,project_id=project, password=password, email=email,
                                          description=description)


if __name__ == "__main__":
    a = Keystone("a","A","a","A", "second project")
    print a.project_id

