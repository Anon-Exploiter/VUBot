FROM alpine:latest 

WORKDIR /root/

ADD vu-alpine ./vu
RUN chmod +x ./vu

ENTRYPOINT [ "./vu" ]
