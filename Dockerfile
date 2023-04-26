# FROM python:3.10
FROM python:3.10-slim-buster


WORKDIR /app


COPY requirements.txt .


RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y build-essential cmake \
    && apt-get install -y libopenblas-dev liblapack-dev \
    && apt-get install -y libx11-dev libgtk-3-dev \
    && pip install cmake==3.26.1 \
    && pip install -r requirements.txt



COPY . .


EXPOSE 8000

CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]
