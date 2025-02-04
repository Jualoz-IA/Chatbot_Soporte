from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .modelssql import User

def create_user(db: Session, username: str, email: str, password: str):
    try:
        db_user = User(username=username, email=email, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"user": db_user}  # Devuelve un diccionario con el usuario creado
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            return {"error": "The username is already taken."}
        elif "email" in str(e.orig):
            return {"error": "The email is already registered."}
        else:
            return {"error": "An unexpected error occurred."}
    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_user_credentials(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return {"status": "user_not_found"}
    elif not user.password == password:
        return {"status": "wrong_password"}
    else:
        return {"status": "success", "user": user}