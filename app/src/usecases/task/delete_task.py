from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.infra.exceptions.exceptions import OperationFailureException

class DeleteTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo   
    
    async def execute(
        self,
        task_id: str,
        user_id: str,
    ) -> bool:
        
        try:
            return await self.task_repo.delete_task(task_id, user_id)
        except:
            raise OperationFailureException(500, "Internal server error")  