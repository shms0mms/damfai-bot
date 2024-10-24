import datetime
from pydantic import BaseModel, EmailStr, field_validator

from ..themes.themes_schema import ShowTheme

from .auth_models import Role


class LoginUser(BaseModel):
    
    email: EmailStr
    
    password: str   
    
class RegisterUser(BaseModel):
        
    email: EmailStr
    
    name:str
    surname:str
    
    dob:datetime.date


    role: Role | None
    password: str | bytes 
    
    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class ShowUser(BaseModel):
    
    id:int
    role: Role
    name:str
    surname:str
    email: EmailStr
    
    created_at:datetime.datetime
    dob:datetime.date



class ShowUserWithToken(BaseModel):
    

    email: EmailStr
    name:str
    surname:str
    
    dob:datetime.date

    token:str




class UpdateUser(BaseModel):

    name:str | None
    surname:str | None

    email: EmailStr | None  


    password:str | bytes | None
    
    