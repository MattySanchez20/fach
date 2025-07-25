import logging
import random
from datetime import datetime
from time import sleep

from jets import F16, F18
from utils import p_by_distance, dogfight

log_filename = f"dogfight_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"logs/{log_filename}",
)

# TODO: this big function can be split into smaller ones
def main():

    logging.info("Initializing jets...")
    f16 = F16()
    f18 = F18()

    logging.info("Jets initialized successfully.")
    logging.debug(f"F16 initial state: {f16}")
    logging.debug(f"F18 initial state: {f18}")

    start_distance = 800
    logging.info(f"Dogfight initiated at a starting distance of {start_distance}")

    for distance in range(start_distance, 0, -5):

        duration = random.uniform(0, 10)
        sleep(duration)
        logging.info(f"Both jets fired cannons for {duration} seconds")
        dogfight_details = dogfight(fighter1=f16, fighter2=f18, distance=distance, duration=duration)

        logging.debug(dogfight_details)

if __name__ == "__main__":
    main()
