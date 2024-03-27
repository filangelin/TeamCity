import allure
from playwright.sync_api import Page, expect
from enums.host import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/login.html')
        self.username_field = '#username'
        self.password_field = '#password'
        self.login_button = '.loginButton'

    def go_to_login_page(self):
        with allure.step("Переход на страницу авторизации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def input_login_details(self, username, password):
        with allure.step("Ввод данных для авторизации"):
            self.actions.input_text(self.username_field, username)
            self.actions.input_text(self.password_field, password)

    def click_login_button(self):
        with allure.step("Нажатие на кнопку 'Log in'"):
            self.actions.click_button(self.login_button)

    def login(self, username, password):
        self.go_to_login_page()
        self.input_login_details(username, password)
        self.click_login_button()
        self.page_url = ('/favorite/projects?mode=builds')
        self.actions.wait_for_url_change(self.page_url, timeout=60000)
