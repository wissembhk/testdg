from fastapi import APIRouter, FastAPI
from utils.database import create_db
from routers import AlertRoute as AlertRoute

app = FastAPI()
router = APIRouter(prefix="/api")

create_db()
router.include_router(AlertRoute.router)
app.include_router(router)
