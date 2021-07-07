from pydantic import BaseModel

class StockPredictionResult(BaseModel):
    stock_prediction_value: int