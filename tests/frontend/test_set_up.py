from pages.setup_page import SetupPage


def test_set_up(browser):
    page = SetupPage(browser)
    page.set_up()
