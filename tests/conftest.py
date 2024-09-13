import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from biblioteca_digital.app import app
from biblioteca_digital.database import get_session
from biblioteca_digital.models import User, table_registry
from biblioteca_digital.schemas import UserPublic


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    db_user = User(
        username='Teste', email='teste@test.com', password='testsecret'
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    user = UserPublic.model_validate(db_user).model_dump()

    return user
