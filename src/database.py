from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	db: Session = SessionLocal()
	try:
		yield db
	finally:
		db.close()
