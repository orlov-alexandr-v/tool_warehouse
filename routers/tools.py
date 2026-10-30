# routers/tools.py
from fastapi import Depends, HTTPException, Query, APIRouter
from typing import List
from sqlalchemy.orm import Session

import schemas
import database
import crud

router = APIRouter(prefix="")

@router.post("/", response_model=schemas.Tool)
def create_new_tool(tool: schemas.ToolCreate, db: Session = Depends(database.get_db)):

    return crud.create_tool(db=db, tool=tool)


@router.get("/", response_model=List[schemas.Tool])
def read_tools(
    skip: int = Query(0, ge=0),
    limit: int = Query(4, ge=1, le=100),
    search_d: str = Query(None, description="Search by Diameter (D)"),
    search_type: str = Query(None, description="Search by Type"),
    search_name: str = Query(None, description="Search by Name"),
    db: Session = Depends(database.get_db)
):
    tools = crud.get_tools(db, skip=skip, search_d=search_d, search_type=search_type, search_name=search_name)

    return tools


@router.get("/{tool_id}", response_model=schemas.Tool)
def read_tool(tool_id: int, db: Session = Depends(database.get_db)):
    db_tool = crud.get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    return db_tool


@router.put("/{tool_id}", response_model=schemas.Tool)
def update_existing_tool(tool_id: int, tool_update: schemas.ToolUpdate, db: Session = Depends(database.get_db)):
    db_tool = crud.update_tool(db, tool_id=tool_id, tool_update=tool_update)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    return db_tool


@router.delete("/{tool_id}", response_model=schemas.Tool)
def delete_existing_tool(tool_id: int, db: Session = Depends(database.get_db)):
    db_tool = crud.delete_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    return db_tool