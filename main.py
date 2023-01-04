import uvicorn

from api.api import creat_app


def main():
    app = creat_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
