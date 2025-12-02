from pydantic import BaseModel,field_validator
from typing import List
import re
#数据模型
class EcoModel(BaseModel):
    text: str
    author: str
    tags: List[str]

    # --- 清洗规则示例 ---
    @field_validator("text")
    def remove_smart_quotes(cls, v):
        return v.replace("“", '"').replace("”", '"')

    @field_validator("author")
    def capitalize(cls, v):
        return v.strip().title()

    @field_validator("tags")
    def lowercase_tags(cls, v):
        return [t.strip().lower() for t in v if t.strip()]