from app.src.repo.interface.Itask_repo import ITaskRepo
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.infra.db.mongodb.collections.task_collection import TaskCollection
from bson.objectid import ObjectId
from beanie.operators import And

class TaskMongodbRepo(ITaskRepo):
        
    async def insert_task(
        self,
        task: TaskModel,
    ) -> TaskModel | None:
                    
        new_task = await TaskCollection.insert(
            TaskCollection(**task.model_dump(exclude={"id"})),
        )
        
        if not new_task:
            return None
                
        return TaskModel.model_validate(new_task, from_attributes=True)
    
    async def get_all_user_tasks(
        self,
        user_id: str,
    ) ->  list[TaskModel] | None:
        
        tasks = await TaskCollection.find(
            TaskCollection.user_id == ObjectId(user_id),
        ).to_list()
        
        if not tasks:
            return []
    
        return [ TaskModel.model_validate(t, from_attributes=True) for t in tasks ]
    
    async def get_task_by_id(
        self,
        task_id: str,
        user_id: str,
    ) ->  TaskModel | None:
    
        task = await TaskCollection.find_one(
            TaskCollection.id == ObjectId(task_id),
            TaskCollection.user_id == ObjectId(user_id),
        )
        
        if not task:
            return None
        
        return TaskModel.model_validate(task, from_attributes=True)
    
    async def update_task(
        self,
        task: TaskModel,
    ) ->  TaskModel | None:
                
        update_task = await TaskCollection.find_one(
            And(
                TaskCollection.id == ObjectId(task.id),
                TaskCollection.user_id == ObjectId(task.user_id),
            )
        ).update(
            {
                "$set": task.model_dump(exclude_unset=True, exclude_none=True, exclude={"id", "user_id"}),
            },
        )
                
        if update_task.matched_count == 0:
            return None
        
        return await self.get_task_by_id(task.id, task.user_id)
        
    
    async def delete_task(
        self,
        task_id: str,
        user_id: str,
    ) -> bool:
        
        task = TaskCollection.find(
            TaskCollection.id == ObjectId(task_id),
            TaskCollection.user_id == ObjectId(user_id),
        )                
        
        delete_task = await task.delete()
        
        return bool(delete_task.deleted_count)