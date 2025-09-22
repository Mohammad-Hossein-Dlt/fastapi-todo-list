from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.infra.exceptions.exceptions import OperationFailureException

class GetAllUserTasks:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo  
    
    async def execute(
        self,
        user_id: str,
    ) -> list[TaskModel]:
        
        try:
            tasks: list[TaskModel] = await self.task_repo.get_all_user_tasks(user_id)
            return tasks
        except:
            raise OperationFailureException(500, "Internal server error")  