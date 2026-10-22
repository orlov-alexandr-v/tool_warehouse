# -*- coding: utf-8 -*-

from . import database, models, schemas
from sqlalchemy.orm import Session

def init():
    models.Base.metadata.create_all(bind=database.engine)
    db: Session = database.SessionLocal()

    if db.query(models.Tool).first():
        print("База данных уже содержит данные. Инициализация пропущена.")
        db.close()
        return

    tools_data = [
        {"Type": "Сверло", "Name": "HSS-G DIN338", "D": "5.0", "L": "86", "Kol": 50},
        {"Type": "Фреза", "Name": "Концевая", "D": "12.0", "S": "4", "Kol": 10},
        {"Type": "Метчик", "Name": "М8", "D": "8.0", "Kol": 25},
        {"Type": "Развертка", "Name": "Ручная", "D": "10.0", "Kol": 5},
    ]

    for tool in tools_data:
        db_tool = models.Tool(**tool)
        db.add(db_tool)

    db.commit()
    db.close()
    print("База данных инициализирована.")

if __name__ == "__main__":
    init()