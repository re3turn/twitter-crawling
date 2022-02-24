FROM python:3.10 as builder

WORKDIR /app

COPY api/requirements.txt /app
RUN pip3 install -r requirements.txt


FROM python:3.10-slim as service
WORKDIR /api
ENV PYTHON_VERSION 3.10
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

COPY api/src /api/src
COPY api/run.py /api

EXPOSE 8000

ENTRYPOINT ["python", "/api/run.py"]
