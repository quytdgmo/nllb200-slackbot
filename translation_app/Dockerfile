FROM ubuntu:20.04

RUN apt-get update && apt-get install -y software-properties-common \
&& apt-get install -y python3.9 && apt-get install -y python3-pip \
&& pip install --upgrade pip \
&& pip install --upgrade setuptools \
&& apt-get install -y git

RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV SLACK_API_TOKEN xoxb-2523231391122-4568907382871-9is0JMh7wbI8soY9ZRCebJhc

WORKDIR /app
COPY ./translation_app/ /app
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

CMD ["/bin/bash","-c","cd /app && python3 /app/app.py"]
