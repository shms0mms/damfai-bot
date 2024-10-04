FROM python:alpine3.17 


WORKDIR /app


COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY . .


CMD python -u src/main.py

