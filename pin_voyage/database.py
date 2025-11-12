from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(
    bind=engine, autocommit=False, expire_on_commit=False, autoflush=False
)


def get_db():
    print(DATABASE_URL)
    db = Session()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
