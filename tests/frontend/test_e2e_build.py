import time
from http import HTTPStatus

import allure
import pytest

from data.build_data import BuildData, BuildResponseModel
from pages.build_management_page import BuildManagementPage
from pages.create_build_page import BuildCreationPage
from pages.login_page import LoginPage
from resources.user_creds import AdminCreds


@allure.feature('Управление билдами')
@allure.story('Создание билда UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
@allure.title('Проверка создания билда UI')
@allure.description('Тест проверяет создание нового билда через UI')
@pytest.mark.teardown_required
def test_create_build(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()
        build_data = BuildData.create_build_data(project_data.id)
        build_name = build_data.name
        build_id = build_data.id

    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)

    with allure.step('Создание проекта'):
        super_admin.api_object.project_api.create_project(project_data.model_dump())
    with allure.step('Создание билда'):
        build_creation_browser = BuildCreationPage(browser, project_data.id)
        build_creation_browser.create_ui_build(build_name, build_id, f'Описание билда {build_name}')

    with (allure.step('Проверка созданного билда')):
        check_build = super_admin.api_object.build_api.check_build(build_data.id).text
        build_response = BuildResponseModel.model_validate_json(check_build)
        with pytest.assume:
            assert build_response.id == build_data.id, \
                f"Build with id {build_data.id} not found"


@allure.feature('Управление билдами')
@allure.story('Удаление билда UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
@allure.title('Проверка удаления билда UI')
@allure.description('Тест проверяет удаление билда через UI')
@pytest.mark.teardown_required
def test_delete_build(browser, project_data_body, super_admin):
    with allure.step("Подготовка данных"):
        project_data = project_data_body()
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)
    with allure.step('Создание проекта'):
        super_admin.api_object.project_api.create_project(project_data.model_dump())
    with allure.step('Создание билда'):
        build_data = BuildData.create_build_data(project_data.id)
        super_admin.api_object.build_api.create_build(build_data.model_dump())

    with allure.step("Удаление билда"):
        build_management_browser = BuildManagementPage(browser)
        build_management_browser.delete_build_ui(build_data.id, project_data.id)

    with allure.step('Проверка отсутствия удаленного билда'):
        super_admin.api_object.build_api.check_build(build_data.id, expected_status=HTTPStatus.NOT_FOUND)
