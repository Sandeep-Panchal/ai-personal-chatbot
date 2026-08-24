from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from collections.abc import Iterable

app = FastAPI()

@app.post("/api", response_class=StreamingResponse)
def stream(text: str) -> Iterable[str]:

    for i in text.split():
        yield i