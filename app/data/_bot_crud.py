from sqlalchemy.orm import Session
from app.models.sql_alchemy_models import Bot,BotTone
from app.schemas._bot import BotCreate, BotUpdate
import datetime

def create_bot(db: Session, bot_data: BotCreate) -> Bot:
    bot = Bot(
        business_id=bot_data.business_id,
        name=bot_data.name,
        archetype_id=bot_data.archetype_id,
        formality_level=bot_data.formality_level,
        proactivity_level=bot_data.proactivity_level,
        response_length=bot_data.response_length,
        main_goal=bot_data.main_goal,
        limiting_instructions=bot_data.limiting_instructions,
        version=bot_data.version,
        status=bot_data.status,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(bot)
    db.flush()  # para obtener bot_id

    for tone_id in bot_data.tone_ids:
        db.add(BotTone(
            bot_id=bot.bot_id,
            tone_id=tone_id,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        ))

    db.commit()
    db.refresh(bot)
    return bot



def update_bot(db: Session, bot_id: int, update_data: BotUpdate) -> Bot:
    bot = db.query(Bot).filter(Bot.bot_id == bot_id).first()
    if not bot:
        raise ValueError(f"Bot with ID {bot_id} not found")

    # Actualizar campos simples
    for field, value in update_data.model_dump(exclude_unset=True).items():
        if field != "tone_ids":
            setattr(bot, field, value)

    # Actualizar tonos si se envió tone_ids
    if update_data.tone_ids is not None:
        existing_tone_ids = {bt.tone_id for bt in db.query(BotTone).filter(BotTone.bot_id == bot_id).all()}
        new_tone_ids = set(update_data.tone_ids)

        # Eliminar tonos que ya no están
        tones_to_delete = existing_tone_ids - new_tone_ids
        if tones_to_delete:
            db.query(BotTone).filter(BotTone.bot_id == bot_id, BotTone.tone_id.in_(tones_to_delete)).delete(synchronize_session=False)

        # Agregar nuevos tonos
        tones_to_add = new_tone_ids - existing_tone_ids
        now = datetime.datetime.now(datetime.timezone.utc)
        for tone_id in tones_to_add:
            db.add(BotTone(bot_id=bot_id, tone_id=tone_id, created_at=now, updated_at=now))

    bot.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(bot)
    return bot