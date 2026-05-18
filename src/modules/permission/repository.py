from src.core.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.modules.permission.model import Permission

class PermissionRepository(BaseRepository[Permission]):
    SEARCH_FIELDS = [
        'code',
        'name'
    ]
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Permission, db)

    # 按照权限码查找权限功能
    # 为了编码方便，好多语言才引入了强类型检查
    async def get_by_code(self, code: str) -> Permission | None:
        stmt = select(Permission).where(Permission.code == code)
        result = await self.db.scalar(stmt)
        return result

    async def get_by_ids(self, ids: list[int]) -> list[Permission]:
        result = await self.db.scalars(select(Permission).where(Permission.id.in_(ids)))
        return result.all()
# 分页搜索
    async def search_page(self, offset: int,
                          limit: int,
                          keyword: str | None) -> tuple[list[Permission], int]:
        return await self.get_page(offset, limit, keyword, self.SEARCH_FIELDS)
