import allure
import pytest

from data.project_data import ProjectResponseModel
from enums.roles import Roles


class TestProjectCreate:
    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
    @allure.title('Проверка создания проекта')
    @allure.description('Тест проверяет создание нового проекта')
    def test_project_create(self, prepared_project):
        with allure.step('Подготовка данных'):
            project_data, user = prepared_project
        with allure.step('Создание проекта'):
            create_project_response = user.api_object.project_api.create_project(project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(create_project_response)
            with pytest.assume:
                assert project_response.id == project_data.id
        with allure.step('Проверка наличия только что созданного проекта в списке проектов'):
            get_projects_response = user.api_object.project_api.get_project_by_locator(project_data.id).text
            received_project = ProjectResponseModel.model_validate_json(get_projects_response)
            with pytest.assume:
                assert received_project.id == project_data.id
