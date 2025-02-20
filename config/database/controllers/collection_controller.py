from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict, List, Optional
from config.models.models_sql import Options

def get_all_options(db: Session):
    """Obtener todas las opciones de chat"""
    try:
        return db.query(Options).all()
    except Exception as e:
        return {"error": f"Error al obtener opciones: {str(e)}"}

def get_active_collections_map(db: Session) -> Dict[str, str]:
    """
    Obtener un diccionario de opciones activas en formato:
    {opción: colección}
    """
    try:
        options = db.query(Options)\
                   .filter(Options.active == True)\
                   .all()
        return {opt.option: opt.colleption for opt in options}
    except Exception as e:
        return {"error": f"Error al obtener el mapa de colecciones: {str(e)}"}

def create_option(db: Session, option: str, collection: str, active: bool = True):
    """Crear una nueva opción"""
    try:
        new_option = Options(
            option=option,
            colleption=collection,
            active=active
        )
        db.add(new_option)
        db.commit()
        return {"success": f"Opción '{option}' creada exitosamente"}
    except IntegrityError:
        db.rollback()
        return {"error": "La opción ya existe"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al crear opción: {str(e)}"}

def update_option(db: Session, option: str, collection: Optional[str] = None, active: Optional[bool] = None):
    """Actualizar una opción existente"""
    try:
        opt = db.query(Options).filter(Options.option == option).first()
        if not opt:
            return {"error": "Opción no encontrada"}
        
        if collection is not None:
            opt.colleption = collection
        if active is not None:
            opt.active = active
            
        db.commit()
        return {"success": f"Opción '{option}' actualizada exitosamente"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar opción: {str(e)}"}

def delete_option(db: Session, option: str):
    """Eliminar una opción"""
    try:
        opt = db.query(Options).filter(Options.option == option).first()
        if not opt:
            return {"error": "Opción no encontrada"}
        
        db.delete(opt)
        db.commit()
        return {"success": f"Opción '{option}' eliminada exitosamente"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al eliminar opción: {str(e)}"}

def bulk_create_options(db: Session, options_data: List[Dict]):
    """
    Crear múltiples opciones a la vez
    options_data: Lista de diccionarios con formato:
    [{"option": "texto", "collection": "nombre_coleccion", "active": True}]
    """
    try:
        for data in options_data:
            new_option = Options(
                option=data["option"],
                colleption=data["collection"],
                active=data.get("active", True)
            )
            db.add(new_option)
        db.commit()
        return {"success": "Opciones creadas exitosamente"}
    except IntegrityError:
        db.rollback()
        return {"error": "Una o más opciones ya existen"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al crear opciones: {str(e)}"}