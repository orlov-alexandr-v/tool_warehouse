from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import models
import schemas

def get_tool(db: Session, tool_id: int):
    return db.query(models.Tool).filter(models.Tool.id == tool_id).first()

def get_tools(db: Session, skip: int = 0, limit: int = 10, search_d: str = None, search_type: str = None, search_name: str = None):
    query = db.query(models.Tool)

    # Поиск (регистронезависимый, частичное совпадение)
    if search_d or search_type or search_name:
        conditions = []
        if search_d:
            conditions.append(models.Tool.D.ilike(f"%{search_d}%"))
        if search_type:
            conditions.append(models.Tool.Type.ilike(f"%{search_type}%"))
        if search_name:
            conditions.append(models.Tool.Name.ilike(f"%{search_name}%"))
        query = query.filter(or_(*conditions))

    return query.offset(skip).limit(limit).all()

def create_tool(db: Session, tool: schemas.ToolCreate):
    db_tool = models.Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def update_tool(db: Session, tool_id: int, tool_update: schemas.ToolUpdate):
    db_tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not db_tool:
        return None
    for var, value in tool_update.model_dump(exclude_unset=True).items():
        setattr(db_tool, var, value)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def delete_tool(db: Session, tool_id: int):
    db_tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not db_tool:
        return None
    db.delete(db_tool)
    db.commit()
    return db_tool