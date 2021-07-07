# for FastAPI Application
import uvicorn

from fastapi import FastAPI, Response, WebSocket, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

from typing import Optional

from app.api.routers import stock_tf_model_trainer, stock_tf_model_predictor


def create_app() -> FastAPI:

    app = FastAPI()

    app.include_router(stock_tf_model_trainer.router)
    app.include_router(stock_tf_model_predictor.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8890)