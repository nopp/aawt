FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
		&& apk add py-pip git bash \
		&& git clone https://github.com/nopp/aawt.git \
		&& cd aawt \
		&& pip install -r requirements.txt \
		&& mkdir /etc/aawt \
		&& mv /aawt/config.cfg /etc/aawt/config.cfg 

WORKDIR /aawt

COPY run.sh /aawt

RUN chmod +x /aawt/run.sh

EXPOSE 8082

ENTRYPOINT ["./run.sh"]
