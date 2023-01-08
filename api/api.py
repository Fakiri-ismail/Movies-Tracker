from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.handlers.movie import router
from api.middleware import PrometheusMiddleware


def creat_app():
    app = FastAPI(docs_url="/")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    PrometheusMiddleware(app)

    # Router
    app.include_router(router=router)
    return app
