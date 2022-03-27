FROM python:3.10.4-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
