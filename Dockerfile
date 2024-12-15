FROM python:3.9-slim
WORKDIR /SWEbonus
COPY . .
RUN pip install flask flask-restful flask-swagger-ui flasgger
EXPOSE 5000
CMD ["python", "src/app.py"]
