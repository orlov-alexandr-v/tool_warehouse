# routers/__init__.py
from .tools import router as tools_router

# Если у вас есть роутер пользователей
# from .users import router as users_router

__all__ = ["tools_router"]