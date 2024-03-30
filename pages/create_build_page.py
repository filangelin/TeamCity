import allure
from pages.base_page import BasePage


class BuildCreationPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.error_id_selector = '#error_buildTypeExternalId'
        self.error_name_selector = '#error_buildTypeName'
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.go_to_build_button = 'span.icon_before >> text="Create build configuration"'
        self.build_name_selector = "input#buildTypeName"
        self.build_id_selector = "input#buildTypeExternalId"
        self.build_description_selector = "input#description"
        self.create_build_button = "input[value=Create]"
        self.created_build_page = "/admin/editVcsRoot.html?action=addVcsRoot&editingScope=buildType%3A{build_id}&cameFromUrl=%2Fadmin%2FeditBuildTypeVcsRoots.html%3Finit%3D1%26id%3DbuildType%3A{build_id}%26cameFromUrl%3D%252Fadmin%252FeditProject.html%253Finit%253D1%2526projectId%253D{project_id}&cameFromTitle=Version%20Control%20Settings&showSkip=true"

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

    def create_ui_build(self, name, build_id, description, project_id):
        self.go_to_addition_build_page()
        self.input_build_details(name, build_id, description)
        self.click_create_button()
        self.page_url = self.created_build_page.format(build_id=build_id, project_id=project_id)
        self.actions.wait_for_url_change(self.page_url, timeout=60000)

    def create_build_with_empty_name(self, name, build_id):
        self.go_to_addition_build_page()
        self.input_build_details(name, build_id, '')
        self.click_create_button()
        self.actions.assert_text_in_element(self.error_name_selector, 'Name must not be empty')

    def create_build_with_empty_id(self, name, build_id):
        self.go_to_addition_build_page()
        self.input_build_details(name, build_id, '')
        self.click_create_button()
        self.actions.assert_text_in_element(self.error_id_selector, 'The ID field must not be empty.')
