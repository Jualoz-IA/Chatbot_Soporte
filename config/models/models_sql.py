from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.sql_connection import Base

# Tabla de asociación para la relación many-to-many entre usuarios y roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Por ejemplo: "admin", "user", "editor"
    description = Column(String)
    
    # Relación con los usuarios a través de la tabla de asociación
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    # Lista de permisos asociados al rol
    permissions = relationship("Permission", back_populates="role")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    resource = Column(String)  # Por ejemplo: "posts", "users", "comments"
    action = Column(String)    # Por ejemplo: "read", "write", "delete"
    
    role = relationship("Role", back_populates="permissions")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación many-to-many con roles
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    # Método helper para verificar roles
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    # Método helper para verificar permisos
    def has_permission(self, resource, action):
        for role in self.roles:
            for permission in role.permissions:
                if permission.resource == resource and permission.action == action:
                    return True
        return False
    
class Parametro(Base):
    __tablename__ = "parametros"
    
    clave = Column(String, primary_key=True)
    valor = Column(String)
    tipo = Column(String)
