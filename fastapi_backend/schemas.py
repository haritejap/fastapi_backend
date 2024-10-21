from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserRegistration(BaseModel):
    first_name : str
    last_name : str
    email : str
    mobile_no : int
    year_of_study : int
    branch : int
    dob : date
    admission_date : date
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True