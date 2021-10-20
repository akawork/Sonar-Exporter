FROM python:3.6-slim

RUN apt update && apt install -y build-essential
RUN groupadd --gid 1000 sonar-exporter
RUN useradd --uid 1000 --gid 1000 --create-home sonar-exporter
WORKDIR /home/sonar-exporter
USER sonar-exporter
COPY . .
RUN pip3.6 install -r requirements.txt

EXPOSE 9119
ENTRYPOINT [ "/bin/bash",  "entrypoint.sh" ]
