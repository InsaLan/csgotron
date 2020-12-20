FROM python:3-slim

WORKDIR /app

ADD requirements.txt .

ADD main.py .

RUN pip3 install -r requirements.txt

ADD src src

CMD python3 main.py
