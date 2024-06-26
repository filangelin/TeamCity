import pytest
import requests

from data.project_data import ProjectDataModel, ProjectData
from data.user_data import UserData
from entities.user import User, Role
from enums.roles import Roles
from resources.user_creds import SuperAdminCreds
from api.api_manager import ApiManager


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def project_data_body(super_admin) -> ProjectDataModel:
    project_id_pool = []

    def _create_project_data():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        return project

    yield _create_project_data

    for project_id in project_id_pool:
        super_admin.api_object.project_api.clean_up_project(project_id)


@pytest.fixture()
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, new_session, ["SUPER_ADMIN", "g"])
    super_admin.api_object.auth_api.auth_and_get_csrf(super_admin.creds)
    return super_admin


@pytest.fixture
def user_create(user_session, super_admin):
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_object.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])

        return User(user_data['username'], user_data['password'], new_session, [Role(role)])

    yield _user_create

    for username in created_users_pool:
        super_admin.api_object.user_api.delete_user(username)


@pytest.fixture(params=[Roles.SYSTEM_ADMIN, Roles.PROJECT_ADMIN, Roles.AGENT_MANAGER])
def prepared_project(request, user_create, project_data_body):
    role = request.param
    project_data = project_data_body()
    user = user_create(role.value)
    user.api_object.auth_api.auth_and_get_csrf(user.creds)
    function_name = request.node.name
    if not function_name.startswith("test_project_create"):
        user.api_object.project_api.create_project(project_data.model_dump())
    return project_data, user
