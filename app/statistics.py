# app/statistics.py
import statistics
from databases import Database
from fastapi import Depends
from flask import app
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from .models import Roll

def get_statistics(db: Session, start_date: datetime, end_date: datetime):
    added_count = db.query(func.count(Roll.id)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    removed_count = db.query(func.count(Roll.id)).filter(Roll.date_removed.between(start_date, end_date)).scalar()
    
    avg_length = db.query(func.avg(Roll.length)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    avg_weight = db.query(func.avg(Roll.weight)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    
    min_length = db.query(func.min(Roll.length)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    max_length = db.query(func.max(Roll.length)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    min_weight = db.query(func.min(Roll.weight)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    max_weight = db.query(func.max(Roll.weight)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    
    total_weight = db.query(func.sum(Roll.weight)).filter(Roll.date_added.between(start_date, end_date)).scalar()
    
    return {
        "added_count": added_count,
        "removed_count": removed_count,
        "avg_length": avg_length,
        "avg_weight": avg_weight,
        "min_length": min_length,
        "max_length": max_length,
        "min_weight": min_weight,
        "max_weight": max_weight,
        "total_weight": total_weight,
    }

@app.get("/rolls/statistics/")
def read_statistics(start_date: datetime, end_date: datetime, db: Session = Depends(Database.get_db)):
    return statistics.get_statistics(db, start_date=start_date, end_date=end_date)
