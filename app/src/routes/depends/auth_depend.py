from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.src.domain.schemas.auth.jwt_payload import JWTPayload
from app.src.infra.fastapi_config.app import app
from app.src.infra.fastapi_config.app_state import AppStates, get_app_state
from app.src.infra.auth.jwt_handler import JWTHandler
from app.src.usecases.user.get_user import GetUser
from app.src.infra.exceptions.exceptions import AppBaseException
from app.src.repo.interface.Iuser_repo import IUserRepo
from .user_repo_depend import get_user_repo

schema = OAuth2PasswordBearer(tokenUrl="/api_v1/user/login")

def get_jwt_handler() -> JWTHandler:
    
    secret = get_app_state(app, AppStates.JWT_SECRET)
    algorithm = get_app_state(app, AppStates.JWT_ALGORITHM)
    jwt_expiration_minutes = get_app_state(app, AppStates.JWT_EXPIRATION_MINUTES)
    
    jwt_handler = JWTHandler(secret, algorithm, jwt_expiration_minutes)
    
    return jwt_handler

async def get_authenticated_token_payload(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    token: str = Depends(schema),
    user_repo: IUserRepo = Depends(get_user_repo),
) -> JWTPayload:
    
    try:
        payload = jwt_handler.decode_jwt_token(token)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
    
    if jwt_handler.is_token_valid(payload.model_dump()):
        get_user_usecase = GetUser(user_repo)
        user = await get_user_usecase.execute(payload.user_id)
        if user:
            return payload
        
        raise HTTPException(status_code=404, detail="User not found")
    
    raise HTTPException(status_code=401, detail="Token expired") 