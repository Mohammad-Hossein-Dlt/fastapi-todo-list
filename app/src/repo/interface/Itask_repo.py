from abc import ABC, abstractmethod
from app.src.domain.schemas.task.task_model import TaskModel


class ITaskRepo(ABC):
        
    @abstractmethod
    async def insert_task(
        task: TaskModel,
    ) -> TaskModel | None:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_user_tasks(
        user_id: str,
    ) ->  list[TaskModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_task_by_id(
        task_id: str,
        user_id: str,
    ) ->  TaskModel | None:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_task(
        task: TaskModel,
    ) ->  TaskModel | None:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_task(
        task_id: str,
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError