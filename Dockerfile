FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN pip3 install virtualenv
RUN python3 -m virtualenv .venv

COPY requirements.txt /app/

SHELL ["/bin/bash", "-c"]
RUN source /app/.venv/bin/activate && pip3 install -r requirements.txt

COPY *.py /app/
COPY *.ini /app/
COPY service.sh /app/

CMD /app/service.sh
