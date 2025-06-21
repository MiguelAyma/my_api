
from sqlalchemy import  Boolean, Integer, String, DECIMAL, DateTime, ForeignKey,ARRAY
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
    



class Archetype(Base):
    __tablename__ = "adk_archetype"

    archetype_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    icon: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    #bots: Mapped[list["Bot"]] = relationship(back_populates="archetype")
    
class Tone(Base):
    __tablename__ = "adk_tone"

    tone_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    associated_emoji: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    #bot_tones: Mapped[list["BotTone"]] = relationship(back_populates="tone")


class Bot(Base):
    __tablename__ = "adk_bot"
    bot_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(100))
    archetype_id: Mapped[int] = mapped_column(ForeignKey("adk_archetype.archetype_id"))
    formality_level: Mapped[int] = mapped_column(Integer)
    proactivity_level: Mapped[int] = mapped_column(Integer)
    response_length: Mapped[int] = mapped_column(Integer)
    main_goal: Mapped[str] = mapped_column(String(255))
    limiting_instructions: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    #archetype: Mapped["Archetype"] = relationship(back_populates="bots")
    bot_tones: Mapped[list["BotTone"]] = relationship(back_populates="bot")


class BotTone(Base):
    __tablename__ = "bot_tones"

    bot_tone_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(ForeignKey("adk_bot.bot_id"))
    tone_id: Mapped[int] = mapped_column(ForeignKey("adk_tone.tone_id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    bot: Mapped["Bot"] = relationship(back_populates="bot_tones")
    #tone: Mapped["Tone"] = relationship(back_populates="bot_tones")


class KnowledgeEntries(Base):
    __tablename__ = "adk_knowledge_entries"
    entry_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("adk_business.business_id"))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(1000))
    content_type: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    icon: Mapped[str] = mapped_column(String(255))
    improved_title: Mapped[str] = mapped_column(String(255))
    improved_content: Mapped[str] = mapped_column(String(1000))
    categories: Mapped[list[str]] =  mapped_column(ARRAY(String(255)))