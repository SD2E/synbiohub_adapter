FROM sd2e/python2:ubuntu16

RUN apt-get update
RUN apt-get install -y libraptor2-dev

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

RUN pip install -r /opt/scripts/requirements.txt

# custom wheel for Ubuntu
RUN pip install https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_2/dist/pySBOL-2.3.0.post11-py2-none-any.whl?raw=true

CMD python -m unittest discover /opt/scripts/tests