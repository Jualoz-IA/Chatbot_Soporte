from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.models.models_sql import Parametro

# Obtener todos los parámetros
def get_parametros(db: Session):
    try:
        return db.query(Parametro).all()
    except Exception as e:
        return {"error": f"Error al obtener parámetros: {str(e)}"}

# Obtener parámetros en formato clave-valor
def get_parametros_dict(db: Session):
    try:
        parametros = db.query(Parametro.clave, Parametro.valor).all()
        return {param.clave: param.valor for param in parametros}
    except Exception as e:
        return {"error": f"Error al obtener parámetros: {str(e)}"}

# Guardar o actualizar parámetros
def guardar_parametros(db: Session, parametros):
    try:
        for clave, valor, tipo in parametros:
            param = db.query(Parametro).filter_by(clave=clave).first()
            if param:
                param.valor = str(valor)
                param.tipo = tipo
            else:
                param = Parametro(clave=clave, valor=str(valor), tipo=tipo)
                db.add(param)
        db.commit()
        return {"success": "Parámetros guardados exitosamente"}
    except IntegrityError:
        db.rollback()
        return {"error": "Error de integridad al guardar parámetros"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al guardar parámetros: {str(e)}"}

# Eliminar un parámetro
def delete_parametro(db: Session, clave: str):
    param = db.query(Parametro).filter(Parametro.clave == clave).first()
    if not param:
        return {"error": "Parámetro no encontrado"}
    
    try:
        db.delete(param)
        db.commit()
        return {"success": f"Parámetro '{clave}' eliminado exitosamente"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al eliminar parámetro: {str(e)}"}
