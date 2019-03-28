FROM sd2e/python3:ubuntu17

RUN apt-get update
RUN apt-get install -y libraptor2-dev libjsoncpp1 git

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

RUN python3 setup.py install

CMD python3 -m unittest discover /opt/scripts/tests
