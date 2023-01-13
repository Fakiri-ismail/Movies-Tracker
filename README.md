# Build a Modern API with FastAPI and Python

## Command Line
### Makefile
- make format [to format code]
### Docker
- docker exec -it [mongo image name] mongosh
- docker build . -t movie-tracker
- docker run -p 8080:8080 movie-tracker
- docker-compose up
- sudo kill -9 $(sudo lsof -t -i:8080)
### MicroK8
- microk8s enable registry
- docker tag movie-tracker:latest localhost:32000/movie-tracker
- docker push localhost:32000/movie-tracker
- kubectl apply -f movie_tracker_deployment.yaml
- kubectl get services
### Gunicorn
- gunicorn -k uvicorn.workers.UvicornWorker main:create_app [run the app with one worker]
- gunicorn -k api.workers.MyUvicornWorker -w 2 main:create_app   [To understand more](https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/)

## Deploiment
### Kubernetes
- install microk8s and kubectl
## Gunicorn
- install gunicorn

## Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor : Asynchronous Python driver for MongoDB](https://motor.readthedocs.io/en/stable/index.html)
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Starlette](https://www.starlette.io/)
- [JSON WEB TOKENS (JWT)](https://jwt.io/introduction)
- [Scaling API](https://www.apriorit.com/dev-blog/776-cloud-api-scaling)