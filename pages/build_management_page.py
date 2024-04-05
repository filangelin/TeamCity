import allure

from enums.host import BUILD_INFO, REMOVED_BUILD_PAGE
from pages.base_page import BasePage


class MenuListActions(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.delete_build_selector = 'a >> text="Delete..."'
        self.links = BuildManagerFragment(page)

    def click_on_delete_build(self):
        with allure.step("Нажатие на кнопку удаления билда"):
            self.links.expand_list_actions()
            self.page.on("dialog", lambda dialog: dialog.accept())
            self.actions.click_button(self.delete_build_selector)
            self.actions.wait_for_page_load()


class BuildManagerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button_selector = "#btActions"

    def expand_list_actions(self):
        with allure.step("Нажатие на кнопку Actions"):
            self.actions.click_button(self.actions_button_selector)


class BuildManagementPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = BUILD_INFO
        self.edit_button = "[title='Edit build configuration settings']"
        self.menu_list_actions = MenuListActions(page)

    def go_to_build_management_page(self, build_id):
        with allure.step("Переход на страницу управления билдом"):
            self.actions.navigate(self.page_url.format(build_id=build_id))
            self.actions.wait_for_page_load()
            self.actions.click_button(self.edit_button)
            self.actions.wait_for_page_load()

    def delete_build_ui(self, build_id, project_id):
        self.go_to_build_management_page(build_id)
        self.menu_list_actions.click_on_delete_build()
        self.page_url = REMOVED_BUILD_PAGE.format(project_id=project_id)
        self.actions.wait_for_url_change(self.page_url)
