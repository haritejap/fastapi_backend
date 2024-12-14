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
    user_type : str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class GetProfileData(BaseModel):
    student_id : str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PostUserRegistration(BaseModel):
    student_id : str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class LoginForUser(BaseModel):
    user_login_type : str
    user_name : str
    password : str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ImageData(BaseModel):
    image : str
    reg_number : str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class fileData(BaseModel):
    file : str
    subject_id : str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True