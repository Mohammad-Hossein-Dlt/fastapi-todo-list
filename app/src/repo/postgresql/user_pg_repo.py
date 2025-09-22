from sqlalchemy.orm import Session
from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.domain.schemas.user.user_model import UserModel
from app.src.infra.db.postgresql.models.user_db_model import UserDBModel

class UserPgRepo(IUserRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
            
    async def insert_user(
        self,
        user: UserModel,
    ) -> UserModel | None:
        
        existing_user = await self.get_user_by_username(user.username)
        
        if existing_user:
            return user
                
        user = UserDBModel(**user.model_dump(exclude_none=True))
        
        self.db.add(user)
        self.db.commit()
        
        return UserModel.model_validate(user, from_attributes=True)
        
    
    async def get_user_by_id(
        self,
        user_id: str,
    ) ->  UserModel | None:
    
        user = self.db.query(
            UserDBModel   
        ).where(
            UserDBModel.id == user_id,
        ).first()
        
        if not user:
            return None
        
        return UserModel.model_validate(user, from_attributes=True)
    
    async def get_user_by_username(
        self,
        username: str,
    ) -> UserModel | None:
        
        user = self.db.query(
            UserDBModel   
        ).where(
            UserDBModel.username == username,
        ).first()
        
        if not user:
            return None
        
        return UserModel.model_validate(user, from_attributes=True)
    
    async def delete_user(
        self,
        user_id: str,
    ) -> bool:
        
        user = await self.get_user_by_id(user_id)
        
        if user:
            user = self.db.merge(UserDBModel(**user.model_dump()))
            
        if isinstance(user, UserDBModel):
            self.db.delete(user)
            self.db.commit()
            return True
        
        return False
        