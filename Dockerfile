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
RUN apt-get install -y build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev tox lcov valgrind
RUN apt-get install -y libpq-dev
RUN apt-get install ldap-utils

RUN pip3 install gunicorn
RUN pip3 install ipdb
RUN pip3 install ipython
RUN pip install psycopg2

WORKDIR /app

RUN git clone https://github.com/Full-Tortuga/decide-full-tortuga-visualizacion.git .
RUN pip3 install -r requirements.txt


WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py

ADD ./.env /app/decide

RUN ./manage.py collectstatic

CMD ./manage.py runserver 0.0.0.0:$PORT
