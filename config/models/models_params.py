from sqlalchemy import Column, Integer, String, Double, Float
class ModelParams():
    __tablename__ = "model_config"
    
    id = Column(Integer, primary_key=True, index=True)
    currentGroqToken = Column(String)
    selected_model = Column(String)
    temperature = Column(Float)
    max_tokens = Column(Integer)
    top_p = Column(Double)
    frequency_penalty = Column(Double)
    presence_penalty = Column(Double)
    