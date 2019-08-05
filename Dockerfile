FROM python:3.6-slim

WORKDIR /root/
COPY . .
RUN pip3.6 install -r requirements.txt

EXPOSE 9119
ENTRYPOINT [ "/bin/bash",  "entrypoint.sh" ]
