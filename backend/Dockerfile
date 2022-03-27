FROM python:3.10.4-slim as base

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

###############################################################################
###############################################################################

FROM base as dev

COPY ./requirements.dev.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.dev.txt

COPY ./src/api /app/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]

###############################################################################
###############################################################################

FROM dev as test

COPY ./test /app/test

CMD ["ptw"]  # runs pytest-watch
