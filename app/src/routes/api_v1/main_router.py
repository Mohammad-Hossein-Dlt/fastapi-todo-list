from fastapi import APIRouter
from app.src.routes.api_v1.user._router import router as user_router
from app.src.routes.api_v1.task._router import router as task_router

ROUTE_PREFIX_VERSION_API = "/api_v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(user_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(task_router, prefix=ROUTE_PREFIX_VERSION_API)
