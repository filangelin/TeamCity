import allure
import pytest

from data.build_data import BuildData


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

        with (allure.step('Проверка созданного билда')):
            check_build = user.api_object.build_api.check_build(build_data.id)
            with pytest.assume:
                assert check_build.status_code == 200, \
                    f"Expected status-code - 200, but given - '{check_build.status_code}''"
