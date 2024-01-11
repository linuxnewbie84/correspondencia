from pydantic import BaseModel, Field
from typing import Optional

class Doc_Schema(BaseModel):
    id:Optional[int] = None
    