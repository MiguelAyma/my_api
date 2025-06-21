from sqlalchemy.orm import Session
from app.models.sql_alchemy_models import Tone
from app.schemas._tone import ToneCreate, ToneUpdate
import datetime

def get_all_tones(db: Session) -> list[Tone]:
    return db.query(Tone).order_by(Tone.name).all()

def create_tone(db: Session, data: ToneCreate) -> Tone:
    now = datetime.datetime.now(datetime.timezone.utc)
    tone = Tone(
        name=data.name,
        associated_emoji=data.associated_emoji,
        created_at=now,
        updated_at=now
    )
    db.add(tone)
    db.commit()
    db.refresh(tone)
    return tone

def update_tone(db: Session, tone_id: int, data: ToneUpdate) -> Tone:
    tone = db.query(Tone).filter(Tone.tone_id == tone_id).first()
    if not tone:
        raise ValueError(f"Tone with ID {tone_id} not found")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(tone, field, value)
    
    tone.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(tone)
    return tone
