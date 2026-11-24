from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Note

app = FastAPI(title="FastAPI starter")


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class NoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime


@app.get("/health", include_in_schema=False)
def health():
    # No database call: a slow database shouldn't take the app out of rotation.
    return {"ok": True}


@app.get("/")
def index(session: Session = Depends(get_session)):
    notes = session.scalar(select(func.count()).select_from(Note))
    return {"message": "Hello from FastAPI on Containify", "notes": notes, "docs": "/docs"}


@app.get("/notes", response_model=list[NoteOut])
def list_notes(session: Session = Depends(get_session)):
    return session.scalars(select(Note).order_by(Note.id.desc()).limit(50)).all()


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteIn, session: Session = Depends(get_session)):
    row = Note(text=note.text)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row
