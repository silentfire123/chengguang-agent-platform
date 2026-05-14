from datetime import datetime
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import BizException
from src.modules.auth.schema import LoginRequest, TokenResponse
from src.modules.captcha.schema import CaptchaVerifyRequest
from src.modules.captcha.service import CaptchaService
from src.modules.user.repository import UserRepository
from src.utils.jwt_utils import encode_jwt
from src.utils.password_utils import verify_password
from loguru import logger

class AuthService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.captcha_svc = CaptchaService(redis)
        self.user_repo = UserRepository(db)

    async def login(self, data: LoginRequest) -> TokenResponse:
        # 1. 校验验证码
        captcha_verify_req = CaptchaVerifyRequest(
            key=data.captcha_key,
            code=data.captcha_code
        )
        await self.captcha_svc.verify_captcha(captcha_verify_req)
        # 2. 校验通过，查询用户信息
        user = await self.user_repo.get_by_username(data.username)
        if not user:
            raise BizException(code=10002, message='用户不存在')
        if not user.is_active:
            raise BizException(code=10004, message='用户已被禁用')
        # 3. 校验密码
        if not verify_password(data.password, user.hashed_password):
            raise BizException(code=10003, message='密码错误')
        # 4. 生成token:强制sub是str
        payload = {'sub': str(user.id), 'username': user.username, 'email': user.email}
        token = encode_jwt(payload)
        logger.info(f'生成token：{token}')

        return TokenResponse(access_token=token)
