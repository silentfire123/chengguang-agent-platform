from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from src.core.base_schema import ResponseSchema
from src.infra.database import get_db
from src.infra.redis_cache import get_redis_client
from src.modules.auth.schema import LoginRequest, TokenResponse
from src.modules.auth.service import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])

# 依赖注入
def get_auth_service(db: AsyncSession = Depends(get_db),
                     redis: Redis = Depends(get_redis_client)) -> AuthService:
    return AuthService(db, redis)
# POST /api/v1/auth/login
@router.post('/login', response_model=ResponseSchema[TokenResponse], summary='用户登录')
async def login(
        data: LoginRequest,
        svc: AuthService = Depends(get_auth_service)
):
    resp = await svc.login(data)
    return ResponseSchema(data=resp)
    pass
