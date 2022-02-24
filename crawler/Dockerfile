FROM python:3.10 as builder

WORKDIR /app

COPY crawler/requirements.txt /app
RUN pip3 install -r requirements.txt


FROM python:3.10-slim as service
WORKDIR /crawler
ENV PYTHON_VERSION 3.10
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

COPY crawler/app /crawler/app
COPY crawler/run.py /crawler

ENTRYPOINT ["python", "/crawler/run.py"]
