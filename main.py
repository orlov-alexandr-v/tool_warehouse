# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

# Используем абсолютный импорт
import routers

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Tool Warehouse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["authorization", "content-type"],
)

app.include_router(routers.tools.router, prefix="/tools", tags=[""])

app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
