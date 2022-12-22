from fastapi import FastAPI

from api.handlers.demo import router


def creat_app():
    app = FastAPI(docs_url="/")
    app.include_router(router=router)
    return app
