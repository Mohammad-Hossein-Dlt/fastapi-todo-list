from ._router import router
from fastapi import Depends, HTTPException
from app.src.routes.http_response.responses import ResponseMessage
from app.src.models.schemas.user.create_user_input import CreateUserInput
from app.src.usecases.user.create_user import CreateUser
from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.routes.depends.user_repo_depend import get_user_repo
from app.src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/register-me",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_user(
    user_data: CreateUserInput = Depends(CreateUserInput),
    user_repo: IUserRepo = Depends(get_user_repo),
):
    try:
        create_user_usecase = CreateUser(user_repo)
        return await create_user_usecase.execute(user_data)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
