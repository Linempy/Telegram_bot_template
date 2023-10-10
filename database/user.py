from .database import BaseModel
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseModel):
    __tablename__ = 'users'

    # Telegram user id
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True, primary_key=True )
    
    # Telegram user name
    username: Mapped[str] = mapped_column(String(30), nullable=True)

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'
