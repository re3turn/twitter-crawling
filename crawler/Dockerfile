FROM python:3.10 as builder

WORKDIR /app

COPY requirements.lock /app
RUN pip3 install -r requirements.lock


FROM python:3.10-slim as service
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY app /service
COPY run.py /service

ENTRYPOINT ["python", "/service/run.py"]
