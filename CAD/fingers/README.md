# Finger Components for 24-DOF Robotic Hand

This directory contains the 3D model files for all finger components of the 24-DOF anthropomorphic robotic hand.

## Finger Structure

Each finger is composed of three main segments following human anatomy:
- **Proximal Phalanx** - Connected to the metacarpal via the MCP joint
- **Middle (Intermediate) Phalanx** - Between the proximal and distal segments
- **Distal Phalanx** - The fingertip segment

## Joint Types

The finger design incorporates two types of joints:
1. **Ball and Socket Joints** - Used for MCP joints, allowing flexion/extension and abduction/adduction
2. **Pin Joints** - Used for PIP and DIP joints, providing 1-DOF flexion/extension

## Directory Structure

- **distal/** - Distal phalanx designs for each finger
- **middle/** - Middle phalanx designs for each finger
- **proximal/** - Proximal phalanx designs for each finger
- **thumb/** - Specialized thumb components with different joint structure

## Design Features

- **Tendon Routing Channels** - Integrated channels for routing tendons through each segment
- **Tendon Termination Points** - Designed attachment points for securing tendons
- **Anatomical Joint Surfaces** - Joint surfaces follow human anatomical shapes
- **Tactile Sensor Mounts** - Provisions for mounting tactile sensors (optional)
- **Modular Design** - Components can be replaced individually without disassembling the entire hand

## Printing Recommendations

- **Resolution**: 0.10mm layer height recommended for joint surfaces
- **Material**: 
  - PLA+ or PETG for general use
  - TPU/Flexible filament for fingertips if tactile compliance is desired
- **Infill**: 40-50% for structural strength
- **Orientation**: Print with joint surfaces facing upward when possible to maximize surface quality

## Finger Dimensions

Finger lengths approximate average adult male hand proportions:
- **Index finger**: ~80mm (total length)
- **Middle finger**: ~85mm (total length)
- **Ring finger**: ~80mm (total length)
- **Pinky finger**: ~65mm (total length)
- **Thumb**: ~65mm (total length)

## Assembly Notes

- Each finger requires specific hardware from the BOM (bearings, screws, etc.)
- Refer to the assembly instructions in `/docs/assembly_instructions/` for detailed guidance
- Pre-tensioning of joints is critical for proper operation
