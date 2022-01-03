from ubuntu

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN apt-get -y install python3-pip
RUN apt install -y git gcc libc-dev
RUN apt install -y gcc g++ make libffi-dev python3-dev
RUN apt install -y build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev tox lcov valgrind

RUN pip3 install gunicorn
RUN pip3 install ipdb
RUN pip3 install ipython

WORKDIR /app

RUN git clone https://github.com/Full-Tortuga/decide-full-tortuga-autenticacion.git .
RUN pip3 install -r requirements.txt


WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py

RUN ./manage.py collectstatic

CMD ["gunicorn", "-w 5", "decide.wsgi", "--timeout=500", "-b 0.0.0.0:80"]
