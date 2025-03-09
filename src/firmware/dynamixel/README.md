# Dynamixel Motor Control for 24-DOF Robotic Hand

This directory contains code specific to controlling the Dynamixel servo motors used in the 24-DOF anthropomorphic robotic hand.

## Implementation

The code in this directory provides a wrapper around the Dynamixel SDK to facilitate:

- Motor initialization and device detection
- Command transmission and error handling
- Reading motor states (position, temperature, load)
- Motor configuration (PID values, operating modes, etc.)

## Motor Specification

The hand uses Dynamixel XC-330-T228-T servo motors

## Motor ID Assignment

Motors are assigned IDs based on the following scheme:

<!-- 1-4: Thumb (MCP, MCP_ABD, PIP, DIP)  
5-8: Index finger (MCP, MCP_ABD, PIP, DIP)  
9-12: Middle finger (MCP, MCP_ABD, PIP, DIP)  
13-16: Ring finger (MCP, MCP_ABD, PIP, DIP)  
17-20: Pinky finger (MCP, MCP_ABD, PIP, DIP)  
21-22: Wrist (horizontal, vertical)  
23-24: Abduction (thumb, pinky) -->

## Usage

The modules in this directory are typically not called directly but are used by the higher-level `Hand` class defined in the `control` directory.

## Error Handling

The implementation includes robust error handling to manage:

- Communication timeouts
- Overheating protection
- Torque limiting for safety
- Connection loss recovery
