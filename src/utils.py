import math
import random

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
