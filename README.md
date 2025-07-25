# FACH - Fighter Aircraft Combat Simulator

A Python-based air combat simulation that models dogfights between different fighter aircraft types. The simulator features realistic combat mechanics including distance-based hit probability calculations, weapon systems modeling, and health management.

## Features

- **Realistic Combat Physics**: Distance-based hit probability calculations using cannon spread and aircraft cross-sectional areas
- **Multiple Aircraft Types**: Currently supports F-16 Fighting Falcon and F/A-18 Hornet with unique specifications
- **Dynamic Combat Scenarios**: Variable engagement distances, durations, and random elements
- **Extensible Design**: Abstract base class architecture allows easy addition of new aircraft types

## Aircraft Specifications

### F-16 Fighting Falcon
- **Health**: 100%
- **Cannon Ammunition**: 120 rounds
- **Fire Rate**: 40 rounds/second
- **Wingspan**: 45 feet
- **Damage per Round**: 0.05%
- **Cannon Spread**: 4 degrees

### F/A-18 Hornet
- **Health**: 100%
- **Cannon Ammunition**: 240 rounds
- **Fire Rate**: 50 rounds/second
- **Wingspan**: 50 feet
- **Damage per Round**: 0.03%
- **Cannon Spread**: 6 degrees

## Installation

This project uses Poetry for dependency management. Ensure you have Python 3.11+ installed.

```bash
# Clone the repository
git clone <repository-url>
cd fach

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Usage

### Running a Combat Simulation

```bash
python src/main.py
```

The main simulation runs a series of engagements between an F-16 and F/A-18, starting at 100 units distance and closing by 25 units each round until one aircraft is destroyed or they reach point-blank range.

### Example Output

```
FIGHTING.................

Dogfight details:
distance=100
duration=3.2

F18 has hit the F16
Deducted 4.8% health
F16 Health: 95.2
F18 Health: 100.0
```

## Code Structure

```
src/
├── main.py          # Main simulation runner
├── jets.py          # Aircraft class definitions
├── utils.py         # Combat calculation utilities
└── __init__.py      # Package initialization
```

### Core Components

#### `jets.py`
- **`JetFighter`**: Abstract base class defining the aircraft interface
- **`F16`**: F-16 Fighting Falcon implementation
- **`F18`**: F/A-18 Hornet implementation

#### `utils.py`
- **`p_by_distance()`**: Calculates hit probability based on distance, cannon spread, and target cross-section
- **`dogfight()`**: Utility function for running individual combat engagements

#### `main.py`
- Main simulation loop that runs a series of engagements at decreasing distances

## Combat Mechanics

### Hit Probability Calculation

The simulation uses realistic physics to calculate hit probability:

1. **Cannon Spread Area**: `π × (tan(spread_angle) × distance)²`
2. **Target Cross-Section**: `π × (wingspan/2)²`
3. **Hit Probability**: `min(1.0, target_area / spread_area)`

### Damage System

- Damage is calculated as: `fire_rate × damage_per_round × engagement_duration`
- Health is reduced by the calculated damage amount
- Aircraft are destroyed when health reaches 0%

### Random Elements

- Engagement duration (0-10 seconds)
- Hit success based on probability vs random roll (0-1)
- Distance variation in utility functions

## Development

### Dependencies

- **pandas**: Data manipulation and analysis
- **matplotlib**: Plotting and visualization (for future features)
- **black**: Code formatting
- **isort**: Import sorting

### Code Style

This project uses Black for code formatting and isort for import organization:

```bash
# Format code
black src/

# Sort imports  
isort src/
```

### Adding New Aircraft

To add a new aircraft type:

1. Create a new class inheriting from `JetFighter`
2. Implement all abstract methods (`shoot`, `deduct_health`, `add_health`, `obtain_health`)
3. Define aircraft specifications in `__init__`
4. Calculate `cross_sectional_area` based on wingspan

Example:
```python
class F22(JetFighter):
    def __init__(self):
        super().__init__(
            name="F22",
            health=120,
            cannon_ammo=480,
            fire_rate=100,
            wingspan=44.5,
            damage_per_round=0.06,
            cannon_spread_rads=math.radians(3)
        )
        self.cross_sectional_area = (self.wingspan / 2) ** 2 * 3.141
```

## Future Enhancements

- [ ] Missile systems modeling
- [ ] Multiple engagement scenarios
- [ ] Statistical analysis and visualization
- [ ] GUI interface
- [ ] Network multiplayer support
- [ ] More aircraft types (bombers, interceptors)
- [ ] Environmental factors (weather, altitude)

## License

This project is open source. Please refer to the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.