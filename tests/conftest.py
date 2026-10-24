import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from shop.models import Base, Category, Product


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with TestingSessionLocal() as session:
        yield session

    Base.metadata.drop_all(engine)