import math
import random
from time import sleep

from jets import JetFighter


def p_by_distance(attacker: JetFighter, defender: JetFighter, d_ab):

    attacker_cannon_spread_area = (
        math.tan(attacker.cannon_spread_rads) * d_ab
    ) ** 2 * 3.141
    defender_cannon_spread_area = (
        math.tan(defender.cannon_spread_rads) * d_ab
    ) ** 2 * 3.141

    if attacker_cannon_spread_area <= defender.cross_sectional_area:
        p_a = float(1)
    else:
        p_a = float(defender.cross_sectional_area / attacker_cannon_spread_area)

    if defender_cannon_spread_area <= attacker.cross_sectional_area:
        p_d = float(1)
    else:
        p_d = float(attacker.cross_sectional_area / defender_cannon_spread_area)

    return (p_a, p_d)


def dogfight(attacker: JetFighter, defender: JetFighter):

    # pick a random number between 0 and 1 for each pilot
    zero_to_one_rand_attacker = random.uniform(0, 1)
    zero_to_one_rand_defender = random.uniform(0, 1)

    distance_rand = random.uniform(0, 1000)

    eng_duration_secs = random.uniform(0, 10)

    p_a, p_b = p_by_distance(attacker=attacker, defender=defender, d_ab=distance_rand)

    print("\nFIGHTING.................")
    sleep(eng_duration_secs)

    print(
        f"\nDogfight details:\ndistance={distance_rand}\nduration={eng_duration_secs}"
    )

    if p_b >= zero_to_one_rand_defender:

        attacker.health -= attacker.fire_rate * eng_duration_secs

        print(f"B52 has hit the F16")
        print(f"F16's health reduced to {attacker.health}%")

    if p_a >= zero_to_one_rand_attacker:

        defender.health -= defender.fire_rate * eng_duration_secs

        print("F16 has hit the B52")
        print(f"B52's health reduced to {defender.health}%")
