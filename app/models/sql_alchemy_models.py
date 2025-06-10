from sqlalchemy import JSON, Boolean, Integer, String, DECIMAL, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = 'adk_user'
    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

class Business(Base):
    __tablename__ = 'adk_business'
    business_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("adk_user.user_id"))
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_description: Mapped[str] = mapped_column(String(1500), nullable=True)
    logo_path: Mapped[str] = mapped_column(String(500), nullable=True)
    facebook_url: Mapped[str] = mapped_column(String(255), nullable=True)
    instagram_url: Mapped[str] = mapped_column(String(255), nullable=True)
    tiktok_url: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    whatsapp_url: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    address_url: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_by_user: Mapped[bool] = mapped_column(Boolean, default=False)
    #meta = relationship("Meta", uselist=False, back_populates="business")
    #categories = relationship("Category", back_populates="business")
    #items = relationship("Item", back_populates="business")
    



    
    
    
    
    