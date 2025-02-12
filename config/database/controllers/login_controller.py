from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config.models.models_params import ModelParams
from ...models.models_sql import User, Role
from passlib.hash import bcrypt
from typing import Optional, Dict, Any

def create_user(db: Session, username: str, email: str, password: Optional[str] = None, role: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea un nuevo usuario. Soporta tanto creación con contraseña como registro mediante Google,
    permitiendo asignar un rol específico.
    """
    try:
        # Si se proporciona contraseña, hashearla
        hashed_password = bcrypt.hash(password) if password else None
        
        # Crear el usuario
        db_user = User(
            username=username,
            email=email,
            password=hashed_password
        )
        
        # Asignar el rol seleccionado
        selected_role = db.query(Role).filter(Role.name == role).first()
        if selected_role:
            db_user.roles.append(selected_role)
        else:
            # Si el rol no existe, asignar "user" por defecto
            default_role = db.query(Role).filter(Role.name == "user").first()
            if default_role:
                db_user.roles.append(default_role)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "status": "success",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "roles": [role.name for role in db_user.roles]
            }
        }
        
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            return {"status": "error", "message": "The username is already taken."}
        elif "email" in str(e.orig):
            return {"status": "error", "message": "The email is already registered."}
        return {"status": "error", "message": "An unexpected database error occurred."}
        
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}

def verify_user_credentials(db: Session, username: str, password: str) -> Dict[str, Any]:
    """
    Verifica las credenciales del usuario y devuelve la información si son correctas
    """
    try:
        # Buscar usuario
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return {"status": "user_not_found"}
            
        # Si el usuario no tiene contraseña (registro por Google)
        if not user.password:
            return {"status": "error", "message": "This account uses Google authentication"}
            
        # Verificar contraseña
        if not bcrypt.verify(password, user.password):
            return {"status": "wrong_password"}
            
        return {
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles]
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Busca un usuario por su email
    """
    return db.query(User).filter(User.email == email).first()

def get_roles(db: Session):
    """Obtiene todos los roles disponibles en la base de datos."""
    try:
        roles = db.query(Role).all()
        return [role.name for role in roles]
    except Exception as e:
        return {"error": f"Error al obtener roles: {str(e)}"}
