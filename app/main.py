from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.ToDoItem)
def create_item(item: schemas.ToDoItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/{item_id}", response_model=schemas.ToDoItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[schemas.ToDoItem])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.put("/items/{item_id}", response_model=schemas.ToDoItem)
def update_item(item_id: int, item: schemas.ToDoItemUpdate, db: Session = Depends(get_db)):
    return crud.update_item(db=db, item_id=item_id, item=item)

@app.delete("/items/{item_id}", response_model=schemas.ToDoItem)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db=db, item_id=item_id)
