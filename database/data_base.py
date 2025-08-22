from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Указываем тип бд(postgres, sqlite)
SQL_DATABASE ="sqlite:///./movielib.db"

# Создание движка
engine = create_engine(SQL_DATABASE)

# Создание сессии для хранения данных
SessionLocal = sessionmaker(bind=engine)


# Создаём полнаценную базу
Base = declarative_base()


# Функция для подключения к бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
