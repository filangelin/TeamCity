import allure
from pages.base_page import BasePage


class BuildCreationPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.go_to_build_button = 'span.icon_before >> text="Create build configuration"'
        self.build_name_selector = "input#buildTypeName"
        self.build_id_selector = "input#buildTypeExternalId"
        self.build_description_selector = "input#description"
        self.create_build_button = "input[value=Create]"

    def go_to_addition_build_page(self):
        with allure.step("Переход на страницу для создания билда"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()
            self.actions.click_button(self.go_to_build_button)

    def input_build_details(self, name, build_id, description):
        with allure.step("Ввод данных для создания билда"):
            self.actions.wait_for_selector(self.build_name_selector)
            self.actions.input_text(self.build_name_selector, name)
            self.actions.input_text(self.build_id_selector, build_id)
            self.actions.input_text(self.build_description_selector, description)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания билда"):
            self.actions.click_button(self.create_build_button)
            self.actions.wait_for_page_load()

    def create_ui_build(self, name, project_id, description):
        self.go_to_addition_build_page()
        self.input_build_details(name, project_id, description)
        self.click_create_button()
        self.actions.wait_for_page_load()



