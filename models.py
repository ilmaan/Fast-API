from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class Gender(str, Enum):
    male="male"
    female="female"

class Role(str, Enum):
    admin="admin"
    user="user"



class User(BaseModel):
    id: Optional[UUID]
    fname: str
    lname: str
    gender: Gender
    roles: List[Role]
