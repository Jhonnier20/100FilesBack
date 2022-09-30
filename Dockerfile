# Ubuntu image of 20.04
FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

# Install git
RUN apt update

WORKDIR /app
COPY . .

# Python configuration
RUN apt install -y python3-pip
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt install -y python3-venv
RUN apt install python3-waitress

RUN ls
RUN pip3 install -r requirements.txt

RUN pip3 install -e .
RUN pip list
RUN pip3 install wheel
RUN pip3 install waitress
RUN python3 setup.py bdist_wheel

# CMD [ "waitress-serve", "--port=2010", "--call 'flaskr:create_app'" ]
# ENTRYPOINT ["waitress-serve", "Yo, Entrypoint!!"]
#CMD [ "waitress-serve --port=2010 --call flaskr:create_app" ]
RUN ls
COPY deploy.sh ./
CMD ["sh","deploy.sh"]
# CMD ["flask", "--app flaskr --debug run"]

## docker run -d -p 5000:5000 python-docker

# RUN pip install --no-cache-dir -r requirements.txt
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]% 