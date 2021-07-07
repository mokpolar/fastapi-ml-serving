from fastapi import APIRouter
from starlette.requests import Request

from app.services.models import StockPredictionModel
from app.models.payloads import StockPredictionPayload
from app.models.predictions import StockPredictionResult

router = APIRouter()

@router.post('/predict')
def predict(
    request: Request,
    data: StockPredictionPayload = None
) -> StockPredictionResult:

    model: StockPredictionModel = request.app.state.model
    prediction: StockPredictionResult = model.predict(data)

    return prediction
