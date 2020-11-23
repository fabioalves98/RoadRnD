FROM python:3.8


COPY requirements.txt .
RUN pip install -r requirements.txt

ADD payment_service src/payment_service
COPY *.py src/

WORKDIR /src
CMD [ "python", "./run.py" ] 