from logging import getLogger

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware

from api.settings import Settings, settings_instance


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, test_option: bool = False) -> None:
        super().__init__(app)
        self._test_option = test_option

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Custom"] = "Exemple"
        return response


class PrometheusMiddleware:
    def __init__(self, app: FastAPI) -> None:
        logger = getLogger("api.PrometheusMiddleware")
        settings: Settings = settings_instance()
        if settings.enable_metrics:
            logger.info("metrics enabeld")
            Instrumentator().instrument(app).expose(app)
        else:
            logger.info("metrics disabeld")
