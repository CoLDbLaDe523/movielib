from database import get_db
from database.models import User, Movie, Favorite, Rating


# Функция для создания пользователя
def create_user(username, phonenumber):
    db = next(get_db()) # Подключение к БД

    new_user = User(username=username, phonenumber=phonenumber)
    db.add(new_user)
    db.commit()
    return "Пользователь успешно добавлен"

# Функция для получения всех пользователей
def get_all_users_db():
    db = next(get_db())

    all_users = db.query(User).all()
    return all_users

# Функция для получения определённого юзера
def get_exact_user_db(user_id=None):
    db = next(get_db())
    if user_id:
        exact_user = db.query(User).filter_by(id=user_id).first()
        if exact_user:
            return exact_user
        return False
    return db.query(User).all

# Функция удаления пользователя
def delete_user_db(user_id):
    db = next(get_db())

    exact_user = db.query(User).filter_by(id=user_id).delete()
    if exact_user:
        db.delete(exact_user)
        db.commit()
        return "Пользователь удалён"
    return False

