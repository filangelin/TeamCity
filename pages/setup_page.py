from pages.base_page import BasePage


class FirstStartsWindow(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.proceed_button_selector = "input#proceedButton"

    def proceed_step(self):
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.proceed_button_selector, timeout=60000)
        self.actions.click_button(self.proceed_button_selector)


class Loading(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def wait_loading(self):
        self.actions.wait_for_page_load()


class Agreement(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/showAgreement.html"
        self.checkbox_selector = "input#accept"
        self.continue_button_selector = "checkbox_selector"

    def check_in_box(self):
        self.actions.wait_for_selector(self.checkbox_selector, timeout=60000)
        self.actions.check_in_box(self.checkbox_selector)

    def continue_agreement(self):
        self.actions.is_button_active(self.continue_button_selector)
        self.actions.click_button(self.continue_button_selector)
        self.actions.wait_for_page_load()


class SetupUser(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_selector = "input#input_teamcityUsername"
        self.password_selector = "input#password1"
        self.password_confirm_selector = "input#retypedPassword"
        self.create_account_button_selector = "input[type='Submit']"
        self.page_url_after_creating = "/favorite/projects"

    def fill_user_data(self, username, password):
        self.actions.input_text(self.username_selector, username)
        self.actions.input_text(self.password_selector, password)
        self.actions.input_text(self.password_confirm_selector, password)

    def create_admin(self):
        self.actions.click_button(self.create_account_button_selector)
        self.actions.wait_for_page_load()
        self.actions.wait_for_url_change(self.page_url_after_creating)


class SetupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = f"/mnt"
        self.first_starts_window = FirstStartsWindow(self.page)
        self.loading = Loading(self.page)
        self.agreement = Agreement(self.page)
        self.setup_user = SetupUser(self.page)

    def set_up(self, username="admin", password="admin"):
        self.actions.navigate(self.page_url)
        self.actions.wait_for_page_load()
        self.first_starts_window.proceed_step()
        self.loading.wait_loading()
        self.first_starts_window.proceed_step()
        self.agreement.check_in_box()
        self.actions.check_url(self.agreement.page_url)
        self.agreement.continue_agreement()
        self.actions.wait_for_page_load()
        self.setup_user.fill_user_data(username, password)
        self.setup_user.create_admin()
