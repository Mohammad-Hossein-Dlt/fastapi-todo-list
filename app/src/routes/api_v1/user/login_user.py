from ._router import router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.src.routes.http_response.responses import ResponseMessage
from app.src.models.schemas.user.login_user_input import LoginUserInput
from app.src.usecases.user.login_user import LoginUser
from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.routes.depends.user_repo_depend import get_user_repo
from app.src.infra.auth.jwt_handler import JWTHandler
from app.src.routes.depends.auth_depend import get_jwt_handler
from app.src.infra.exceptions.exceptions import AppBaseException


@router.post(
    "/login",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def get_user_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: IUserRepo = Depends(get_user_repo),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
):
    try:
        login_user_usecase = LoginUser(user_repo, jwt_handler)
        return await login_user_usecase.execute(LoginUserInput(username=form_data.username, password=form_data.password))
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
