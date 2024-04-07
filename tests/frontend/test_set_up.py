from pages.setup_page import SetupPage


def test_set_up(browser_for_setup):
    page = SetupPage(browser_for_setup)
    page.set_up()
