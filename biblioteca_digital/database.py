from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from biblioteca_digital.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
