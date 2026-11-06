from sqlalchemy.orm import Session, selectinload, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func
from fastapi.exceptions import HTTPException
from typing import List
import models
import schemas

def get_tool(db: Session, tool_id: int):
    return db.query(models.Tool).filter(models.Tool.id == tool_id).first()

def get_tools(db: Session, skip: int = 0, search_d: str = "", search_type: str = "", search_name: str = ""):
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

    return query.offset(skip).all()

def create_tool(db: Session, tool: schemas.ToolCreate):
    # Преобразуем Pydantic-модель в словарь
    tool_data = tool.model_dump()

    # Если ссылка передана, превращаем объект Url в обычную строку
    if tool_data.get("manufacturer_url"):
        tool_data["manufacturer_url"] = str(tool_data["manufacturer_url"])

    db_tool = models.Tool(**tool_data)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)

    return db_tool

def update_tool(db: Session, tool_id: int, tool_update: schemas.ToolUpdate):
    db_tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not db_tool:
        return None

    # ИСПРАВЛЕНИЕ:
    tool_data = tool_update.model_dump(mode='json', exclude_unset=True)

    for var, value in tool_data.items():
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

#---User---
def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreat):
    # Преобразуем Pydantic-модель в словарь
    user_data = user.model_dump()

    db_user = models.User(**user_data)
    db.add(db_user)
    try:
        db.commit()
        #db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с такими данными уже существует")

    return db_user


def delete_user(db: Session, user_id: int):
    # Ищем пользователя
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return False

    # Удаляем и фиксируем транзакцию
    db.delete(user)
    db.commit()
    return True

#---issue---
def issue_tool(db: Session, user_id: int, tool_id: int, quantity: int):
    # Используем joinedload, чтобы сразу загрузить данные инструмента и избежать лишних запросов
    db_tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()

    if not db_tool:
        raise HTTPException(status_code=404, detail="Инструмент не найден")

    if db_tool.Kol < quantity:
        raise HTTPException(status_code=400, detail=f"Недостаточно инструмента на складе. В наличии: {db_tool.Kol}")

    try:
        # 1. Вычитаем количество (атомарная операция)
        db_tool.Kol -= quantity

        # 2. Создаем запись в истории
        history_entry = models.HistoryTool(
            user_id=user_id,
            tool_id=tool_id,
            quantity=quantity
        )
        db.add(history_entry)

        # 3. Обновляем данные инструмента в сессии
        db.add(db_tool)

        # 4. Фиксируем транзакцию
        db.commit()
        db.refresh(db_tool)

        return {"detail": "success", "tool_name": db_tool.Name, "remaining": db_tool.Kol}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

#---history---
def get_history_list(
    db: Session,
    *,
    search_user: str | None = None,
    search_tool: str | None = None
) -> List[schemas.HistoryItem]:

    # 1. Базовый запрос с eager loading (загружаем связи для отображения)
    query = db.query(models.HistoryTool).options(
        selectinload(models.HistoryTool.user),
        selectinload(models.HistoryTool.tool)
    )

    # 2. Фильтрация (добавляем JOIN только если ищем)
    if search_user:
        search_term = f"%{search_user.lower()}%"
        # Явно говорим SQLAlchemy сделать JOIN для фильтрации
        query = query.join(models.HistoryTool.user).filter(
            or_(
                func.lower(models.User.surname).ilike(search_term),
                func.lower(models.User.name).ilike(search_term),
            )
        )

    if search_tool:
        search_term = f"%{search_tool.lower()}%"
        query = query.join(models.HistoryTool.tool).filter(
            func.lower(models.Tool.name).ilike(search_term)
        )

    history_items_db = query.all()

    # 3. Преобразование (теперь item.user и item.tool НЕ None)
    result: List[schemas.HistoryItem] = []
    for item in history_items_db:
        # Защита на случай, если в БД все же NULL (хотя join его не вернет)

        # Формируем ФИО: Фамилия + Имя (защита от None в БД)
        if item.user:
            user_fio_string = " ".join([item.user.name, item.user.surname])
        else:
            user_fio_string = "[Нет пользователя]"

        # Формируем название инструмента
        if item.tool:
            tool_name_string = item.tool.Name
        else:
            tool_name_string = "[Инструмент удален]"

        result.append(schemas.HistoryItem(
            id=item.id,
            issue_date=item.issue_date,
            user_fio=user_fio_string,
            tool_name=tool_name_string,
            quantity=item.quantity
        ))

    return result