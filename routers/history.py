from fastapi import Depends, APIRouter, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session

import schemas
import database
import crud

router = APIRouter()

@router.get("/history/", response_model=List[schemas.HistoryItem])
def read_history(
    db: Session = Depends(database.get_db),
    search_user: str | None = Query(None, alias="search_user"),
    search_tool: str | None = Query(None, alias="search_tool")
):
    """
    Возвращает список выдачи инструментов.
    Фильтрация на бэкенде, сортировка и пагинация — на фронтенде.
    """
    history = crud.get_history_list(
        db=db,
        search_user=search_user,
        search_tool=search_tool
    )
    return history

@router.delete("/history/{historyId}/")
def delete_hystor(historyId: int, db: Session = Depends(database.get_db)):
    history = crud.delete_history(db, history_id=historyId);

    if history is None:
            raise HTTPException(status_code=404, detail="history not found")
    
    return history
