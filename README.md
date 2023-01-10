## Build a Modern API with FastAPI and Python

### Command Line
- docker exec -it [mongo image name] mongosh
- make fmt [to format code]
- docker build . -t movie-tracker
- docker run -p 8000:8000 movie-tracker
- docker-compose up
- sudo kill -9 $(sudo lsof -t -i:8000)

### Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor](https://motor.readthedocs.io/en/stable/index.html) : Asynchronous Python driver for MongoDB
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Starlette](https://www.starlette.io/)
- [JSON WEB TOKENS (JWT)](https://jwt.io/introduction)