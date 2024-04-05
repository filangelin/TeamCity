import allure

from pages.base_page import BasePage


class MenuListCreateFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.create_from_url_selector = "a.createOption:has-text('From a repository URL')"
        self.create_manually_selector = "a.createOption:has-text(' Manually')"

    def click_create_from_url(self):
        with allure.step("Выбор создания проекта по URL"):
            self.actions.click_button(self.create_from_url_selector)

    def click_create_manually(self):
        with allure.step("Выбор создания проекта вручную"):
            self.actions.click_button(self.create_manually_selector)

    def is_create_from_url_active(self):
        with allure.step("Проверка активности кнопки создания проекта по URL"):
            return self.actions.is_element_presents(self.create_from_url_selector)

    def is_create_manually_active(self):
        with allure.step("Проверка активности кнопки создания проекта мануально"):
            return self.actions.is_element_presents(self.create_manually_selector)


class CreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.create_project_button = "input.submitButton"

    def input_project_details(self, name, project_id, description):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            self.actions.input_text(self.project_id_selector, project_id)
            self.actions.input_text(self.project_description_selector, description)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания проекта"):
            self.actions.click_button(self.create_project_button)


class ProjectCreationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu'
                         '&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)
        self.message_project_created = "#message_projectCreated"
        self.error_name_selector = '#errorName'
        self.error_id_selector = '#errorExternalId'

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project(self, name, project_id, description):
        self.go_to_creation_page()
        self.menu_list_create.click_create_manually()
        self.create_form_container.input_project_details(name, project_id, description)
        self.create_form_container.click_create_button()
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.actions.wait_for_url_change(self.page_url, timeout=60000)

    def create_project_with_empty_name(self, project_id):
        self.go_to_creation_page()
        self.menu_list_create.click_create_manually()
        self.create_form_container.input_project_details('', project_id, '')
        self.create_form_container.click_create_button()
        self.actions.assert_text_in_element(self.error_name_selector, 'Project name is empty')

    def create_project_with_empty_id(self, project_name):
        self.go_to_creation_page()
        self.menu_list_create.click_create_manually()
        self.create_form_container.input_project_details(project_name, '', '')
        self.create_form_container.click_create_button()
        self.actions.assert_text_in_element(self.error_id_selector, 'Project ID must not be empty.')

    def create_project_with_nonlatin_id(self, project_name, project_id):
        self.go_to_creation_page()
        self.menu_list_create.click_create_manually()
        self.create_form_container.input_project_details(project_name, project_id, '')
        self.create_form_container.click_create_button()
        self.actions.assert_text_in_element(self.error_id_selector,
                                            f"""Project ID \"{project_id}\" is invalid: contains non-latin letter
                                            '{project_id[0]}'. ID should start with a latin letter and contain only
                                            latin letters, digits and underscores (at most 225 characters).""")
