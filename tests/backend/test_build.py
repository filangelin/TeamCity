import allure
import pytest

from data.build_data import BuildData, BuildResponseModel


class TestBuild:

    @allure.story('Создание билда')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка создания билда')
    @allure.description('Тест проверяет создание нового билда')
    def test_check_build_status(self, prepared_project):
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
