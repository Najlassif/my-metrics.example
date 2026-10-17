
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

EMAIL = "22f3000259@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-be6mty.example.com"

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = (
        f"{time.perf_counter() - start:.6f}"
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Statistics API is running"}


@app.get("/stats")
def stats(values: str):
    try:
        numbers = [
            int(value.strip())
            for value in values.split(",")
        ]

        if not numbers:
            raise ValueError("No numbers")

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Provide comma-separated integers"
        )

    total = sum(numbers)

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers)
    }
