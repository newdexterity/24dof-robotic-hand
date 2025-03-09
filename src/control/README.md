# Control Software for 24-DOF Robotic Hand

This directory contains the high-level control software for operating the 24-DOF anthropomorphic robotic hand.

## Files

- **Hand.py** - Main hand control class that provides methods for:
  - Motor initialization and configuration
  - Individual and grouped joint control
  - Finger motion control
  - Hand state management
  - Calibration operations

- **finger_params.py** - Contains the configuration parameters for each finger, including:
  - Min/max joint angles
  - Servo ID mapping
  - Calibration offsets
  - Motor parameters

- **full_gui.py** - Graphical user interface for controlling the hand with features including:
  - Real-time joint control sliders
  - Hand gesture recording and playback
  - Calibration interface
  - Motor torque control
  - Connection to external systems (e.g., MATLAB for visual feedback)

## Usage

### Hand Control

The `Hand` class is the main interface for programmatic control:

```python
from Hand import Hand

# Initialize hand
hand = Hand()

# Enable torque
hand.set_torque(True)

# Move specific finger joints
hand.update_finger_joint("index", {"mcp": 45, "pip": 30, "dip": 20})
hand.move_finger(["index"], t_exec=2000)  # 2000ms execution time

# Get current hand state
state = hand.get_hand_states()
```

### GUI Control

Run the graphical interface with:

```python
python full_gui.py
```

The interface provides:
- Sliders for individual joint control
- Time parameter adjustment for motion speed
- CSV-based recording and playback system
- Calibration tools for motor offset adjustment

## Data Storage

Hand gestures and positions are stored as CSV files in the `./data` directory. The files contain rows of waypoints, with each column representing a specific joint in the format `finger#joint`.

## Calibration

The calibration tab in the GUI allows for fine-tuning of motor offsets for each joint. Adjustments are saved automatically to the finger parameter configuration.
