# db/models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .conectionsql import Base  # Importamos Base para heredar de ella

class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True, index=True)  # ID de usuario
    username = Column(String, unique=True, index=True, nullable=False)  # Nombre de usuario único
    email = Column(String, unique=True, index=True, nullable=False)  # Correo electrónico único
    password = Column(String,  nullable=False)  # Contraseña del usuario
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación