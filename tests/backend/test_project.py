from http import HTTPStatus

import allure
import pytest

from data.project_data import ProjectResponseModel


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
                assert project_response.id == project_data.id, \
                    f"Expected project id - {project_data.id}, but given - {project_response.id}"
        with allure.step('Проверка наличия только что созданного проекта в списке проектов'):
            get_projects_response = user.api_object.project_api.get_project_by_locator(project_data.id).text
            received_project = ProjectResponseModel.model_validate_json(get_projects_response)
            with pytest.assume:
                assert received_project.id == project_data.id, \
                    f"Expected project id - {project_data.id}, but given - {received_project.id}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/120', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/450', name='Тест-кейс')
    @allure.title('Проверка невозможность создания проекта с пустым телом')
    @allure.description('Тест проверяет невозможность создания проекта c пустым телом')
    def test_project_create_with_empty_body(self, super_admin):
        with allure.step('Попытка создания проекта'):
            created_project = super_admin.api_object.project_api.create_project({}, expected_status=HTTPStatus.BAD_REQUEST).text
        with allure.step('Проверка ответа о невозможности создания проекта с пустым телом'):
            with pytest.assume:
                assert f"Project name cannot be empty." in created_project, \
                    f"Expected project without body can not to be created"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
    @allure.title('Проверка невозможность создания проекта c занятым именем')
    @allure.description('Тест проверяет невозможность создания проекта c уже занятым именем')
    def test_project_create_with_taken_name(self, prepared_project):
        with allure.step('Подготовка данных'):
            project_data, user = prepared_project
            project_data_2 = {**project_data.model_dump(), 'name': project_data.name, 'id': f'{project_data.id}_id'}
        with allure.step('Создание проекта'):
            user.api_object.project_api.create_project(project_data.model_dump())
        with allure.step('Попытка создания проекта 2'):
            user.api_object.project_api.create_project(project_data_2, expected_status=HTTPStatus.BAD_REQUEST)
        with allure.step('Проверка, что не создался проект с занятым именем'):
            get_project = user.api_object.project_api.get_project().json()
            project_ids = [project.get('id') for project in get_project.get('project')]
            with pytest.assume:
                assert project_data_2.get('id') not in project_ids, \
                    f"Expected project with id - {project_data_2.get('id')} doesn't exist"
