from fastapi import FastAPI, Request, Response

from .auth import routers as auth_routers
from .database import SessionLocal
from .users import routers as users_routers

app = FastAPI()
app.include_router(auth_routers.router)
app.include_router(users_routers.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {"message": "We are online"}
