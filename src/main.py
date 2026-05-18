from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.middlewares.logging import LoggingMiddleware
from src.core.exceptions import register_exception_handlers
from contextlib import asynccontextmanager
from src.core.logger import setup_logger
from src.infra.database import engine
from loguru import logger
from src.modules.user.api import router as user_router
from src.modules.captcha.api import router as captcha_router
from src.modules.auth.api import router as auth_router
from src.modules.permission.api import router as permission_router
from src.modules.role.api import router as role_router
from src.modules.provider.api import router as provider_router


# 使用上下文管理器感知项目生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()  # 配置日志组件
    settings = get_settings()
    logger.info(f'{settings.APP_NAME}启动..| 使用环境：{settings.APP_ENV}')
    yield
    await engine.dispose()
    logger.info(f'{settings.APP_NAME}关闭..')
def create_app():
    settings = get_settings()

    # 创建应用
    app = FastAPI(title=settings.APP_NAME,
                  version='1.0.0',
                  debug=settings.APP_DEBUG)

    # 注册中间件
    app.add_middleware(LoggingMiddleware)
    # 注册跨域中间件
    app.add_middleware(CORSMiddleware,
                        allow_origins=['*'],
                        allow_credentials=True,
                        allow_methods=['*'],
                        allow_headers=['*'])
    # 注册异常处理器
    register_exception_handlers(app)

    # 注册路由
    app.include_router(user_router, prefix='/api/v1')
    app.include_router(captcha_router, prefix='/api/v1')
    app.include_router(auth_router,prefix='/api/v1')
    app.include_router(permission_router, prefix='/api/v1')
    app.include_router(role_router, prefix='/api/v1')
    app.include_router(provider_router, prefix="/api/v1")
    return app
app = create_app()

@app.get('/health')
async def root():
    return {'status': 'ok'}