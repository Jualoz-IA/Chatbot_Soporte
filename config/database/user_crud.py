from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.database.modelssql import User, Role

# **Obtener todos los usuarios**
def get_users(db: Session):
    try:
        return db.query(User).all()
    except Exception as e:
        return {"error": f"Error al obtener usuarios: {str(e)}"}

# **Actualizar Usuario**
def update_user(db: Session, user_id: int, username: str = None, email: str = None, role_name: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Usuario no encontrado"}

    if username:
        if len(username) < 3 or len(username) > 20:
            return {"error": "El nombre de usuario debe tener entre 3 y 20 caracteres"}
        user.username = username

    if email:
        if "@" not in email or "." not in email:
            return {"error": "Correo electrónico inválido"}
        user.email = email

    if role_name:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return {"error": "Rol no válido"}
        
        # Actualizar los roles del usuario
        user.roles = [role]

    try:
        db.commit()
        db.refresh(user)
        return {"success": f"Usuario '{user.username}' actualizado exitosamente con rol '{role_name}'"}
    except IntegrityError:
        db.rollback()
        return {"error": "El nombre de usuario o correo ya está en uso"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar usuario: {str(e)}"}

# **Obtener roles del usuario**
def get_user_roles(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return [role.name for role in user.roles]
    return []

# **Eliminar Usuario**
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Usuario no encontrado"}
    
    try:
        db.delete(user)
        db.commit()
        return {"success": f"Usuario '{user.username}' eliminado exitosamente"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al eliminar usuario: {str(e)}"}