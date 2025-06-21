from sqlalchemy.orm import Session
from app.models.sql_alchemy_models import BotTone
from app.schemas._bot import BotCreate, BotResponse, BotUpdate
from app.data._bot_crud import create_bot, update_bot

def create_bot_service(db: Session, bot_data: BotCreate) -> BotResponse:
    bot = create_bot(db, bot_data)
    tone_ids = [tone.tone_id for tone in bot.bot_tones] if hasattr(bot, 'bot_tones') else bot_data.tone_ids

    return BotResponse(
        bot_id=bot.bot_id,
        business_id=bot.business_id,
        name=bot.name,
        archetype_id=bot.archetype_id,
        formality_level=bot.formality_level,
        proactivity_level=bot.proactivity_level,
        response_length=bot.response_length,
        main_goal=bot.main_goal,
        limiting_instructions=bot.limiting_instructions,
        version=bot.version,
        status=bot.status,
        created_at=bot.created_at,
        updated_at=bot.updated_at,
        tone_ids=tone_ids
    )

def update_bot_service(db: Session, bot_id: int, update_data: BotUpdate) -> BotResponse:
    bot = update_bot(db, bot_id, update_data)

    tone_ids = [bt.tone_id for bt in db.query(BotTone).filter(BotTone.bot_id == bot.bot_id).all()]

    return BotResponse(
        bot_id=bot.bot_id,
        business_id=bot.business_id,
        name=bot.name,
        archetype_id=bot.archetype_id,
        formality_level=bot.formality_level,
        proactivity_level=bot.proactivity_level,
        response_length=bot.response_length,
        main_goal=bot.main_goal,
        limiting_instructions=bot.limiting_instructions,
        version=bot.version,
        status=bot.status,
        created_at=bot.created_at,
        updated_at=bot.updated_at,
        tone_ids=tone_ids
    )