from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.domain.schemas.user.user_model import UserModel
from app.src.infra.db.mongodb.collections.user_collection import UserCollection
from app.src.infra.db.mongodb.collections.task_collection import TaskCollection
from bson.objectid import ObjectId

class UserMongodbRepo(IUserRepo):
            
    async def insert_user(
        self,
        user: UserModel,
    ) -> UserModel | None:
        
        existing_user = await self.get_user_by_username(user.username)
        
        if existing_user:
            return user
                
        new_user = await UserCollection.insert(
            UserCollection(**user.model_dump(exclude={"id", "_id"})),
        )
        
        if not new_user:
            return None
        
        return UserModel.model_validate(new_user, from_attributes=True)
        
    
    async def get_user_by_id(
        self,
        user_id: str,
    ) ->  UserModel | None:
    
        user = await UserCollection.get(user_id)
        
        if not user:
            return None
        
        return UserModel.model_validate(user, from_attributes=True)
    
    async def get_user_by_username(
        self,
        username: str,
    ) -> UserModel | None:
        
        user = await UserCollection.find_one(
            UserCollection.username == username,
        )
        
        if not user:
            return None
        
        return UserModel.model_validate(user, from_attributes=True)
    
    async def delete_user(
        self,
        user_id: str,
    ) -> bool:
        
        user = UserCollection.find(
            UserCollection.id == ObjectId(user_id),
        )
        
        tasks = TaskCollection.find(
            TaskCollection.user_id == ObjectId(user_id),
        )                
        
        delete_tasks = await tasks.delete()
        
        if delete_tasks.deleted_count:
            delete_user = await user.delete()
            return bool(delete_user.deleted_count)
        else:
            return bool(delete_tasks.deleted_count) 