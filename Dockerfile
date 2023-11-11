FROM ubuntu:22.04
WORKDIR /app/
EXPOSE 8000
RUN apt -y update && apt -y upgrade && apt install -y python3 python3-pip netcat mysql-client
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .