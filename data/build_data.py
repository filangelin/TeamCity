from pydantic import BaseModel, ConfigDict, validator

from utils.datagenerator import DataGenerator
from typing import Optional, List, Dict


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


class PropertyModel(BaseModel):
    name: str
    value: str


class Templates(BaseModel):
    count: int
    buildType: list


class Property(BaseModel):
    name: str
    value: str


class Settings(BaseModel):
    property: Optional[List[Property]] = None
    count: int


class Parameters(BaseModel):
    property: list
    count: int
    href: str


class VcsRootEntries(BaseModel):
    count: int
    vcs_root_entry: list


class Counter(BaseModel):
    count: int


class Href(BaseModel):
    href: str


class StepProperty(BaseModel):
    name: str
    value: str


class StepProperties(BaseModel):
    property: List[StepProperty]
    count: int


class Step(BaseModel):
    id: str
    name: str
    type: str
    properties: StepProperties


class Steps(BaseModel):
    count: int
    steps: Optional[Step] = None

class BuildResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str
    project: ProjectModel
    templates: Optional[Templates] = None
    vcs_root_entries: Optional[VcsRootEntries] = None
    settings: Optional[Settings] = None
    parameters: Optional[Parameters] = None
    steps: Steps
    features: Optional[Counter] = None
    triggers: Optional[Counter] = None
    snapshot_dependencies: Optional[Counter] = None
    artifact_dependencies: Optional[Counter] = None
    agent_requirements: Optional[Counter] = None
    builds: Optional[Href] = None
    investigations: Optional[Href] = None
    compatibleAgents: Optional[Href] = None
    compatibleCloudImages: Optional[dict] = None


class BuildTypeItem(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str


class LocatedBuildsModel(BaseModel):
    count: int
    href: str
    buildType: List[BuildTypeItem]
