from playwright.sync_api import Page, expect
import allure


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        with allure.step(f"Переход на URL: {url}"):
            self.page.goto(url)

    def check_url(self, expected_url):
        with allure.step(f"Проверка URL: ожидаемый - {expected_url}"):
            expect(self.page).to_have_url(expected_url)

    def wait_for_url_change(self, expected_url):
        with allure.step(f"Ожидание изменения URL на {expected_url}"):
            self.page.wait_for_url(expected_url)

    def wait_for_page_load(self, timeout=3000):
        with allure.step("Ожидание загрузки страницы"):
            self.page.wait_for_load_state('load', timeout=timeout)

    def click_button(self, selector):
        with allure.step(f"Клик по элементу: {selector}"):
            self.page.click(selector)

    def is_element_presents(self, selector):
        with allure.step(f"Проверка видимости элемента: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()

    def is_button_active(self, selector):
        with allure.step(f"Проверка активности кнопки: {selector}"):
            expect(self.page.locator(selector)).to_be_enabled()

    def input_text(self, selector, text):
        with allure.step(f"Ввод текста '{text}' в элемент {selector}"):
            self.page.fill(selector, text)

    def input_filtered_text(self, selector, text):
        with allure.step(f"Ввод текста 'FILTERED' в элемент {selector}"):
            self.page.fill(selector, text)

    def wait_for_selector(self, selector):
        with allure.step(f"Ожидаем появления селектора {selector}"):
            self.page.wait_for_selector(selector, state='visible')

    def wait_for__disappear_selector(self, selector):
        with allure.step(f"Ожидаем исчезновения селектора {selector}"):
            self.page.wait_for_selector(selector, state='detached')

    def assert_text_presents_on_page(self, text):
        with allure.step(f"Проверка наличия текста '{text}' на странице"):
            expect(self.page).to_have_text(text)

    def assert_text_in_element(self, selector, text):
        with allure.step(f"Проверка наличия текста '{text}'в элементе {selector}"):
            expect(self.page).locator(selector).to_contain_text(text)

    def assert_element_attribute(self, selector, attribute, value):
        with allure.step(f"Проверка значения '{value}' атрибута '{attribute}' элемента {selector}"):
            expect(self.page.locator(selector)).to_have_attribute(value)

    def assert_element_hidden(self, selector):
        with allure.step(f"Проверка, что элемент {selector} скрыт"):
            expect(self.page).locator(selector).to_be_hidden()

    def check_url_in_new_tab(self, button, expected_url):
        with allure.step(
                f"Проверка, что при нажатии на  {button} осуществляется переход на ссылку {expected_url} в новой вкладке"):
            with self.page.context.expect_page() as new_page_info:
                self.click_button(button)
                new_page = new_page_info.value
                expect(new_page).to_have_url(expected_url)
