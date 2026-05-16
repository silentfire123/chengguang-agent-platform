from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import BizException, ERR_PERM_NOT_FOUND_MSG, ERR_PERM_NOT_FOUND
from src.modules.permission.model import Permission
from src.modules.permission.repository import PermissionRepository
from src.modules.permission.schema import PermissionCreate, PermissionUpdate


class PermissionService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = PermissionRepository(db)

    async def create_permission(self, data: PermissionCreate) -> Permission:
        # 1. 检查 code 是否已存在，已存在则抛 BizException
        perm = await self.repo.get_by_code(data.code)
        if perm:
            raise BizException(code=30001, message='权限标识已存在')

        # 2. 创建 Permission 对象
        perm = Permission(code=data.code, name=data.name, description=data.description)

        # 3. 调用 repo.create() 保存
        await self.repo.create(perm)
        return perm

    async def get_permission(self, permission_id: int) -> Permission:
        # 查不到抛 BizException(code=ERR_PERM_NOT_FOUND)
        perm = await self.repo.get_by_id(permission_id)
        if not perm:
            raise BizException(code=ERR_PERM_NOT_FOUND, message=ERR_PERM_NOT_FOUND_MSG)
        return perm

    async def list_permissions(self) -> list[Permission]:
        # 调用 repo.get_all()
        perms = await self.repo.get_all()
        return perms

    async def update_permission(self, permission_id: int, data: PermissionUpdate) -> Permission:
        # 1. 查找权限，不存在抛异常
        perm = await self.get_permission(permission_id)

        # 2. 只更新 data 中非 None 的字段
        if data.name:
            perm.name = data.name
        if data.description:
            perm.description = data.description

        # 3. 调用 repo.update()
        return await self.repo.update(perm)

    async def delete_permission(self, permission_id: int) -> None:
        # 1. 查找权限，不存在抛异常
        # 2. 调用 repo.delete()
        await self.repo.delete_by_id(permission_id)
