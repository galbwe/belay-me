from typing import Dict, List

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/healthcheck")
def healthcheck() -> str:
    return "OK"


@app.get("/api/v1/users")
def get_users() -> Dict[str, List]:
    return {"users": ["user1", "user2"]}
