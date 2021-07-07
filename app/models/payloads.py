from typing import List
from pydantic import BaseModel


class StockPredictionPayload(BaseModel):
    date: int
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int


def payload_to_list(dppl: StockPredictionPayload) -> List:
    return [
        dppl.date,
        dppl.open,
        dppl.high,
        dppl.low,
        dppl.close,
        dppl.adj_close,
        dppl.volume,
        ]