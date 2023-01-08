from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.handlers.movie import router
from api.middleware import CustomHeaderMiddleware, PrometheusMiddleware


def creat_app():
    app = FastAPI(docs_url="/")

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom Middleware
    app.add_middleware(CustomHeaderMiddleware, test_option=True)

    # Prometheus Middleware
    PrometheusMiddleware(app)

    # Router
    app.include_router(router=router)
    return app
