# Source Code for the 24-DOF Anthropomorphic Robotic Hand

This directory contains all the software components for controlling and operating the 24-DOF anthropomorphic robotic hand developed by the New Dexterity research group at the University of Auckland.

## Directory Structure

- **control/** - High-level control software for operating the robotic hand
  - `Hand.py` - Main hand control class
  - `finger_params.py` - Parameters for each finger (min/max angles, offsets)
  - `full_gui.py` - Graphical user interface for hand control

- **firmware/** - Low-level firmware for the hardware interface
  - **dynamixel/** - Code for interfacing with Dynamixel servo motors

- **kinematics/** - Kinematic models and calculations for the robotic hand

- **examples/** - Example scripts demonstrating various hand functionalities

- **simulation/** - Simulation environments for testing hand behaviors

## Dependencies

The software requires the following dependencies:
- Python 3.7+
- PySimpleGUI
- Pandas
- Dynamixel SDK
- NumPy

Install the required dependencies with:
```
pip install -r requirements.txt
```

## Getting Started

1. Connect the hand to your computer via USB
2. Ensure all motors are powered
3. Run the GUI:
```
python control/full_gui.py
```

## Control Interface

The GUI provides controls for:
- Individual joint angle control
- Finger position presets
- Hand gesture recording and playback
- Motor torque toggle
- Calibration interface

## Data Format

Hand gestures and positions are stored as CSV files in the `./data` directory with each joint position stored in the following format:
```
finger#joint
```

For example:
```
thumb#mcp, thumb#pip, thumb#dip, index#mcp, ...
```
