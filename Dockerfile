FROM ubuntu:14.04

MAINTAINER Luciano Afranllie <luafran@gmail.com>

LABEL name=the-best version=1.0.0

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libcurl4-openssl-dev \
    libev4 libev-dev python \
    python-dev \
    python-distribute \
    python-pip

# Deploy application
# RUN mkdir /var/log/tornadoservice/
COPY ./dist /tmp/dist
WORKDIR /tmp/dist
RUN pip install thebest-1.0.*.tar.gz && rm -rf /tmp/dist

# Expose port
EXPOSE 10001

# Run app
ENTRYPOINT ["thebest-runservice"]
CMD ["service1", "--port", "10001"]
