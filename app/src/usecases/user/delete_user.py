from app.src.repo.interface.Iuser_repo import IUserRepo
from app.src.infra.exceptions.exceptions import OperationFailureException

class DeleteUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo    
    
    async def execute(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            return await self.user_repo.delete_user(user_id)
        except:
            raise OperationFailureException(500, "Internal server error")  