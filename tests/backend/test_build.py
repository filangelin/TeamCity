from http import HTTPStatus

import allure
import pytest

from data.build_data import BuildData, BuildResponseModel, LocatedBuildsModel


class TestBuild:

    @allure.story('Создание билда')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка создания билда')
    @allure.description('Тест проверяет создание нового билда')
    def test_create_build(self, prepared_project):
        project_data, user = prepared_project
        with allure.step('Создание билда'):
            build_data = BuildData.create_build_data(project_data.id)
            user.api_object.build_api.create_build(build_data.model_dump())
            build_name = build_data.name

        with (allure.step('Проверка созданного билда')):
            check_build = user.api_object.build_api.check_build(build_data.id).text
            build_response = BuildResponseModel.model_validate_json(check_build)
            with pytest.assume:
                assert build_response.id == build_data.id, \
                    f"Expected build id - {build_data.id}, but given - {build_response.id}"
            with pytest.assume:
                assert build_response.name == build_name, \
                    f"Expected build name - {build_name}, but given - {build_response.name}"
            with pytest.assume:
                assert build_response.project.id == project_data.id, \
                    f"Expected build's project id - {project_data.id}, but given - {build_response.project.id}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/120', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/450', name='Тест-кейс')
    @allure.title('Проверка невозможность создания билда с пустым телом')
    @allure.description('Тест проверяет невозможность создания билда c пустым телом')
    def test_build_create_with_empty_body(self, prepared_project):
        with allure.step('Подготовка данных'):
            project_data, user = prepared_project
        with allure.step('Попытка создания проекта'):
            created_build = user.api_object.build_api.create_build({}, expected_status=HTTPStatus.BAD_REQUEST).text
        with allure.step('Проверка ответа о невозможности создания билда с пустым телом'):
            with pytest.assume:
                assert f"Build type creation request should contain project node." in created_build, \
                    f"Expected build without body can not to be created"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания одинаковых билдов')
    @allure.description('Тест проверяет невозможность создания одинаковых билдов')
    def test_create_existing_build(self, prepared_project):
        project_data, user = prepared_project
        with allure.step('Создание билда'):
            build_data = BuildData.create_build_data(project_data.id)
            user.api_object.build_api.create_build(build_data.model_dump())
        with allure.step('Попытка создания идентичного билда'):
            user.api_object.build_api.create_build(build_data.model_dump(), expected_status=HTTPStatus.BAD_REQUEST)
            build_of_project = user.api_object.build_api.locate_builds_of_project(project_data.id).text
            located_response = LocatedBuildsModel.model_validate_json(build_of_project)
            with pytest.assume:
                assert located_response.count == 1, \
                    f"Expected project has 1 build, but given - {located_response.count} builds"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка удаления билда')
    @allure.description('Тест проверяет удаление билда')
    def test_delete_build(self, prepared_project):
        project_data, user = prepared_project
        with allure.step('Создание билда'):
            build_data = BuildData.create_build_data(project_data.id)
            user.api_object.build_api.create_build(build_data.model_dump())
        with (allure.step('Проверка, что у проекта появился билд')):
            build_of_project = user.api_object.build_api.locate_builds_of_project(project_data.id).text
            located_response = LocatedBuildsModel.model_validate_json(build_of_project)
            with pytest.assume:
                assert located_response.count == 1, \
                    f"Expected project has build, but given - {located_response.count} builds"
            with pytest.assume:
                assert located_response.buildType[0].id == build_data.id, \
                    f"Expected project's build id - {project_data.id}, but given - {located_response.buildType[0].id}"

        with allure.step('Удаление билда'):
            user.api_object.build_api.delete_build(build_data.id)
        with allure.step('Проверка отсутствия удаленного билда'):
            user.api_object.build_api.check_build(build_data.id, expected_status=HTTPStatus.NOT_FOUND)
        with allure.step('Проверка, что у проекта нет билдов'):
            build_of_project = user.api_object.build_api.locate_builds_of_project(project_data.id).text
            located_response = LocatedBuildsModel.model_validate_json(build_of_project)
            with pytest.assume:
                assert located_response.count == 0, \
                    f"Expected project hasn't builds, but given - {located_response.count} builds"
