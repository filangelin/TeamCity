import allure

from pages.login_page import LoginPage
from resources.user_creds import AdminCreds


@allure.title('Проверка футера')
def test_about_teamcity(browser):
    page = LoginPage(browser)
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)

    with allure.step(f"Проверка кнопки футера About TeamCity"):
        page.footer.go_to_about_teamcity()


@allure.title('Проверка футера')
def test_license_agreement(browser):
    page = LoginPage(browser)
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login(AdminCreds.USERNAME, AdminCreds.PASSWORD)

    with allure.step(f"Проверка кнопки футера License Agreement"):
        page.footer.go_to_license_agreement()
