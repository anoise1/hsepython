from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select

engine = create_engine("sqlite:///universities.db")


class University(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    city: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def main_page():
    return "Hello"


@app.post("/university")
def add_uni(university: University, session: Session = Depends(get_session)):
    session.add(university)
    session.commit()
    session.refresh(university)
    return university


@app.get("/university/add")
def add_uni_get(name: str, city: str, session: Session = Depends(get_session)):
    university = University(name=name, city=city)
    session.add(university)
    session.commit()
    session.refresh(university)
    return university


@app.get("/universities")
def get_all_uni(session: Session = Depends(get_session)):
    return session.exec(select(University)).all()


@app.get("/university/{uni_id}")
def get_uni(uni_id: int, session: Session = Depends(get_session)):
    return session.get(University, uni_id)
