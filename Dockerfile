FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get upgrade
# RUN apt-get install -y apt-utils
# RUN apt-get install -y dialog
# RUN apt-get install -y python3-pkg-resources 
# RUN apt-get --reinstall install -y python3-pkg-resources
# RUN apt-get install -y python3-setuptools 
# RUN apt-get install -y python3-wheel 
# RUN apt-get install -y python3-pip


RUN apt-get update
RUN apt-get install -y build-essential cmake
RUN apt-get install -y libopenblas-dev liblapack-dev
RUN apt-get install -y libx11-dev libgtk-3-dev
# RUN apt-get install -y python3-dev python3-pip

RUN pip install cmake==3.26.1

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
