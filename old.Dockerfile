# Ubuntu image of 20.04
FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

# Install git
RUN apt-get update
RUN apt-get update --fix-missing

WORKDIR /app
COPY . .

# Python configuration
RUN apt install -y python3-pip
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt install -y python3-venv
RUN apt install -y python3-waitress

RUN ls
RUN pip3 install -r requirements.txt

RUN pip3 install -e .
RUN pip list
RUN pip3 install wheel
RUN pip3 install waitress
RUN python3 setup.py bdist_wheel


RUN ls
COPY deploy.sh ./
CMD ["sh","deploy.sh"]