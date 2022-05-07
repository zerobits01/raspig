from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., example="running", max_length=1024)


class Task(TaskBase):
    id: int = Field(..., gt=0, example=1)
    done: bool = Field(False, description="done task or not")

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    done: bool = Field(False, description="done task or not")

# look at pydantic as serializers, 
# it can parse a dictionary to a class based on some validations
