# Build a Modern API from scratch using FastAPI and Python
In this project, I builded a movie tracking API from scratch using Python with FastAPI and MongoDB.
During the project, I learned the basics of web application development, how to structure a Python project, how to apply design patterns and write unit tests for the API.
I also learned how to use the tools that professional Python developers use in their daily work and improve my workflow.

## Commands Line
### Makefile
- Format the project files
```bash
make format
```
- Generate the project documentation
```bash
make generate-docs
```
- Run the project unit tests
```bash
make tests
```
### Docker
- Run the application using Dockerfile
```bash
docker run mongo:5.0.14
docker build . -t movie-tracker
docker run -p 8000:8000 movie-tracker
```
- Run the application using Docker-compose
```bash
docker-compose up
```

## Deploiment
### Kubernetes
- install [Microk8s](https://microk8s.io/) and [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
```bash
microk8s enable registry metrics-server dns storage
docker tag movie-tracker:latest localhost:32000/movie-tracker
docker push localhost:32000/movie-tracker
kubectl apply -f movie_tracker_deployment.yaml
kubectl get services
```
### Gunicorn
- install [Gunicorn](https://docs.gunicorn.org/en/stable/install.html)
```bash
# Run the app with the default UvicornWorker and one worker
gunicorn -k uvicorn.workers.UvicornWorker main:create_app
# Run the app with the MyUvicornWorker and two worker
- gunicorn -k api.workers.MyUvicornWorker -w 2 main:create_app
```
[To understand more](https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/)

## Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor : Asynchronous Python driver for MongoDB](https://motor.readthedocs.io/en/stable/index.html)
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Starlette](https://www.starlette.io/)
- [JSON WEB TOKENS (JWT)](https://jwt.io/introduction)
- [Scaling API](https://www.apriorit.com/dev-blog/776-cloud-api-scaling)