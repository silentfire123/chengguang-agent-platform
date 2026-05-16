from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import BaseModel
import datetime
from src.modules.role.model import Role, user_roles
from typing import List

class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment="邮箱")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="密码哈希")
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否启用")
    is_superuser: Mapped[bool] = mapped_column(default=False, comment="是否为超级管理员")
    last_login: Mapped[datetime.datetime | None] = mapped_column(comment='最后登录时间')
    # user.roles 可以拿到用户对应的所有角色
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        lazy="selectin", # 立即加载关联角色
    )
