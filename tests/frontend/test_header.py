import allure

from pages.login_page import LoginPage
from resources.user_creds import AdminCreds


@allure.feature('Элементы страницы')
@allure.story('Создание проекта UI')
@allure.severity(allure.severity_level.MINOR)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
@allure.title('Проверка футера')
def test_header_projects(browser):
    page = LoginPage(browser)
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)

    with allure.step("Проверка кнопки хэдера Projects"):
        page.header.go_to_projects_throw_header_button()
