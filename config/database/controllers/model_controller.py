from sqlalchemy.orm import Session
from config.models.models_params import ModelParams

def update_model_params(db: Session, modelParams: ModelParams):
    modelParams = db.query(ModelParams).filter(ModelParams.id == modelParams.id).first()
    try:
        db.commit()
        db.refresh(modelParams)
        return {"success": f"Parametros del modelo '{modelParams.selected_model}' actualizados exitosamente"}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar el modelo: {str(e)}"}