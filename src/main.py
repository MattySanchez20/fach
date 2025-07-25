import random
from time import sleep

from jets import F16, F18
from utils import p_by_distance
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/dogfight.log"
)

def main():

    logging.info("Initializing jets...")
    f16 = F16()
    f18 = F18()

    logging.info("Jets initialized successfully.")
    logging.debug(f"F16 initial state: {f16}")
    logging.debug(f"F18 initial state: {f18}")

    start_distance = 1024
    logging.info(f"Dogfight initiated at a starting distance of {start_distance}")

    for distance in range(start_distance, 0, -8):

        logging.info(f"They engage at a distance of {distance}")
        logging.debug(f"Current engagement distance: {distance}")

        zero_to_one_rand_attacker = random.uniform(0, 1)
        zero_to_one_rand_defender = random.uniform(0, 1)

        logging.debug(f"Random cannon hit numbers generated: Attacker={zero_to_one_rand_attacker}, Defender={zero_to_one_rand_defender}")

        eng_duration_secs = random.uniform(0, 10)
        logging.info(f"They each fire their cannons for {eng_duration_secs:.2f} seconds")
        sleep(eng_duration_secs)
        
        p_a, p_d = p_by_distance(attacker=f16, defender=f18, d_ab=distance)
        
        logging.debug(f"Probabilities of the attacker hitting defender is {p_a:.4f}, and defender hitting attacker is {p_d:.4f}")

        # shoot and obtain damage
        # TODO: damage is only inflicted if it hits target
        f18_damage_to_f16 = f18.shoot(eng_duration_secs)
        f16_damage_to_f18 = f16.shoot(eng_duration_secs)

        if p_d >= zero_to_one_rand_defender:
            logging.info("F18 has hit the F16!")
            logging.debug(f"F18 damage to F16: {f18_damage_to_f16}")
            f16.deduct_health(damage=f18_damage_to_f16)
        else:
            logging.info("F18 has missed!")

        if p_a >= zero_to_one_rand_attacker:
            logging.info("F16 has hit the F18!")
            logging.debug(f"F16 damage to F18: {f16_damage_to_f18}")
            f18.deduct_health(damage=f16_damage_to_f18)
        else:
            logging.info("F16 has missed!")

        f16_health_post_engagement = f16.obtain_health()
        f18_health_post_engagement = f18.obtain_health()

        logging.info(f"F16's health after engagement: {f16_health_post_engagement}")
        logging.info(f"F18's health after engagement: {f18_health_post_engagement}")
        logging.debug(f"Post-engagement states: F16={f16}, F18={f18}")

        if f16_health_post_engagement <= 0 or f18_health_post_engagement <= 0:
            logging.info("One of the jets has been destroyed. Ending dogfight.")
            break

    logging.info("Dogfight simulation completed.")

if __name__ == "__main__":
    main()
