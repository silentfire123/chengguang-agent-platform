from redis.asyncio.client import Redis
from src.core.base_schema import ResponseSchema
from src.infra.redis_cache import get_redis_client
from fastapi import APIRouter, Depends
from src.modules.captcha.service import CaptchaService
from src.modules.captcha.schema import CaptchaRead, CaptchaVerifyRequest

router = APIRouter(prefix='/captcha', tags=['验证码'])

# 注入 CaptchaService 依赖、 CaptchaService 依赖 redis
def get_captcha_service(redis:Redis = Depends(get_redis_client)) -> CaptchaService:
    return CaptchaService(redis=redis)

@router.get('', response_model=ResponseSchema[CaptchaRead], summary='获取验证码')
async def get_captcha(
        svc: CaptchaService = Depends(get_captcha_service),
):
    captcha = await svc.create_captcha()
    return ResponseSchema[CaptchaRead](data=captcha)

@router.post('', response_model=ResponseSchema[bool], summary='校验验证码')
async def verify_captcha(
        captcha:CaptchaVerifyRequest,
        svc: CaptchaService = Depends(get_captcha_service),
):
    is_valid = await svc.verify_captcha(captcha)
    return ResponseSchema[bool](data=is_valid)
