import random
from utils import p_by_distance
from jets import F16, F18
from time import sleep

f16 = F16()
f18 = F18()

def main():

    start_distance = 100

    for distance in range(start_distance, 0, -25):
        zero_to_one_rand_attacker = random.uniform(0, 1)
        zero_to_one_rand_defender = random.uniform(0, 1)

        eng_duration_secs = random.uniform(0, 10)

        p_a, p_b = p_by_distance(attacker=f16, defender=f18, d_ab=distance)

        print("\nFIGHTING.................")
        sleep(eng_duration_secs)

        print(f"\nDogfight details:\ndistance={distance}\nduration={eng_duration_secs}")

        if p_b >= zero_to_one_rand_defender:

            print("F18 has hit the F16")
            
            f16_damage_incurred = f18.damage_per_round * f18.fire_rate * eng_duration_secs

            f16.deduct_health(damage=f16_damage_incurred)

        if p_a >= zero_to_one_rand_attacker:
            
            print("F16 has hit the f18")

            f18_damage_incurred = f16.damage_per_round * f16.fire_rate * eng_duration_secs

            f18.deduct_health(damage=f18_damage_incurred)

        f16_health_post_engagement = f16.obtain_health()
        f18_health_post_engagement = f18.obtain_health()

        print(f"F16 Health: {f16_health_post_engagement}")
        print(f"F18 Health: {f18_health_post_engagement}")


if __name__=="__main__":
    main()