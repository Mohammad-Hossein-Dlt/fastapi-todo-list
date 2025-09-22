from app.src.repo.interface.Itask_repo import ITaskRepo
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from app.src.infra.fastapi_config.app import app
from app.src.infra.fastapi_config.app_state import AppStates, get_app_state
from app.src.repo.postgresql.task_pg_repo import TaskPgRepo
from app.src.repo.mongodb.task_mongodb_repo import TaskMongodbRepo

def get_task_repo() -> ITaskRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    if isinstance(db_client, Session):
        return TaskPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return TaskMongodbRepo()