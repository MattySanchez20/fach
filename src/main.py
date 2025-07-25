import logging
import random
from datetime import datetime
from time import sleep

from jets import F16, F18
from utils import p_by_distance, dogfight

log_filename = f"dogfight_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"logs/{log_filename}",
)

# TODO: this big function can be split into smaller ones
def main():

    logging.info("Initializing jets...")
    fighter1 = F16()
    fighter2 = F18()

    logging.info("Jets initialized successfully.")
    logging.debug(f"{fighter1.name} initial state: {fighter1}")
    logging.debug(f"{fighter2.name} initial state: {fighter2}")

    start_distance = 800
    logging.info(f"Dogfight initiated at a starting distance of {start_distance}")

    for distance in range(start_distance, 0, -5):

        logging.info("FIGHTING......")
        duration = random.uniform(0, 10)
        sleep(duration)
        logging.info(f"Both jets fired cannons for {duration} seconds")

        # TODO: dogfight is not the right word, it should be exchange
        dogfight_details = dogfight(fighter1=fighter1, fighter2=fighter2, distance=distance, duration=duration)
        logging.debug(dogfight_details)

        f1_ammo_left, f1_health_post_hit, f1_hit_bool, f2_damage_inflicted_on_f1 = dogfight_details["fighter1"]
        f2_ammo_left, f2_health_post_hit, f2_hit_bool, f1_damage_inflicted_on_f2 = dogfight_details["fighter2"]

        if f1_health_post_hit <= 0:
            logging.info(f"The {fighter2.name} has destroyed the {fighter1.name}")
            break

        if f2_health_post_hit <= 0:
            logging.info(f"The {fighter1.name} has destroyed the {fighter2.name}")
            break

        if f1_hit_bool:
            logging.info(f"{fighter1.name} post dogfight details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, damage inflicted on opponent={f1_damage_inflicted_on_f2}")
        else:
            logging.info(f"{fighter1.name} post dogfight details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, no damage inflicted on opponent")

        if f2_hit_bool:
            logging.info(f"{fighter2.name} post dogfight details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, damage inflicted on opponent={f2_damage_inflicted_on_f1}")
        else:
            logging.info(f"{fighter2.name} post dogfight details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, no damage inflicted on opponent")

if __name__ == "__main__":
    main()
