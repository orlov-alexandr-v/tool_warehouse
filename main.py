import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import tools, users, issue

app = FastAPI(title="Tool Warehouse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["authorization", "content-type"],
)

app.include_router(tools.router, prefix="/tools", tags=[""])
app.include_router(users.router, prefix="/users", tags=[""])
app.include_router(issue.router, prefix="/issue", tags=[""])

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
