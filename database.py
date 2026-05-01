import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from utils.config_hander import database_conf

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    
    f"{database_conf['driver']}://"
    f"{database_conf['username']}:{database_conf['password']}@"
    f"{database_conf['host']}:{database_conf['port']}/"
    f"{database_conf['database_name']}?"
    f"charset={database_conf['charset']}",
)

print(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()


def init_db() -> None:
    # Delayed import to avoid circular dependency.
    #import models  # noqa: F401

    Base.metadata.create_all(bind=engine)