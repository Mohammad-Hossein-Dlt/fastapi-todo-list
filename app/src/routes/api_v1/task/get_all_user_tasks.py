from ._router import router
from fastapi import Depends, HTTPException
from app.src.routes.http_response.responses import ResponseMessage
from app.src.usecases.task.get_all_user_tasks import GetAllUserTasks
from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.routes.depends.task_repo_depend import get_task_repo
from app.src.routes.depends.auth_depend import get_authenticated_token_payload
from app.src.domain.schemas.auth.jwt_payload import JWTPayload
from app.src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get-all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_user_tasks(
    task_repo: ITaskRepo = Depends(get_task_repo),
    user: JWTPayload = Depends(get_authenticated_token_payload)
):
    try:
        get_all_user_tasks_usecase = GetAllUserTasks(task_repo)
        return await get_all_user_tasks_usecase.execute(user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
