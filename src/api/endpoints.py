from fastapi import APIRouter

from scripts.jets import F16, F18
from scripts.utils import exchange

router = APIRouter()


@router.get("/dogfight/exchange/{distance}/{duration}")
def exchange_endpoint(distance: int, duration: int):
    fighter1 = F16()
    fighter2 = F18()
    post_exchange = exchange(
        fighter1=fighter1, fighter2=fighter2, distance=distance, duration=duration
    )
    return post_exchange
