from typing import List
from pydantic import BaseModel
from datetime import datetime as datetime_type


class Asset(BaseModel):
    id: int
    user_id: int
    datetime: datetime_type
    uri: str
    is_video: bool

class Assets: List[Asset]
