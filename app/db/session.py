from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

env = Env()
env.read_env()
database = env.str("DATABASE_URL", default="sqlite:///./sql_app.db")

if "sqlite" in database:  # pragma: no cover
    engine = create_engine(database, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print("USING SQLITE")
else:
    engine = create_engine(database, echo=True)
    print("USING POSTGRESS")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
