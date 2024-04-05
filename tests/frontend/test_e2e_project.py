import allure
import pytest

from pages.login_page import LoginPage
from pages.create_project_page import ProjectCreationPage
from data.project_data import ProjectResponseModel
from pages.project_management_page import ProjectManagementPage
from resources.user_creds import AdminCreds


@allure.feature('Управление проектами')
@allure.story('Создание проекта UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
@allure.title('Проверка создания проекта UI')
@allure.description('Тест проверяет создание нового проекта через UI')
@pytest.mark.teardown_required
def test_create_project(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()
        project_id = project_data.id
        project_name = project_data.name

    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project(project_name, project_id, f'Описание проекта {project_name}')

    with allure.step("Отправка запроса на получение информации созданного проекта"):
        response = super_admin.api_object.project_api.get_project_by_locator(project_data.name).text
        created_project = ProjectResponseModel.model_validate_json(response)
        assert created_project.id == project_data.id, \
            f"Project with id {project_data.id} not found"


@allure.feature('Управление проектами')
@allure.story('Удаление проекта UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
@allure.title('Проверка удаления проекта UI')
@allure.description('Тест проверяет удаление проекта через UI')
def test_delete_project(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()

    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step("Создание проекта"):
        super_admin.api_object.project_api.create_project(project_data.model_dump())
    with allure.step("Удаление проекта"):
        project_management_browser = ProjectManagementPage(browser)
        project_management_browser.delete_project(project_data.id)

    with allure.step("Отправка запроса для проверки удаления проекта"):
        get_project = super_admin.api_object.project_api.get_project().json()
        project_ids = [project.get('id') for project in get_project.get('project')]
        assert project_data.id not in project_ids, "Project found, but expected to be deleted"


def test_create_project_with_empty_name(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()
        project_id = project_data.id
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step("Создание проекта c пустым именем"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_with_empty_name(project_id)


def test_create_project_with_empty_id(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()
        project_name = project_data.name
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step("Создание проекта c пустым id"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_with_empty_id(project_name)


def test_create_project_with_nonlatin_id(browser, project_data_body, super_admin):
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step("Создание проекта c id символами нелатинского алфавита"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_with_nonlatin_id('проект', 'айди')
