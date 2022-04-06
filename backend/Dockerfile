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

COPY ./belay_me /app/belay_me

CMD ["uvicorn", "belay_me.api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

###############################################################################
###############################################################################

FROM dev as test

COPY ./test /app/test
COPY ./setup.py /app/

RUN pip install -e .

CMD ["ptw"]  # runs pytest-watch
