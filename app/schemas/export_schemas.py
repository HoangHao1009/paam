from pydantic import BaseModel
from typing import List

class ExportSettingSchema(BaseModel):
    control_vars: List[str]
    target_vars: List[str]
    deep_vars: List[str]