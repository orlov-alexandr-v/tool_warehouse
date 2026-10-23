import os
import sys
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Настройка путей (если скрипт лежит в подпапке)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import schemas
import database

def insert_tools_from_list(tools_list: list[dict]):
    """
    Принимает список словарей, валидирует их через Pydantic
    и вставляет в таблицу tools.
    """
    if not tools_list:
        print("Список инструментов пуст. Нечего вставлять.")
        return

    # Собираем список объектов SQLAlchemy
    db_tools_to_add = []

    for tool_dict in tools_list:
        try:
            # 1. Валидация каждого словаря через Pydantic
            # Это гарантирует, что в БД не попадут некорректные данные
            tool_data = schemas.ToolCreate(**tool_dict)

            # 2. Создание объекта SQLAlchemy из валидированного словаря
            db_tool = models.Tool(**tool_data.dict())
            db_tools_to_add.append(db_tool)

        except Exception as e:
            # Если один словарь в списке битый, мы его пропустим и пойдем дальше
            print(f"Пропущен некорректный инструмент {tool_dict.get('Name', 'без имени')}: {e}")
            continue

    if not db_tools_to_add:
        print("Ни один инструмент не прошел валидацию.")
        return

    # Подключаемся к БД
    db: Session = database.SessionLocal()

    try:
        # 3. Добавляем ВЕСЬ список объектов одной командой
        db.add_all(db_tools_to_add)

        # 4. Один commit на весь список (быстро и надежно)
        db.commit()

        # 5. Обновляем объекты, чтобы получить их ID (опционально, если нужно работать с ними дальше)
        for tool in db_tools_to_add:
            db.refresh(tool)

        print(f"Успешно добавлено {len(db_tools_to_add)} инструментов.")

        # Выводим ID добавленных записей для проверки
        #added_ids = [tool.id for tool in db_tools_to_add]
        #print(f"ID добавленных записей: {added_ids}")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Ошибка базы данных при массовой вставке: {e}")
    except Exception as e:
        db.rollback()
        print(f"Непредвиденная ошибка: {e}")
    finally:
        db.close()

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---

if __name__ == "__main__":
    # Список словарей для вставки
    df = pd.read_excel(r"BASA/main.xlsx", dtype=str)

    tools_to_import = []

    for v in df.to_dict(orient='records'):
        tools_to_import.append(dict(v))

    insert_tools_from_list(tools_to_import)