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

WORKDIR /

EXPOSE 6060

RUN git clone https://github.com/thammegowda/nllb-serve && cd /nllb-serve && pip3 install -e .

ENV PATH "$PATH:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

CMD ["/bin/bash","-c","cd /nllb-serve && python3 -m nllb_serve"]
