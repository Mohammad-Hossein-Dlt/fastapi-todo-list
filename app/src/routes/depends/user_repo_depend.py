from app.src.repo.interface.Iuser_repo import IUserRepo
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from app.src.infra.fastapi_config.app import app
from app.src.infra.fastapi_config.app_state import AppStates, get_app_state
from app.src.repo.postgresql.user_pg_repo import UserPgRepo
from app.src.repo.mongodb.user_mongodb_repo import UserMongodbRepo

def get_user_repo() -> IUserRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    if isinstance(db_client, Session):
        return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return UserMongodbRepo()