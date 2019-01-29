FROM sd2e/python3:ubuntu17

RUN apt-get update
RUN apt-get install -y libraptor2-dev libjsoncpp1 git

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

RUN pip3 install --upgrade pip

RUN pip3 install --process-dependency-link /opt/scripts/

CMD python3 -m unittest discover /opt/scripts/tests
