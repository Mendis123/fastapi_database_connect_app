from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=1, le=80)
    email: EmailStr

class UserUpdate(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr

class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(validation_alias='id')
    name: str
    age: int
    email: EmailStr