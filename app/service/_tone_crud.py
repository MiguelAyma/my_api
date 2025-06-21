from sqlalchemy.orm import Session
from app.schemas._tone import ToneCreate, ToneUpdate, ToneResponse
from app.data._tone_crud import get_all_tones, create_tone, update_tone

def get_all_tones_service(db: Session) -> list[ToneResponse]:
    tones = get_all_tones(db)
    return [ToneResponse.model_validate(t) for t in tones]

def create_tone_service(db: Session, data: ToneCreate) -> ToneResponse:
    tone = create_tone(db, data)
    return ToneResponse.model_validate(tone)

def update_tone_service(db: Session, tone_id: int, data: ToneUpdate) -> ToneResponse:
    tone = update_tone(db, tone_id, data)
    return ToneResponse.model_validate(tone)
