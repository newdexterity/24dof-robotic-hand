# Firmware for 24-DOF Robotic Hand

This directory contains the firmware and hardware interface code for the 24-DOF anthropomorphic robotic hand.

## Overview

The firmware provides a low-level interface to the hardware components of the hand, primarily the Dynamixel servo motors that drive the tendon-based actuation system. It handles communication protocols, motor configuration, and direct control commands.

## Subdirectories

- **dynamixel/** - Contains code specific to interfacing with Dynamixel servo motors

## Hardware Components

The hand uses 24 Dynamixel XC-330-T228-T servo motors:
- 20 motors for finger joints (4 per finger)
- 2 motors for wrist movement
- 2 motors for additional abduction/adduction movements

## Communication Protocol

- Communication with the motors is achieved via the Dynamixel Protocol 2.0
- Default baud rate: 115,200 bps
- Each motor has a unique ID from 1-24
- Communication over USB via U2D2 converter

## Motor Configuration

Default motor configuration includes:
- Operating mode: Extended Position control

## Dependencies

- Dynamixel SDK (Python/C++ versions)

## Implementation Notes

- Direct motor commands should use appropriate velocity profiles for smooth movement
- Temperature monitoring is implemented to prevent motor damage
- Error handling includes automatic reconnection attempts when communication fails
- The core driver implementation is wrapped by the higher-level control classes in the `control` directory
