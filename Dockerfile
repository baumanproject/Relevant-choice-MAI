FROM python:3

MAINTAINER Alexander Somik

#RUN apt-get -yqq update

#RUN apt-get -yqq install python3 python3-pip


COPY requirements.txt /opt/lib/requirements.txt
COPY config /opt/lib/config
COPY pdf_reader_module /opt/lib/pdf_reader_module

COPY get_amount_GD.py /opt/lib/get_amount_GD.py
COPY run.py /opt/lib/run.py


#ADD home/aquafeet/dep/data /opt/data

WORKDIR /opt/lib

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py","--path", "/opt/lib/config/input_docker.json" ]




