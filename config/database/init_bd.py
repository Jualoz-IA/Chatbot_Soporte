from .sql_connection import Base, engine, SessionLocal  # o from .conectionsql import Base, engine, SessionLocal
from ..models.models_sql import User, Role, Permission
from passlib.hash import bcrypt

def create_default_roles(db):
    """Crear roles por defecto si no existen"""
    default_roles = {
        "admin": {
            "description": "Administrator with full access",
            "permissions": [
                ("users", "read"),
                ("users", "write"),
                ("users", "delete"),
                ("roles", "read"),
                ("roles", "write"),
            ]
        },
        "user": {
            "description": "Regular user with limited access",
            "permissions": [
                ("users", "read"),
            ]
        }
    }

    for role_name, role_info in default_roles.items():
        existing_role = db.query(Role).filter(Role.name == role_name).first()
        if not existing_role:
            new_role = Role(
                name=role_name,
                description=role_info["description"]
            )
            db.add(new_role)
            db.flush()

            for resource, action in role_info["permissions"]:
                permission = Permission(
                    role_id=new_role.id,
                    resource=resource,
                    action=action
                )
                db.add(permission)

def create_default_admin(db):
    """Crear usuario administrador por defecto si no existe"""
    import os
    admin_username = os.getenv('USER')
    admin_email = os.getenv('EMAIL')
    admin_password = os.getenv('PASSWORD')

    existing_admin = db.query(User).filter(
        (User.username == admin_username) | (User.email == admin_email)
    ).first()

    if not existing_admin:
        admin_user = User(
            username=admin_username,
            email=admin_email,
            password=bcrypt.hash(admin_password)
        )

        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if admin_role:
            admin_user.roles.append(admin_role)

        db.add(admin_user)

def init_db():
    """Inicializar la base de datos con tablas y datos por defecto"""
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            create_default_roles(db)
            create_default_admin(db)
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    except Exception as e:
        raise