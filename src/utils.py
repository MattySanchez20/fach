import math
import random

from jets import JetFighter


def _calculate_cannon_spread_area(d_12: float, jet: JetFighter):

    jet_cannon_spread_area = (math.tan(jet.cannon_spread_rads) * d_12) ** 2 * 3.141

    return jet_cannon_spread_area


def p_by_distance(fighter1: JetFighter, fighter2: JetFighter, d_12):

    fighter1_cannon_spread_area = _calculate_cannon_spread_area(d_12=d_12, jet=fighter1)
    fighter2_cannon_spread_area = _calculate_cannon_spread_area(d_12=d_12, jet=fighter2)

    fighter1_cross_sectional_area = fighter1.calculate_cross_sectional_area()
    fighter2_cross_sectional_area = fighter2.calculate_cross_sectional_area()

    if fighter1_cannon_spread_area <= fighter2_cross_sectional_area:
        p_1 = float(1)
    else:
        p_1 = float(fighter2_cross_sectional_area / fighter1_cannon_spread_area)

    if fighter2_cannon_spread_area <= fighter1_cross_sectional_area:
        p_2 = float(1)
    else:
        p_2 = float(fighter1_cross_sectional_area / fighter2_cannon_spread_area)

    return (p_1, p_2)

def hit_or_miss(p_1: float, p_2: float):
    f1_zero_to_one_rand_float = random.uniform(0, 1)
    f2_zero_to_one_rand_float = random.uniform(0, 1)
    
    f1_hit = False
    f2_hit = False

    if p_1 >= f1_zero_to_one_rand_float:
        # f1 hit f2
        f1_hit = True

    if p_2 >= f2_zero_to_one_rand_float:
        # f2 hit f1
        f2_hit = True

    return f1_hit, f2_hit


def dogfight(fighter1: JetFighter, fighter2: JetFighter, distance, duration):
    """1 V 1 A Single Exchange"""

    # obtain probabilities for given distance
    p_1, p_2 = p_by_distance(fighter1=fighter1, fighter2=fighter2, d_12=distance)

    # add if statement to check for hit or miss
    f1_hit_bool, f2_hit_bool = hit_or_miss(p_1=p_1, p_2=p_2)

    # shoot cannons
    f1_ammo_left = fighter1.shoot(duration=duration)
    f2_ammo_left = fighter2.shoot(duration=duration)

    # has fighter1 hit fighter2?
    if f1_hit_bool:

        f1_damage_inflicted_on_f2 = fighter1.calculate_damage(duration=duration)

        f2_health_post_hit = fighter2.deduct_health(damage=f1_damage_inflicted_on_f2)
    else: # no hit
        f1_damage_inflicted_on_f2 = 0
        f2_health_post_hit = fighter2.health

    # has fighter2 hit fighter1?
    if f2_hit_bool:

        f2_damage_inflicted_on_f1 = fighter2.calculate_damage(duration=duration)

        f1_health_post_hit = fighter1.deduct_health(damage=f2_damage_inflicted_on_f1)
    else: # no hit
        f2_damage_inflicted_on_f1 = 0
        f1_health_post_hit = fighter1.health

    return {
        "fighter1": [f1_ammo_left, f1_health_post_hit, f1_hit_bool, f2_damage_inflicted_on_f1],
        "fighter2": [f2_ammo_left, f2_health_post_hit, f2_hit_bool, f1_damage_inflicted_on_f2],
    }
