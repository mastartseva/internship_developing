from sqlalchemy.orm import Session
from . import models, schemas

def get_rolls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Roll).offset(skip).limit(limit).all()

def create_roll(db: Session, roll: schemas.RollCreate):
    db_roll = models.Roll(length=roll.length, weight=roll.weight)
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll

def remove_roll(db: Session, roll_id: int):
    db_roll = db.query(models.Roll).filter(models.Roll.id == roll_id).first()
    if db_roll:
        db.delete(db_roll)
        db.commit()
    return db_roll
