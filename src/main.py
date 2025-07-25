import logging
import random
from datetime import datetime
from time import sleep

from jets import F16, F18
from utils import exchange

# Generate unique log filename with timestamp for this dogfight session
log_filename = f"dogfight_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Configure logging to write detailed combat information to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"logs/{log_filename}",
)


# TODO: allow dogfights between more than 2 fighters
def main():
    """
    Execute a complete dogfight simulation between an F16 and F18.

    This function orchestrates the entire combat simulation by:
    1. Initializing two fighter jets (F16 vs F18)
    2. Starting combat at maximum range and closing distance
    3. Processing combat exchanges at each range increment
    4. Monitoring for victory conditions (health, ammo depletion)
    5. Logging all combat events for analysis

    The simulation uses a decreasing distance model where fighters
    start at long range and progressively close to engage in combat.
    Each exchange involves probability-based hit calculations and
    damage application.

    Victory Conditions:
    - Fighter destroyed (health <= 0)
    - Fighter runs out of ammunition

    Note:
        All combat events are logged to a timestamped file in the logs directory.
    """

    # Initialize the two competing fighter jets
    logging.info("Initializing jets...")
    fighter1 = F16()  # First fighter: F-16 Fighting Falcon
    fighter2 = F18()  # Second fighter: F/A-18 Hornet

    # Log successful initialization with fighter specifications
    logging.info(f"{fighter1.name} initialized successfully. Jet Specs: {fighter1}")
    logging.info(f"{fighter2.name} initialized successfully. Jet Specs: {fighter2}")

    # Log detailed initial state for debugging purposes
    logging.debug(f"{fighter1.name} initial state: {fighter1}")
    logging.debug(f"{fighter2.name} initial state: {fighter2}")

    # Set initial engagement distance (700 units - long range combat start)
    start_distance = 700
    logging.info(f"Dogfight initiated at a starting distance of {start_distance}...")

    # Main combat loop: fighters close distance in 50-unit increments
    # Combat continues until one fighter is destroyed or runs out of ammo
    for distance in range(start_distance, 0, -50):

        # Signal start of combat exchange at current distance
        logging.info("FIGHTING......")

        # Generate random firing duration (0-10 seconds) to simulate variable engagement
        duration = random.uniform(0, 10)

        # Add realistic delay to simulate combat duration
        sleep(duration)

        # Log the combat parameters for this exchange
        logging.info(
            f"Both jets fired cannons for {duration} seconds at a distance of {distance}..."
        )

        # Execute the combat exchange using the utils.exchange function
        # This calculates hit probabilities, determines hits/misses, and applies damage
        exchange_details = exchange(
            fighter1=fighter1, fighter2=fighter2, distance=distance, duration=duration
        )
        # Log detailed exchange results for debugging
        logging.debug(exchange_details)

        # Unpack combat results for both fighters
        # Fighter1 results: [ammo_remaining, health_after_damage, hit_opponent, damage_received]
        f1_ammo_left, f1_health_post_hit, f1_hit_bool, f2_damage_inflicted_on_f1 = (
            exchange_details["fighter1"]
        )
        # Fighter2 results: [ammo_remaining, health_after_damage, hit_opponent, damage_received]
        f2_ammo_left, f2_health_post_hit, f2_hit_bool, f1_damage_inflicted_on_f2 = (
            exchange_details["fighter2"]
        )

        # Check victory conditions - Fighter1 destroyed
        if f1_health_post_hit <= 0:
            logging.info(f"The {fighter2.name} has destroyed the {fighter1.name}.")
            break

        # Check victory conditions - Fighter2 destroyed
        if f2_health_post_hit <= 0:
            logging.info(f"The {fighter1.name} has destroyed the {fighter2.name}.")
            break

        # Check escape conditions - Fighter1 out of ammunition
        if f1_ammo_left == 0:
            logging.info(
                f"The {fighter1.name} has run out of ammo. It puts on the afterburners and escapes."
            )
            break

        # Check escape conditions - Fighter2 out of ammunition
        if f2_ammo_left == 0:
            logging.info(
                f"The {fighter2.name} has run out of ammo. It puts on the afterburners and escapes."
            )
            break

        # Log Fighter1 post-exchange status with hit/miss information
        if f1_hit_bool:
            # Fighter1 successfully hit Fighter2 - log damage inflicted
            logging.info(
                f"{fighter1.name} post exchange details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, damage inflicted on opponent={f1_damage_inflicted_on_f2}..."
            )
        else:
            # Fighter1 missed Fighter2 - no damage inflicted
            logging.info(
                f"{fighter1.name} post exchange details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, no damage inflicted on opponent..."
            )

        # Log Fighter2 post-exchange status with hit/miss information
        if f2_hit_bool:
            # Fighter2 successfully hit Fighter1 - log damage inflicted
            logging.info(
                f"{fighter2.name} post exchange details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, damage inflicted on opponent={f2_damage_inflicted_on_f1}..."
            )
        else:
            # Fighter2 missed Fighter1 - no damage inflicted
            logging.info(
                f"{fighter2.name} post exchange details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, no damage inflicted on opponent..."
            )


if __name__ == "__main__":
    main()
