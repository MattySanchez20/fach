import math
from abc import ABC, abstractmethod


class JetFighter(ABC):

    def __init__(
        self,
        name,
        health,
        cannon_ammo,
        fire_rate,
        wingspan,
        damage_per_round,
        cannon_spread_rads,
    ):
        self.name = name
        self.health = health
        self.cannon_ammo = cannon_ammo
        self.fire_rate = fire_rate
        self.wingspan = wingspan
        self.damage_per_round = damage_per_round
        self.cannon_spread_rads = cannon_spread_rads

    @abstractmethod
    def shoot(self, duration: float):
        pass

    @abstractmethod
    def deduct_health(self, damage):
        pass

    @abstractmethod
    def add_health(self):
        pass

    @abstractmethod
    def obtain_health(self):
        pass

    @abstractmethod
    def calculate_cross_sectional_area(self):
        pass

    @abstractmethod
    def calculate_damage(self, duration):
        pass

    def __str__(self):
        return str(
            {
                "Jet Fighter": f"{self.name}",
                "Health": f"{self.health}%",
                "Cannon Ammo": f"{self.cannon_ammo}",
                "Fire Rate": f"{self.fire_rate} rounds/sec",
                "Wingspan": f"{self.wingspan} meters",
                "Damage per Round": f"{self.damage_per_round * 100}%",
                "Cannon Spread": f"{math.degrees(self.cannon_spread_rads):.2f} degrees",
            }
        )


class F16(JetFighter):

    def __init__(self):
        super().__init__(
            name="F16",
            health=100,
            cannon_ammo=100000000,
            fire_rate=80,
            wingspan=45,
            damage_per_round=5 / 100,
            cannon_spread_rads=math.radians(4),
        )

    def shoot(self, duration: float):
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        return self.cannon_ammo

    def deduct_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        return self.health

    def add_health(self, health_points):
        self.health += health_points

        return self.health

    def obtain_health(self):
        return self.health

    def calculate_cross_sectional_area(self):
        cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

        return cross_sectional_area

    def calculate_damage(self, duration):
        return duration * self.fire_rate * self.damage_per_round

class F18(JetFighter):

    def __init__(self):
        super().__init__(
            name="F18",
            health=100,
            cannon_ammo=100000000,
            fire_rate=50,
            wingspan=50,
            damage_per_round=30 / 100,
            cannon_spread_rads=math.radians(6),
        )

    def shoot(self, duration: float):
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        return self.cannon_ammo

    def deduct_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        return self.health

    def add_health(self, health_points):
        self.health += health_points

        return self.health

    def obtain_health(self):
        return self.health

    def calculate_cross_sectional_area(self):
        cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

        return cross_sectional_area

    def calculate_damage(self, duration):
        return duration * self.fire_rate * self.damage_per_round
