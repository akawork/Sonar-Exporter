FROM python:3.6-slim

WORKDIR /root/

COPY . .

RUN pip3.6 install -r requirements.txt

EXPOSE 9119
ENV SONAR_CONFIG_FILE="config/sonar_config.ini"
ENV DEBUG=0

ENTRYPOINT [ "python3.6",  "./sonar_exporter.py" ]