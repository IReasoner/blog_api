from __future__ import annotations # for referenece post before defining it

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC

from database import Base


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  passwordhash: Mapped[str] = mapped_column(String)
  image_file: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

  
  @property
  def image_url(self):
    if self.image_file:
      return f"/media/profile_pics/{self.image_file}"
    return f"/media/profile_pics/default.jpeg"

  to_post: Mapped[list[Post]] = relationship("Post", back_populates="to_user", cascade="all, delete-orphan")
  
class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
  title: Mapped[str] = mapped_column(String, nullable=False)
  content: Mapped[str] = mapped_column(Text)
  date_posted: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC)
    )


  to_user: Mapped[User] = relationship("User", back_populates="to_post")
  