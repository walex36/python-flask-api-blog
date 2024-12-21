from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .base_model import db


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id", name="role_id"), nullable=True)
    role: Mapped["role.Role"] = relationship(back_populates="user")  # type: ignore

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"