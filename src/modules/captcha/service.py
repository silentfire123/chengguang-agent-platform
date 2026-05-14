from redis.asyncio.client import Redis
from src.core.exceptions import BizException
from src.modules.captcha.schema import CaptchaRead, CaptchaVerifyRequest
import random, string, uuid, base64
from captcha.image import ImageCaptcha

class CaptchaService:
    # 验证码过期时间（秒）
    CAPTCHA_EXPIRE = 60 * 5
    # 验证码键前缀
    CAPTCHA_KEY_PREFIX = 'captcha:'
    def __init__(self, redis: Redis):
        self.redis = redis

    def random_code(self) -> str:
        # 生成随机数
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        # 去除可能的易混淆字符
        code = code.replace('0', 'O').replace('1','I').replace('5','S')
        return code

    # 创建验证码
    async def create_captcha(self) -> CaptchaRead:
        code = self.random_code()
        captcha_id = str(uuid.uuid4())
        key = f'{self.CAPTCHA_KEY_PREFIX}{captcha_id}'
        await self.redis.set(key,code,ex=self.CAPTCHA_EXPIRE)

        image_captcha = ImageCaptcha(width=162, height=54)
        image_data = image_captcha.generate(code)
        b64 = base64.b64encode(image_data.read()).decode()

        return CaptchaRead(
            key=captcha_id,
            image=f'data:image/png;base64,{b64}'
        )

# 校验验证码
    async def verify_captcha(self, captcha: CaptchaVerifyRequest) -> bool:
        key = f'{self.CAPTCHA_KEY_PREFIX}{captcha.key}'
        # 从redis获取数据
        stored_code = await self.redis.get(key)
        if not stored_code:
            raise BizException(code=10001, message='验证码不存在或已过期')
        if stored_code.lower() != captcha.code.lower():
            raise BizException(code=10002, message='验证码错误')
        # 删除已校验的验证码
        await self.redis.delete(key)
        return True