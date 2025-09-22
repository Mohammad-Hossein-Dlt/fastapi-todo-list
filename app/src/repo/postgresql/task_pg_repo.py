from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.infra.db.postgresql.models.task_db_model import TaskDBModel

class TaskPgRepo(ITaskRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def insert_task(
        self,
        task: TaskModel,
    ) -> TaskModel | None:
    
        new_task = TaskDBModel(**task.model_dump(exclude_none=True))
        
        self.db.add(new_task)
        self.db.commit()
        
        return TaskModel.model_validate(new_task, from_attributes=True)
    
    async def get_all_user_tasks(
        self,
        user_id: str,
    ) ->  list[TaskModel] | None:
        
        tasks = self.db.query(
            TaskDBModel   
        ).where(
            TaskDBModel.user_id == user_id,
        ).all()
    
        return [ TaskModel.model_validate(t, from_attributes=True) for t in tasks ]
    
    async def get_task_by_id(
        self,
        task_id: str,
        user_id: str,
    ) ->  TaskModel | None:
    
        task = self.db.query(
            TaskDBModel   
        ).where(
            and_(
                TaskDBModel.id == task_id,
                TaskDBModel.user_id == user_id,
            ),
        ).first()
        
        if not task:
            return None
        
        return TaskModel.model_validate(task, from_attributes=True)
    
    async def update_task(
        self,
        task: TaskModel,
    ) ->  TaskModel | None:
        
        update_task = self.db.query(
            TaskDBModel   
        ).where(
            and_(
                TaskDBModel.id == task.id,
                TaskDBModel.user_id == task.user_id,
            ),
        ).update(
            task.model_dump(exclude_none=True, exclude_unset=True),
            synchronize_session='fetch',
        )
        
        self.db.commit()
                
        if not update_task:
            return None
        
        return await self.get_task_by_id(task.id, task.user_id)
        
    
    async def delete_task(
        self,
        task_id: str,
        user_id: str,
    ) -> bool:
        
        task = await self.get_task_by_id(task_id, user_id)
        
        if task:
            task = self.db.merge(TaskDBModel(**task.model_dump()))
            
        if isinstance(task, TaskDBModel):
            self.db.delete(task)
            self.db.commit()
            return True
        
        return False