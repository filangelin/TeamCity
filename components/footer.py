from actions.page_actions import PageAction
from enums.host import BASE_URL


class Footer:
    def __init__(self, actions: PageAction):
        self.actions = actions
        self.container = 'footer#footer'
        self.about_teamcity = 'span >> text="About TeamCity"'
        self.about_teamcity_url = 'https://www.jetbrains.com/teamcity/?fromServer'
        self.license_agreement = 'span >> text="License Agreement"'
        self.license_agreement_url = f'{BASE_URL}/showAgreement.html'

    def go_to_about_teamcity(self):
        self.actions.check_url_in_new_tab(self.about_teamcity, self.about_teamcity_url)

    def go_to_license_agreement(self):
        self.actions.check_url_in_new_tab(self.license_agreement, self.license_agreement_url)
