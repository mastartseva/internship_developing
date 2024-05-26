from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, statistics

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/rolls/", response_model=schemas.Roll)
def create_roll(roll: schemas.RollCreate, db: Session = Depends(database.get_db)):
    return crud.create_roll(db=db, roll=roll)

@app.delete("/rolls/{roll_id}", response_model=schemas.Roll)
def delete_roll(roll_id: int, db: Session = Depends(database.get_db)):
    db_roll = crud.remove_roll(db=db, roll_id=roll_id)
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    return db_roll

@app.get("/rolls/", response_model=list[schemas.Roll])
def read_rolls(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    rolls = crud.get_rolls(db, skip=skip, limit=limit)
    return rolls

@app.get("/rolls/statistics/")
def read_statistics(start_date: datetime, end_date: datetime, db: Session = Depends(database.get_db)):
    return statistics.get_statistics(db, start_date=start_date, end_date=end_date)
   
