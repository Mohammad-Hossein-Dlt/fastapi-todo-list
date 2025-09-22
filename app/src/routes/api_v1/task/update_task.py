from ._router import router
from fastapi import Query, Depends, HTTPException
from app.src.routes.http_response.responses import ResponseMessage
from app.src.models.schemas.task.update_task_input import UpdateTaskInput
from app.src.usecases.task.update_task import UpdateTask
from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.routes.depends.task_repo_depend import get_task_repo
from app.src.routes.depends.auth_depend import get_authenticated_token_payload
from app.src.domain.schemas.auth.jwt_payload import JWTPayload
from app.src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_task(
    task: UpdateTaskInput = Query(None),
    task_repo: ITaskRepo = Depends(get_task_repo),
    user: JWTPayload = Depends(get_authenticated_token_payload),
):
    try:
        update_task_usecase = UpdateTask(task_repo)
        return await update_task_usecase.execute(task, user.user_id)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
