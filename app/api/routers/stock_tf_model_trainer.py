from fastapi import APIRouter
from starlette.requests import Request

from app.services.models import StockPredictionModel
from app.models.payloads import StockPredictionPayload
from app.models.predictions import StockPredictionResult

router = APIRouter()

@router.get(
    "/train",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def train(
        project_id: Optional[List[str]] = Depends(parse_comma_separated_list("project_id", return_type=int)),
        deploy_service: EndpointDeployService = Depends(
            Provide[Container.endpoint_deploy_service]),
        settings = Depends(get_settings),
        ):
    
    project_ids = project_id
    # if not project_ids:
    #     project_ids = "ALL"
    body = {
        "all": 10,
        "healthy": 2,
        "warning": 0,
        "error": 0
    }
    return CommonResponse(data=body)