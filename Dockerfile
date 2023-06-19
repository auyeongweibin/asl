# syntax=docker/dockerfile:1

FROM python3.9-nodejs16-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN npm install

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]