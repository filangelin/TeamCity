from pydantic import BaseModel

from utils.datagenerator import DataGenerator


class BuildDataModel(BaseModel):
    id: str
    name: str
    project: object
    steps: object


class BuildData:
    @staticmethod
    def create_build_data(project_id) -> BuildDataModel:
        return BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name="BuildConfName",
            project={
                "id": project_id
            },
            steps={
                "step":
                    [
                        {
                            "name": "myCommandLineStep",
                            "type": "simpleRunner",
                            "properties": {
                                "property": [
                                    {
                                        "name": "script.content",
                                        "value": "echo 'Hello World!'"
                                    },
                                    {
                                        "name": "teamcity.step.mode",
                                        "value": "default"
                                    },
                                    {
                                        "name": "use.custom.script",
                                        "value": "true"
                                    }
                                ]
                            }
                        }
                    ]
            }

        )


class ProjectModel(BaseModel):
    id: str


class StepModel(BaseModel):
    name: str
    type: str
    properties: object


class StepsModel(BaseModel):
    step: list[StepModel]


class PropertyModel(BaseModel):
    name: str
    value: str


class PropertiesModel(BaseModel):
    property: list[PropertyModel]
