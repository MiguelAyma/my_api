from sqlalchemy import  Boolean, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
import datetime


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

    categories = relationship("Category", back_populates="business")
    items = relationship("Item", back_populates="business")
    
class Category(Base):
    __tablename__ = 'adk_category'
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey('adk_business.business_id'))
    category_name: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(Integer, default=6)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
        # Relación inversa
    items = relationship("ItemCategory", back_populates="category")
    business = relationship("Business", back_populates="categories")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_by_user: Mapped[bool] = mapped_column(Boolean, default=False)
    
class Item(Base):
    __tablename__ = 'adk_item'
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_slug: Mapped[str] = mapped_column(String, unique=True)
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey('adk_business.business_id'))
    item_name: Mapped[str] = mapped_column(String)
    item_description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    price_discount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    is_visible:Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_by_user: Mapped[bool] = mapped_column(Boolean, default=False)
   # Relación con ItemCategory (relación secundaria con Category)
    categories = relationship(
        "ItemCategory",
        back_populates="item",
        cascade="all, delete",
        passive_deletes=True  #Esto evita el UPDATE a NULL
    )
    business = relationship("Business", back_populates="items")

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    
class ItemCategory(Base):
    __tablename__ = 'adk_item_category'
    item_category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('adk_item.item_id', ondelete="CASCADE") )
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('adk_category.category_id'))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    # Relaciones necesarias:
    item = relationship("Item", back_populates="categories")
    category = relationship("Category", back_populates="items")
    



    
    
    
    
    