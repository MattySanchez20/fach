import math
import random
from logging import Logger
from time import sleep

from jets import JetFighter


def _calculate_cannon_spread_area(d_12: float, jet: JetFighter):
    """
    Calculate the cannon spread area at a given distance.

    This is a private helper function that calculates the circular area covered
    by a jet's cannon spread at a specific distance from the target. The spread
    area increases with distance based on the cannon's spread angle.

    Args:
        d_12 (float): Distance between the jet and target
        jet (JetFighter): The jet fighter whose cannon spread is being calculated

    Returns:
        float: The circular area (in square units) covered by the cannon spread

    Note:
        Uses the formula: Area = π * (tan(spread_angle) * distance)²
    """
    # Calculate the radius of the spread circle at the given distance
    spread_radius = math.tan(jet.cannon_spread_rads) * d_12

    # Calculate the circular area using π * r²
    jet_cannon_spread_area = spread_radius**2 * 3.141

    return jet_cannon_spread_area


def p_by_distance(fighter1: JetFighter, fighter2: JetFighter, d_12):
    """
    Calculate hit probabilities for both fighters based on distance.

    Determines the probability of each fighter hitting the other based on the
    relationship between their cannon spread area and the target's cross-sectional area.
    If the cannon spread is smaller than the target, the probability is 1.0 (guaranteed hit).
    Otherwise, the probability is the ratio of target area to spread area.

    Args:
        fighter1 (JetFighter): The first fighter
        fighter2 (JetFighter): The second fighter
        d_12 (float): Distance between the two fighters

    Returns:
        tuple[float, float]: A tuple containing (p_1, p_2) where:
            - p_1 is the probability of fighter1 hitting fighter2
            - p_2 is the probability of fighter2 hitting fighter1
    """
    # Calculate cannon spread areas for both fighters at the given distance
    fighter1_cannon_spread_area = _calculate_cannon_spread_area(d_12=d_12, jet=fighter1)
    fighter2_cannon_spread_area = _calculate_cannon_spread_area(d_12=d_12, jet=fighter2)

    # Get cross-sectional areas (target size) for both fighters
    fighter1_cross_sectional_area = fighter1.calculate_cross_sectional_area()
    fighter2_cross_sectional_area = fighter2.calculate_cross_sectional_area()

    # Calculate probability for fighter1 hitting fighter2
    # If spread area is smaller than target, guaranteed hit (probability = 1.0)
    if fighter1_cannon_spread_area <= fighter2_cross_sectional_area:
        p_1 = float(1)
    else:
        # Otherwise, probability is ratio of target area to spread area
        p_1 = float(fighter2_cross_sectional_area / fighter1_cannon_spread_area)

    # Calculate probability for fighter2 hitting fighter1 (same logic)
    if fighter2_cannon_spread_area <= fighter1_cross_sectional_area:
        p_2 = float(1)
    else:
        p_2 = float(fighter1_cross_sectional_area / fighter2_cannon_spread_area)

    return (p_1, p_2)


def hit_or_miss(p_1: float, p_2: float):
    """
    Determine if each fighter hits their target based on probabilities.

    Uses random number generation to simulate the uncertainty of combat.
    Each fighter gets a random number between 0 and 1, and hits if their
    probability is greater than or equal to their random number.

    Args:
        p_1 (float): Probability of fighter 1 hitting fighter 2 (0.0 to 1.0)
        p_2 (float): Probability of fighter 2 hitting fighter 1 (0.0 to 1.0)

    Returns:
        tuple[bool, bool]: A tuple containing (f1_hit, f2_hit) where:
            - f1_hit is True if fighter 1 hits fighter 2
            - f2_hit is True if fighter 2 hits fighter 1
    """
    # Generate random numbers for each fighter (0.0 to 1.0)
    f1_zero_to_one_rand_float = random.uniform(0, 1)
    f2_zero_to_one_rand_float = random.uniform(0, 1)

    # Initialize hit status as False
    f1_hit = False
    f2_hit = False

    # Fighter 1 hits if their probability exceeds their random number
    if p_1 >= f1_zero_to_one_rand_float:
        # f1 hit f2
        f1_hit = True

    # Fighter 2 hits if their probability exceeds their random number
    if p_2 >= f2_zero_to_one_rand_float:
        # f2 hit f1
        f2_hit = True

    return f1_hit, f2_hit


def exchange(fighter1: JetFighter, fighter2: JetFighter, distance, duration):
    """
    Simulate a single combat exchange between two jet fighters.

    This function represents one round of combat where both fighters simultaneously:
    1. Calculate their hit probabilities based on distance
    2. Determine if they hit each other using random chance
    3. Expend ammunition by firing for the given duration
    4. Apply damage if a hit occurred

    Args:
        fighter1 (JetFighter): The first fighter in the exchange
        fighter2 (JetFighter): The second fighter in the exchange
        distance (float): Distance between the fighters
        duration (float): Duration of the firing exchange

    Returns:
        dict: Combat results containing:
            - "fighter1": [ammo_remaining, health_remaining, hit_target, damage_received]
            - "fighter2": [ammo_remaining, health_remaining, hit_target, damage_inflicted]

    Note:
        This represents a 1v1 single exchange simulation where both fighters
        can potentially hit each other simultaneously.
    """
    # Calculate hit probabilities based on current distance
    p_1, p_2 = p_by_distance(fighter1=fighter1, fighter2=fighter2, d_12=distance)

    # Determine if each fighter hits their target using random chance
    f1_hit_bool, f2_hit_bool = hit_or_miss(p_1=p_1, p_2=p_2)

    # Both fighters expend ammunition by firing for the duration
    f1_ammo_left = fighter1.shoot(duration=duration)
    f2_ammo_left = fighter2.shoot(duration=duration)

    # Process fighter1's attack on fighter2
    if f1_hit_bool:
        # Calculate damage based on fighter1's weapons and firing duration
        f1_damage_inflicted_on_f2 = fighter1.calculate_damage(duration=duration)

        # Apply damage to fighter2's health
        f2_health_post_hit = fighter2.deduct_health(damage=f1_damage_inflicted_on_f2)
    else:  # Fighter1 missed
        f1_damage_inflicted_on_f2 = 0
        f2_health_post_hit = fighter2.health

    # Process fighter2's attack on fighter1
    if f2_hit_bool:
        # Calculate damage based on fighter2's weapons and firing duration
        f2_damage_inflicted_on_f1 = fighter2.calculate_damage(duration=duration)

        # Apply damage to fighter1's health
        f1_health_post_hit = fighter1.deduct_health(damage=f2_damage_inflicted_on_f1)
    else:  # Fighter2 missed
        f2_damage_inflicted_on_f1 = 0
        f1_health_post_hit = fighter1.health

    # Return comprehensive combat results for both fighters
    return {
        "fighter1": [
            f1_ammo_left,  # Remaining ammunition
            f1_health_post_hit,  # Health after taking damage
            f1_hit_bool,  # Whether this fighter hit the opponent
            f2_damage_inflicted_on_f1,  # Damage received from opponent
        ],
        "fighter2": [
            f2_ammo_left,  # Remaining ammunition
            f2_health_post_hit,  # Health after taking damage
            f2_hit_bool,  # Whether this fighter hit the opponent
            f1_damage_inflicted_on_f2,  # Damage received from opponent
        ],
    }


def dogfight(
    fighter1: JetFighter,
    fighter2: JetFighter,
    logger: Logger,
    start_distance: int = 1000,
    step_size: int = -50,
    max_exchange_duration: int = 10,
):
    # Log detailed initial state for debugging purposes
    logger.info(f"{fighter1.name} Jet Specs: {fighter1}")
    logger.info(f"{fighter2.name} Jet Specs: {fighter2}")

    logger.info(f"Dogfight initiated at a starting distance of {start_distance}...")

    # looping through exchanges at closer and closer distances
    for distance in range(start_distance, 0, step_size):
        # Signal start of combat exchange at current distance
        logger.info("FIGHTING......")

        # Generate random firing duration (0-10 seconds) to simulate variable engagement
        duration = random.uniform(0, max_exchange_duration)

        # Add realistic delay to simulate combat duration
        sleep(duration)

        # Log the combat parameters for this exchange
        logger.info(
            f"Both jets fired cannons for {duration} seconds at a distance of {distance}..."
        )

        # Execute the combat exchange using the utils.exchange function
        # This calculates hit probabilities, determines hits/misses, and applies damage
        exchange_details = exchange(
            fighter1=fighter1, fighter2=fighter2, distance=distance, duration=duration
        )
        # Log detailed exchange results for debugging
        logger.debug(exchange_details)

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
            logger.info(f"The {fighter2.name} has destroyed the {fighter1.name}.")
            break

        # Check victory conditions - Fighter2 destroyed
        if f2_health_post_hit <= 0:
            logger.info(f"The {fighter1.name} has destroyed the {fighter2.name}.")
            break

        # Check escape conditions - Fighter1 out of ammunition
        if f1_ammo_left == 0:
            logger.info(
                f"The {fighter1.name} has run out of ammo. It puts on the afterburners and escapes."
            )
            break

        # Check escape conditions - Fighter2 out of ammunition
        if f2_ammo_left == 0:
            logger.info(
                f"The {fighter2.name} has run out of ammo. It puts on the afterburners and escapes."
            )
            break

        # Log Fighter1 post-exchange status with hit/miss information
        if f1_hit_bool:
            # Fighter1 successfully hit Fighter2 - log damage inflicted
            logger.info(
                f"{fighter1.name} post exchange details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, damage inflicted on opponent={f1_damage_inflicted_on_f2}..."
            )
        else:
            # Fighter1 missed Fighter2 - no damage inflicted
            logger.info(
                f"{fighter1.name} post exchange details: health={f1_health_post_hit}, cannon ammo={f1_ammo_left}, no damage inflicted on opponent..."
            )

        # Log Fighter2 post-exchange status with hit/miss information
        if f2_hit_bool:
            # Fighter2 successfully hit Fighter1 - log damage inflicted
            logger.info(
                f"{fighter2.name} post exchange details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, damage inflicted on opponent={f2_damage_inflicted_on_f1}..."
            )
        else:
            # Fighter2 missed Fighter1 - no damage inflicted
            logger.info(
                f"{fighter2.name} post exchange details: health={f2_health_post_hit}, cannon ammo={f2_ammo_left}, no damage inflicted on opponent..."
            )
