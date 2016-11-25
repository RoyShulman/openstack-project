from keystoneclient.v2_0 import client as keystoneClient
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneauth1 import exceptions
import easygui
import constants


class Keystone:
    def __init__(self, user_name, password, project_name, project_description = None):
        #session to be used inside keystone
        self.sess = None
        if project_description is not None:
            #User wants to create a new project
            self.keystone_client = self.password_login()
            project_id = [x.id for x in self.keystone_client.tenants.list() if x.name == project_name]
            if project_id:
                easygui.msgbox("Project with this name already exists!")
                exit(1)
            else:
                project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                                 description=project_description).id
                #create the user associated with the tenant
                user_id = self.add_user(name=user_name, password=password, project_id=project_id)
                role = self.add_role(project_id=project_id, user_id=user_id)
        else:
            #user wants to login to an existing project with his user name
            self.keystone_client = self.password_login(auth_url=constants.ADMIN_AUTH_URL,
                                                       username=user_name,
                                                       password=password,
                                                       project_name=project_name)
            if self.keystone_client is None:
                easygui.msgbox("Wrong user name or password!")
                exit(1)

    def create_project(self, project_name, project_description):
        project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                         description=project_description,
                                                         enabled=True)
        return project_id

    def password_login(self, auth_url=constants.ADMIN_AUTH_URL, username=constants.ADMIN_USERNAME,
                       password=constants.ADMIN_PASSWORD, project_name=constants.ADMIN_TENANT):
        """return a keystone keystoneClient by authenticating with password"""
        auth = v2.Password(auth_url=auth_url, username=username, password=password, tenant_name=project_name)
        self.sess = session.Session(auth=auth)
        keystone_client = keystoneClient.Client(session=self.sess)
        #check if authenticated successfully
        try:
            keystone_client.users.list()
        except exceptions.http.Unauthorized:
            return None
        return keystone_client

    def add_user(self, name, password, project_id):
        """function to add a new user to a project"""
        user_id = self.keystone_client.users.create(name=name, password=password, tenant_id=project_id)
        return user_id

    def add_role(self, project_id, user_id):
        admin_role = [x.id for x in self.keystone_client.roles.list() if x.name == "admin"][0]
        role = self.keystone_client.roles.add_user_role(user=user_id, role=admin_role, tenant=project_id)
        return role

