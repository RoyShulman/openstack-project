from keystoneclient.v2_0 import client as keystoneClient
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneauth1 import exceptions
import easygui
import constants


class Keystone:
    def __init__(self, user_name = None, password = None,
                 project_name = None , project_description = None, system_admin = None):
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
                if user_id == "Username exists":
                    easygui.msgbox("Project with this name is already taken, try a different name")
                    self.keystone_client.tenants.delete(project_id)
                    exit(1)
                role = self.add_admin_role(project_id=project_id, user_id=user_id)

        elif system_admin:
            #SYSTEM ADMIN LOGGING ON
            self.keystone_client = self.password_login()


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
        """
        Create a new tenant
        :param project_name: The name of the project(Tenant) to create
        :param project_description: The description for the project
        :return: The unique ID of the newly created project(String type)
        """
        project_id = self.keystone_client.tenants.create(tenant_name=project_name,
                                                         description=project_description,
                                                         enabled=True)
        return project_id

    def password_login(self, auth_url=constants.ADMIN_AUTH_URL, username=constants.ADMIN_USERNAME,
                       password=constants.ADMIN_PASSWORD, project_name=constants.ADMIN_TENANT):
        """
        Login to keystone and create a keystone object.
        If no parameters are passed logs in using admin credentials
        :param auth_url: Url endpoint to connect to
        :param username: The username to login with
        :param password: The password to login with
        :param project_name: Name of the project to login to
        :return: a keystone client object
        """
        auth = v2.Password(auth_url=auth_url, username=username, password=password, tenant_name=project_name)
        self.sess = session.Session(auth=auth)
        keystone_client = keystoneClient.Client(session=self.sess)
        #check if authenticated successfully
        try:
            keystone_client.users.list()
        except exceptions.http.Unauthorized:
            return None
        except exceptions.connection.ConnectFailure:
            easygui.msgbox("Error!\nCould not establish conection to keystone service")
            return None
        except exceptions.catalog.EmptyCatalog:
            easygui.msgbox("Could not connect to service endpoint! contact system admin!")
            return None
        return keystone_client

    def add_user(self, name, password, project_id):
        """
        Add a user to a given project
        :param name: Name of the user to create
        :param password: The password to give to the user
        :param project_id: The unique ID for the project to associate the user to
        :return: The unique ID of the newly created user
        """
        try:
            user_id = self.keystone_client.users.create(name=name, password=password, tenant_id=project_id)
        except exceptions.http.Conflict:
            easygui.msgbox("Username already taken!")
            return "Username exists"
        return user_id

    def add_admin_role(self, project_id, user_id):
        """
        Associate a user with the admin role
        :param project_id: The unique ID of the project the user is associated with
        :param user_id: The unique ID of the user
        :return: Return the unique ID of the role
        """
        try:
            admin_role = [x.id for x in self.keystone_client.roles.list() if x.name == "admin"][0]
            role = self.keystone_client.roles.add_user_role(user=user_id, role=admin_role, tenant=project_id)
            return role
        except Exception, e:
            easygui.msgbox("Something went wrong please try again")
            print e
            return

    def list_projects(self):
        """
        List all available tenants
        :return: List of all projects(Tenants)
        """
        try:
            return self.keystone_client.tenants.list()
        except Exception, e:
            easygui.msgbox("Something went wrong please try again")
            print e
            return

    def get_tenant(self, tenant_name):
        try:
            tenant = [x.id for x in self.list_projects() if tenant_name == x.name]
            if tenant is not None:
                return self.keystone_client.tenants.get(tenant[0])
        except Exception, e:
            print e
            easygui.msgbox("Something went wrong please try again")


