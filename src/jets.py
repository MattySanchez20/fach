import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
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
    def shoot(self):
        pass

    @abstractmethod
    def deduct_health(self):
        pass

    @abstractmethod
    def add_health(self):
        pass

    @abstractmethod
    def obtain_health(self):
        pass


class F16(JetFighter):

    def __init__(self):
        super().__init__(
            name="F16",
            health=100,
            cannon_ammo=120,
            fire_rate=40,
            wingspan=45,
            damage_per_round=5 / 100,
            cannon_spread_rads=math.radians(4),
        )
        self.cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

    def shoot(self, duration: float):
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        damage = n_rounds * self.damage_per_round

        print(f"Fired {n_rounds} rounds\nDealt {damage}% damage")

        return damage

    def deduct_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        print(f"Deducted {damage}% health")

        return self.health

    def add_health(self, health_points):
        self.health += health_points
        print(f"Added {health_points}% health")

        return self.health

    def obtain_health(self):
        return self.health


class F18(JetFighter):

    def __init__(self):
        super().__init__(
            name="F18",
            health=100,
            cannon_ammo=240,
            fire_rate=50,
            wingspan=50,
            damage_per_round=3 / 100,
            cannon_spread_rads=math.radians(6),
        )
        self.cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

    def shoot(self, duration: float):
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        damage = n_rounds * self.damage_per_round

        print(f"Fired {n_rounds} rounds\nDealt {damage}% damage")

        return damage

    def deduct_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        print(f"Deducted {damage}% health")

        return self.health

    def add_health(self, health_points):
        self.health += health_points
        print(f"Added {health_points}% health")

        return self.health

    def obtain_health(self):
        return self.health
