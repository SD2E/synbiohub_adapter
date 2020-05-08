FROM sd2e/python3:ubuntu17

RUN apt-get update
RUN apt-get install -y libraptor2-dev libjsoncpp1 git

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

# built-in pip is ancient
RUN pip install --upgrade pip
# nuke all existing packages in the image
# ensure we only get the packages we want per the SBH setup.py
RUN pip freeze | xargs pip uninstall -y || true
RUN pip install .

CMD python3 -m unittest discover /opt/scripts/tests
