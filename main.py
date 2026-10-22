from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
import database


app = FastAPI(title="Tool Warehouse API")

# Добавьте эти строки перед определением маршрутов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любого источника (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы при старте, если их нет
models.Base.metadata.create_all(bind=database.engine)

@app.post("/tools/", response_model=schemas.Tool)
def create_new_tool(tool: schemas.ToolCreate, db: Session = Depends(database.get_db)):
    return crud.create_tool(db=db, tool=tool)

@app.get("/tools/", response_model=List[schemas.Tool])
def read_tools(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search_d: str = Query(None, description="Search by Diameter (D)"),
    search_type: str = Query(None, description="Search by Type"),
    search_name: str = Query(None, description="Search by Name"),
    db: Session = Depends(database.get_db)
):
    tools = crud.get_tools(db, skip=skip, limit=limit, search_d=search_d, search_type=search_type, search_name=search_name)
    return tools

@app.get("/tools/{tool_id}", response_model=schemas.Tool)
def read_tool(tool_id: int, db: Session = Depends(database.get_db)):
    db_tool = crud.get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool

@app.put("/tools/{tool_id}", response_model=schemas.Tool)
def update_existing_tool(tool_id: int, tool_update: schemas.ToolUpdate, db: Session = Depends(database.get_db)):
    db_tool = crud.update_tool(db, tool_id=tool_id, tool_update=tool_update)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool

@app.delete("/tools/{tool_id}", response_model=schemas.Tool)
def delete_existing_tool(tool_id: int, db: Session = Depends(database.get_db)):
    db_tool = crud.delete_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool

app.mount("/", StaticFiles(directory="static", html=True), name="static")
