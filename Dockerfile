FROM alpine:latest 

WORKDIR /root/

RUN apk update && \
    apk add python3 py3-pip

ADD requirements.txt vu.py .
RUN pip3 install -r requirements.txt

RUN chmod +x vu.py

ENTRYPOINT [ "./vu.py" ]
