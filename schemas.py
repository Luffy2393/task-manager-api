from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

