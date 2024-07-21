from pydantic import BaseModel

class ToDoItemBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class ToDoItemCreate(ToDoItemBase):
    pass

class ToDoItemUpdate(ToDoItemBase):
    pass

class ToDoItem(ToDoItemBase):
    id: int

    class Config:
        orm_mode = True
