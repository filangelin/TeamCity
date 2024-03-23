import pytest

from pages.setup_page import SetupPage


@pytest.mark.parametrize("browser", ['chromium'], indirect=True)
def test_set_up(browser):
    page = SetupPage(browser)
    page.set_up()
