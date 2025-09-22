from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.infra.exceptions.exceptions import OperationFailureException

class GetTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo  
    
    async def execute(
        self,
        task_id: str,
        user_id: str,
    ) -> TaskModel:
        
        try:
            task: TaskModel = await self.task_repo.get_task_by_id(task_id, user_id)
            return task.model_dump(mode="json") if task else None
        except:
            raise OperationFailureException(500, "Internal server error")