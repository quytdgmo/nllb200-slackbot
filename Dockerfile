FROM ubuntu:20.04
#FROM ubuntu:latest
USER root

RUN apt-get update && apt-get install -y software-properties-common \
&& apt-get install -y python3.9 && apt-get install -y python3-pip && pip install --upgrade pip \
&& pip install --upgrade setuptools
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
#RUN pip install --upgrade pip
#RUN pip install --upgrade setuptools

RUN pip install jupyterlab

RUN echo "now building..."

RUN pip install fairscale

RUN echo "Preparing to install nllb"
RUN apt-get update && apt-get -y install gcc && apt-get install -y g++ && apt-get install -y git && git clone https://github.com/facebookresearch/fairseq

RUN cd /fairseq && git checkout nllb && pip install -e .

#RUN git clone https://github.com/pytorch/fairseq

ENV PYTHONPATH="${PYTHONPATH}:/fairseq/"

#RUN cd /fairseq/ && python -m pip install --editable . &&
RUN cd / && apt-get install -y wget && wget --trust-server-names https://tinyurl.com/nllb200densedst600mcheckpoint && git clone https://github.com/google/sentencepiece.git

RUN pip install sentencepiece -q

RUN apt-get install -y cmake && cd /sentencepiece && mkdir /sentencepiece/build && cd /sentencepiece/build && cmake ..

RUN cd /sentencepiece/build && make -j $(nproc)

RUN cd /sentencepiece/build && make -j $(nproc) && make install && ldconfig -v

RUN cd / && git clone https://github.com/pluiez/NLLB-inference && cd /NLLB-inference
