FROM sd2e/python3:ubuntu16

RUN apt-get update
RUN apt-get install -y libraptor2-dev libjsoncpp1

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

RUN pip3 install --upgrade pip

RUN pip3 install -r /opt/scripts/requirements.txt

# custom wheel for Ubuntu
RUN pip3 install https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-py3-none-any.whl?raw=true

RUN apt-get install -y wget

#TODO remove manual dependency
RUN wget https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/libsbol.so\?raw\=true -O libsbol.so

#TODO remove manual dependency
RUN mv libsbol.so /usr/local/lib

RUN ldconfig -v

CMD python3 -m unittest discover /opt/scripts/tests
