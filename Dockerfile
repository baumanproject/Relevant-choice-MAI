FROM python:3

MAINTAINER Alexander Somik

#RUN apt-get -yqq update

#RUN apt-get -yqq install python3 python3-pip


COPY requirements.txt /opt/lib/requirements.txt
COPY config /opt/lib/config
COPY pdf_reader_module /opt/lib/pdf_reader_module

COPY get_amount_GD.py /opt/lib/get_amount_GD.py
COPY parsing.py /opt/lib/parsing.py
COPY arxiv_api /opt/lib/arxiv_api
COPY api.py /opt/lib/api.py

WORKDIR /opt/lib

RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3.7"]
CMD ["api.py","--path","/opt/lib/config/input_docker.json"]




