import allure

from enums.host import PROJECT_MANAGEMENT, PROJECT_MANAGEMENT_ROOT
from pages.base_page import BasePage


class MenuListActions(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.delete_project_selector = "[title='Delete project']"
        self.links = ProjectManagerFragment(page)

    def click_on_delete_project(self):
        with allure.step("Нажатие на кнопку удаления проекта"):
            self.links.expand_list_actions()
            self.actions.click_button(self.delete_project_selector)


class ProjectManagerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button_selector = "[data-hint-container-id='project-admin-actions']"

    def expand_list_actions(self):
        with allure.step("Нажатие на кнопку Actions"):
            self.actions.click_button(self.actions_button_selector)


class ProjectManagementPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = PROJECT_MANAGEMENT
        self.menu_list_actions = MenuListActions(page)

    def go_to_project_management_page(self, project_id):
        with allure.step("Переход на страницу управления проектом"):
            self.actions.navigate(self.page_url.format(project_id=project_id))
            self.actions.wait_for_page_load()

    def delete_project(self, project_id):
        self.go_to_project_management_page(project_id)
        self.menu_list_actions.click_on_delete_project()
        self.page_url = PROJECT_MANAGEMENT_ROOT
        self.actions.wait_for_url_change(self.page_url, timeout=60000)
