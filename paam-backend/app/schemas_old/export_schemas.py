from pydantic import BaseModel
from typing import List

class ExportSettingSchema(BaseModel):
    controlVars: List[str]
    targetVars: List[str]
    deepVars: List[str]