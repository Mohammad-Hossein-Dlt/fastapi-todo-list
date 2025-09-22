from app.src.models.schemas.task.create_task_input import CreateTaskInput
from app.src.models.schemas.simple.simple_output import SimpleOutput
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.infra.exceptions.exceptions import OperationFailureException

class CreateTask:
    
    def __init__(
        self,
        task_repo: ITaskRepo,
    ):        
        self.task_repo = task_repo
    
    async def execute(
        self,
        task: CreateTaskInput,
        user_id: str,
    ) -> TaskModel:
        
        try:
            task = TaskModel.model_validate(task, from_attributes=True)
            task.user_id = user_id
            task: TaskModel = await self.task_repo.insert_task(task)
            return task.model_dump(mode="json") if task else None
        except:
            raise OperationFailureException(500, "Internal server error")  