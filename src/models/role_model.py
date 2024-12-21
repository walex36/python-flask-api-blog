from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .base_model import db

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role") # type: ignore

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"