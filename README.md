# FACH - Fighter Aircraft Combat Simulator

A Python-based air combat simulation that models dogfights between different fighter aircraft types. The simulator features realistic combat mechanics including distance-based hit probability calculations, weapon systems modeling, and health management.

**Now with comprehensive documentation and enhanced code clarity!**

## Features

- **Realistic Combat Physics**: Distance-based hit probability calculations using cannon spread and aircraft cross-sectional areas
- **Multiple Aircraft Types**: Currently supports F-16 Fighting Falcon and F/A-18 Hornet with unique specifications
- **Dynamic Combat Scenarios**: Variable engagement distances, durations, and random elements
- **Extensible Design**: Abstract base class architecture allows easy addition of new aircraft types
- **Combat Logging**: Detailed engagement feedback and health tracking throughout battles

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
- **`JetFighter`**: Abstract base class defining the aircraft interface with comprehensive docstrings
  - Enforces implementation of combat methods (`shoot`, `deduct_health`, `add_health`, `obtain_health`)
  - Defines common aircraft attributes with type hints
  - Includes detailed parameter documentation
- **`F16`**: F-16 Fighting Falcon implementation with realistic specifications
  - Moderate damage output with tight cannon spread for accuracy
  - 120 rounds ammunition capacity
  - Fully documented methods with mathematical explanations
- **`F18`**: F/A-18 Hornet implementation with naval fighter characteristics  
  - Higher ammunition capacity and fire rate
  - Wider cannon spread but lower damage per round
  - Cross-sectional area calculations for hit probability

#### `utils.py`
- **`p_by_distance()`**: Calculates hit probability based on distance, cannon spread, and target cross-section
  - Uses realistic ballistics: `π × (tan(spread_angle) × distance)²`
  - Includes comprehensive mathematical documentation
  - Returns probability tuple for both aircraft
- **`dogfight()`**: Utility function for running individual combat engagements
  - Randomized engagement parameters (distance, duration, pilot skill)
  - Real-time combat simulation with sleep delays
  - Detailed combat feedback and health tracking

#### `main.py`
- Main simulation loop that runs a series of engagements at decreasing distances
- **Enhanced Documentation**: Step-by-step combat process explanation
- **Realistic Combat Flow**: Distance-based engagement progression (100 → 75 → 50 → 25 units)
- **Comprehensive Logging**: Detailed engagement statistics and health monitoring

#### `__init__.py`
- Package initialization with usage examples
- Import guidance for new developers
- Overview of simulator capabilities

## Combat Mechanics

### Hit Probability Calculation

The simulation uses realistic physics to calculate hit probability with detailed mathematical modeling:

1. **Cannon Spread Area**: `π × (tan(spread_angle) × distance)²`
   - Calculates the circular area covered by cannon fire at target distance
   - Uses trigonometry to model bullet dispersion cone
2. **Target Cross-Section**: `π × (wingspan/2)²`
   - Assumes circular aircraft profile based on wingspan
   - Represents the effective target area for incoming fire
3. **Hit Probability**: `min(1.0, target_area / spread_area)`
   - If spread area ≤ target area: guaranteed hit (probability = 1.0)
   - Otherwise: probability = ratio of target area to spread area
   - Ensures realistic hit chances that decrease with distance

### Damage System

The damage calculation system uses realistic military specifications:

- **Base Formula**: `fire_rate × damage_per_round × engagement_duration`
- **Fire Rate**: Rounds per second (F-16: 40 rps, F/A-18: 50 rps)
- **Damage per Round**: Percentage health damage (F-16: 0.05%, F/A-18: 0.03%)
- **Health Management**: 
  - Health reduced by calculated damage amount
  - Minimum health clamped to 0% (aircraft destruction)
  - Real-time health tracking with console feedback

### Engagement Mechanics

- **Distance Progression**: Starts at 100 units, decreases by 25 per round
- **Random Elements**: 
  - Engagement duration (0-10 seconds) simulates maneuvering time
  - Pilot skill rolls (0-1) determine hit success against probability
  - Variable combat scenarios for realistic unpredictability
- **Combat Flow**: Each engagement includes setup, calculation, execution, and result phases

## Development

### Code Quality

This project maintains high code quality standards:

- **Comprehensive Documentation**: Every class, method, and function includes detailed docstrings
- **Type Hints**: Modern Python typing for better IDE support and code clarity
- **Inline Comments**: Step-by-step explanations of complex calculations and logic
- **Mathematical Documentation**: Formulas and ballistics explanations included
- **TODO Comments**: Clear roadmap for future improvements and known limitations

### Dependencies

- **pandas**: Data manipulation and analysis (ready for statistical features)
- **matplotlib**: Plotting and visualization (prepared for future graphing capabilities)
- **black**: Code formatting for consistent style
- **isort**: Import sorting for clean organization

### Code Style

This project uses Black for code formatting and isort for import organization:

```bash
# Format code
black src/

# Sort imports  
isort src/
```

### Documentation Standards

The codebase follows these documentation practices:

- **Module Docstrings**: Overview of each file's purpose and contents
- **Class Docstrings**: Detailed specifications and characteristics  
- **Method Docstrings**: Parameters, return values, side effects, and usage examples
- **Inline Comments**: Mathematical formulas, logic explanations, and implementation notes
- **Type Annotations**: Full type coverage for better code maintainability

### Adding New Aircraft

To add a new aircraft type, follow the well-documented pattern:

1. Create a new class inheriting from `JetFighter`
2. Implement all abstract methods (`shoot`, `deduct_health`, `add_health`, `obtain_health`)
3. Define aircraft specifications in `__init__` with proper documentation
4. Calculate `cross_sectional_area` based on wingspan
5. Add comprehensive docstrings explaining aircraft characteristics

Example with full documentation:
```python
class F22(JetFighter):
    """
    F-22 Raptor implementation.
    
    The F-22 is a fifth-generation stealth fighter with superior
    performance characteristics and advanced avionics.
    
    Specifications:
        - Health: 120% (enhanced survivability)
        - Cannon Ammo: 480 rounds
        - Fire Rate: 100 rounds/second  
        - Wingspan: 44.5 feet
        - Damage per Round: 0.06%
        - Cannon Spread: 3 degrees (superior accuracy)
    """
    def __init__(self):
        """Initialize F-22 with stealth fighter specifications."""
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
    
    # Implement all abstract methods with proper documentation...
```

## Future Enhancements

### Immediate Improvements (Based on TODO Comments)
- [ ] Add victory condition checks to main simulation loop
- [ ] Implement ammunition bounds checking in shooting mechanics
- [ ] Replace hardcoded aircraft names in `dogfight()` function with dynamic names
- [ ] Enhance damage calculations to use proper `damage_per_round` values

### Advanced Features
- [ ] Missile systems modeling with different engagement ranges
- [ ] Multiple engagement scenarios (beyond distance-based progression)
- [ ] Statistical analysis and visualization using matplotlib integration
- [ ] GUI interface for interactive combat simulation
- [ ] Network multiplayer support for human vs human dogfights
- [ ] More aircraft types (bombers, interceptors, stealth fighters)
- [ ] Environmental factors (weather, altitude, terrain effects)

### Technical Enhancements  
- [ ] Battle replay system with detailed logs
- [ ] Aircraft customization and loadout options
- [ ] Advanced AI pilot behaviors and strategies
- [ ] Performance metrics and combat effectiveness analysis
- [ ] Save/load functionality for simulation scenarios

## License

This project is open source. Please refer to the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.