from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class BuildAPI(CustomRequester):

    def create_build(self, build_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_data, expected_status_code=expected_status)

    def check_build(self, build_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildTypes/id:{build_id}", expected_status_code=expected_status)

    def run_build(self, build_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildQueue", data=build_data, expected_status_code=expected_status)

    def check_runned_build(self, build_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildQueue?locator=buildType(id:{build_id})",
                                 expected_status_code=expected_status)

    def delete_build(self, build_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/buildTypes/{build_id}", expected_status_code=expected_status)

    def locate_builds_of_project(self, project_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildTypes?locator=project:{project_id}", expected_status_code=expected_status)


