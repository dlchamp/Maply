import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Reaction(Base):
    """Represents a reaction in the database."""

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    country_code: Mapped[str] = mapped_column(sa.Text, nullable=False)
    user_count: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
