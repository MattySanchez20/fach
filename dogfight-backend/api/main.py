from src.scripts.jets import F16, F18
from src.scripts.utils import exchange
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"] for your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dogfight/exchange/{distance}/{duration}")
def exchange_endpoint(distance: int, duration: int):
    fighter1 = F16()
    fighter2 = F18()
    post_exchange = exchange(
        fighter1=fighter1, fighter2=fighter2, distance=distance, duration=duration
    )
    return post_exchange
