# syntax=docker/dockerfile:1

FROM python:3.9.16-slim

RUN pip install --upgrade pip

WORKDIR /app

# setup dependencies
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y nodejs npm

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY package.json package.json
RUN npm install

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000