# routers/tools.py
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

import schemas
import database
import crud

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(database.get_db)):
    # Вызываем нашу новую функцию из crud.py
    result = crud.issue_tool(
        db=db,
        user_id=issue.user_id,
        tool_id=issue.tool_id,
        quantity=issue.quantity
    )
    return result
