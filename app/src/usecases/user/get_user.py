from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.domain.schemas.user.user_model import UserModel
from app.src.infra.exceptions.exceptions import OperationFailureException

class GetUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user_id: str,
    ) -> UserModel:
        
        try:
            user: UserModel = await self.user_repo.get_user_by_id(user_id)
            return user.model_dump(mode="json") if user else None
        except:
            raise OperationFailureException(500, "Internal server error")  