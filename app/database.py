from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# задаём строку подключения к нашему файлу-базе tasks.db
SQLALCHEMY_DATABASE_URL = 'sqlite:///./tasks.db'

# создаём движок SQLAlchemy, который будет посредником между кодом и бд
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},      # нужно для корректной работы бд в многопоточном режиме
    echo=True)      # выводит в консоли все SQL запросы

# фабрика сессий для выполнения операций crud
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
