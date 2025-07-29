import math
from abc import ABC, abstractmethod


class JetFighter(ABC):
    """
    Abstract base class for all jet fighter aircraft.

    This class defines the common interface and attributes that all jet fighters
    must implement. It serves as a template for specific aircraft implementations,
    ensuring consistent behavior across different fighter types.

    Attributes:
        name (str): The designation/name of the fighter aircraft
        health (float): Current health percentage (0-100)
        cannon_ammo (int): Remaining cannon ammunition rounds
        fire_rate (float): Rate of fire in rounds per second
        wingspan (float): Wingspan in meters (used for cross-sectional area)
        damage_per_round (float): Damage inflicted per cannon round (as percentage)
        cannon_spread_rads (float): Cannon spread angle in radians
    """

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
        """
        Initialize a jet fighter with its combat characteristics.

        Args:
            name (str): Aircraft designation (e.g., "F16", "F18")
            health (float): Initial health percentage (typically 100)
            cannon_ammo (int): Initial ammunition count
            fire_rate (float): Rounds fired per second
            wingspan (float): Aircraft wingspan in meters
            damage_per_round (float): Damage per round as decimal (e.g., 0.05 = 5%)
            cannon_spread_rads (float): Cannon spread angle in radians
        """
        self.name = name
        self.health = health
        self.cannon_ammo = cannon_ammo
        self.fire_rate = fire_rate
        self.wingspan = wingspan
        self.damage_per_round = damage_per_round
        self.cannon_spread_rads = cannon_spread_rads

    @abstractmethod
    def shoot(self, duration: float):
        """
        Fire the aircraft's cannon for a specified duration.

        This method simulates firing the cannon by calculating ammunition
        consumption based on fire rate and duration, then updating the
        remaining ammunition count.

        Args:
            duration (float): Time spent firing in seconds

        Returns:
            int: Remaining ammunition after firing
        """
        pass

    @abstractmethod
    def deduct_health(self, damage):
        """
        Apply damage to the aircraft's health.

        Reduces the aircraft's health by the specified damage amount.
        Health cannot go below 0.

        Args:
            damage (float): Amount of damage to apply

        Returns:
            float: Remaining health after damage application
        """
        pass

    @abstractmethod
    def add_health(self):
        """
        Restore health to the aircraft.

        This method would be used for repair or healing mechanics
        in extended simulations.

        Returns:
            float: Updated health value
        """
        pass

    @abstractmethod
    def obtain_health(self):
        """
        Get the current health value of the aircraft.

        Returns:
            float: Current health percentage
        """
        pass

    @abstractmethod
    def calculate_cross_sectional_area(self):
        """
        Calculate the aircraft's cross-sectional area for targeting.

        This area is used in hit probability calculations - larger aircraft
        are easier to hit. Typically calculated from wingspan.

        Returns:
            float: Cross-sectional area in square meters
        """
        pass

    @abstractmethod
    def calculate_damage(self, duration):
        """
        Calculate total damage output for a given firing duration.

        Combines fire rate, damage per round, and firing duration to
        determine total damage potential.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            float: Total damage that would be inflicted
        """
        pass

    def __str__(self):
        """
        Return a formatted string representation of the fighter's specifications.

        Provides a human-readable summary of all the fighter's key characteristics
        including converted units (e.g., radians to degrees for cannon spread).

        Returns:
            str: Formatted string containing all fighter specifications
        """
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
    """
    F-16 Fighting Falcon fighter aircraft implementation.

    The F-16 is characterized by:
    - High ammunition capacity (3000 rounds)
    - High rate of fire (80 rounds/sec)
    - Moderate wingspan (45 meters)
    - Low damage per round (5%)
    - Tight cannon spread (3 degrees)

    This configuration makes the F-16 effective at sustained combat with
    high accuracy but requires more hits to inflict significant damage.
    """

    def __init__(self):
        """
        Initialize an F-16 Fighting Falcon with standard specifications.

        Sets up the F-16 with realistic combat characteristics including
        high ammunition capacity and tight cannon grouping for precision.
        """
        super().__init__(
            name="F16",
            health=100,  # Full health at start
            cannon_ammo=3000,  # High ammunition capacity
            fire_rate=80,  # High rate of fire (rounds/sec)
            wingspan=45,  # Moderate wingspan (meters)
            damage_per_round=5 / 100,  # Low damage per round (5%)
            cannon_spread_rads=math.radians(3),  # Tight spread (3 degrees)
        )

    def shoot(self, duration: float):
        """
        Fire the F-16's cannon for the specified duration.

        Calculates rounds fired based on the F-16's fire rate and reduces
        ammunition accordingly. Prevents ammunition from going negative.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            int: Remaining ammunition count after firing
        """
        # Calculate number of rounds fired based on duration and fire rate
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        # Ensure ammunition doesn't go below zero
        if self.cannon_ammo < 0:
            self.cannon_ammo = 0

        return self.cannon_ammo

    def deduct_health(self, damage):
        """
        Apply damage to the F-16's health.

        Reduces health by the damage amount, ensuring it doesn't go below zero.

        Args:
            damage (float): Damage amount to apply

        Returns:
            float: Remaining health after damage
        """
        self.health -= damage
        # Prevent health from going below zero
        if self.health < 0:
            self.health = 0

        return self.health

    def add_health(self, health_points):
        """
        Restore health to the F-16.

        Args:
            health_points (float): Amount of health to restore

        Returns:
            float: Updated health value
        """
        self.health += health_points

        return self.health

    def obtain_health(self):
        """
        Get the F-16's current health.

        Returns:
            float: Current health percentage
        """
        return self.health

    def calculate_cross_sectional_area(self):
        """
        Calculate the F-16's cross-sectional area for targeting calculations.

        Uses wingspan to approximate the aircraft's target profile.
        Formula: π * (wingspan/2)²

        Returns:
            float: Cross-sectional area in square meters
        """
        cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

        return cross_sectional_area

    def calculate_damage(self, duration):
        """
        Calculate total damage output for the F-16 over a firing duration.

        Combines the F-16's fire rate and damage per round to determine
        total damage potential for the given time period.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            float: Total damage that would be inflicted
        """
        return duration * self.fire_rate * self.damage_per_round


class F18(JetFighter):
    """
    F/A-18 Hornet fighter aircraft implementation.

    The F-18 is characterized by:
    - Very high ammunition capacity (4000 rounds)
    - Moderate rate of fire (50 rounds/sec)
    - Large wingspan (50 meters)
    - High damage per round (30%)
    - Wide cannon spread (6 degrees)

    This configuration makes the F-18 a heavy-hitting aircraft that trades
    accuracy for devastating damage output when hits connect.
    """

    def __init__(self):
        """
        Initialize an F/A-18 Hornet with standard specifications.

        Sets up the F-18 with characteristics favoring high damage output
        over precision, making it effective in close-range engagements.
        """
        super().__init__(
            name="F18",
            health=100,  # Full health at start
            cannon_ammo=4000,  # Very high ammunition capacity
            fire_rate=50,  # Moderate rate of fire (rounds/sec)
            wingspan=50,  # Large wingspan (meters)
            damage_per_round=30 / 100,  # High damage per round (30%)
            cannon_spread_rads=math.radians(6),  # Wide spread (6 degrees)
        )

    def shoot(self, duration: float):
        """
        Fire the F-18's cannon for the specified duration.

        Calculates rounds fired based on the F-18's fire rate and reduces
        ammunition accordingly. Prevents ammunition from going negative.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            int: Remaining ammunition count after firing
        """
        # Calculate number of rounds fired based on duration and fire rate
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        # Ensure ammunition doesn't go below zero
        if self.cannon_ammo < 0:
            self.cannon_ammo = 0

        return self.cannon_ammo

    def deduct_health(self, damage):
        """
        Apply damage to the F-18's health.

        Reduces health by the damage amount, ensuring it doesn't go below zero.

        Args:
            damage (float): Damage amount to apply

        Returns:
            float: Remaining health after damage
        """
        self.health -= damage
        # Prevent health from going below zero
        if self.health < 0:
            self.health = 0

        return self.health

    def add_health(self, health_points):
        """
        Restore health to the F-18.

        Args:
            health_points (float): Amount of health to restore

        Returns:
            float: Updated health value
        """
        self.health += health_points

        return self.health

    def obtain_health(self):
        """
        Get the F-18's current health.

        Returns:
            float: Current health percentage
        """
        return self.health

    def calculate_cross_sectional_area(self):
        """
        Calculate the F-18's cross-sectional area for targeting calculations.

        Uses wingspan to approximate the aircraft's target profile.
        Formula: π * (wingspan/2)²

        Returns:
            float: Cross-sectional area in square meters
        """
        cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

        return cross_sectional_area

    def calculate_damage(self, duration):
        """
        Calculate total damage output for the F-18 over a firing duration.

        Combines the F-18's fire rate and damage per round to determine
        total damage potential for the given time period.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            float: Total damage that would be inflicted
        """
        return duration * self.fire_rate * self.damage_per_round


class F22(JetFighter):
    """
    F-22 Raptor fighter aircraft implementation.

    The F-22 is characterized by:
    - Moderate ammunition capacity (2000 rounds)
    - Moderate rate of fire (60 rounds/sec)
    - Very large wingspan (60 meters)
    - Extremely high damage per round (80%)
    - Very tight cannon spread (2 degrees)

    This configuration makes the F-22 the most advanced fighter, combining
    extreme precision with devastating damage output, though with limited
    ammunition requiring careful engagement management.
    """

    def __init__(self):
        """
        Initialize an F-22 Raptor with standard specifications.

        Sets up the F-22 as the most advanced fighter with maximum precision
        and damage output, representing cutting-edge military technology.
        """
        super().__init__(
            name="F22",
            health=100,  # Full health at start
            cannon_ammo=2000,  # Moderate ammunition capacity
            fire_rate=60,  # Moderate rate of fire (rounds/sec)
            wingspan=60,  # Very large wingspan (meters)
            damage_per_round=80 / 100,  # Extremely high damage per round (80%)
            cannon_spread_rads=math.radians(2),  # Very tight spread (2 degrees)
        )

    def shoot(self, duration: float):
        """
        Fire the F-22's cannon for the specified duration.

        Calculates rounds fired based on the F-22's fire rate and reduces
        ammunition accordingly. Prevents ammunition from going negative.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            int: Remaining ammunition count after firing
        """
        # Calculate number of rounds fired based on duration and fire rate
        n_rounds = duration * self.fire_rate
        self.cannon_ammo -= n_rounds

        # Ensure ammunition doesn't go below zero
        if self.cannon_ammo < 0:
            self.cannon_ammo = 0

        return self.cannon_ammo

    def deduct_health(self, damage):
        """
        Apply damage to the F-22's health.

        Reduces health by the damage amount, ensuring it doesn't go below zero.

        Args:
            damage (float): Damage amount to apply

        Returns:
            float: Remaining health after damage
        """
        self.health -= damage
        # Prevent health from going below zero
        if self.health < 0:
            self.health = 0

        return self.health

    def add_health(self, health_points):
        """
        Restore health to the F-22.

        Args:
            health_points (float): Amount of health to restore

        Returns:
            float: Updated health value
        """
        self.health += health_points

        return self.health

    def obtain_health(self):
        """
        Get the F-22's current health.

        Returns:
            float: Current health percentage
        """
        return self.health

    def calculate_cross_sectional_area(self):
        """
        Calculate the F-22's cross-sectional area for targeting calculations.

        Uses wingspan to approximate the aircraft's target profile.
        Formula: π * (wingspan/2)²

        Returns:
            float: Cross-sectional area in square meters
        """
        cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141

        return cross_sectional_area

    def calculate_damage(self, duration):
        """
        Calculate total damage output for the F-22 over a firing duration.

        Combines the F-22's fire rate and damage per round to determine
        total damage potential for the given time period.

        Args:
            duration (float): Firing duration in seconds

        Returns:
            float: Total damage that would be inflicted
        """
        return duration * self.fire_rate * self.damage_per_round
