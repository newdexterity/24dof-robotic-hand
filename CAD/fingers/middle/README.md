# Middle Finger Components for 24-DOF Robotic Hand

This directory contains the 3D model files for the middle finger components of the 24-DOF anthropomorphic robotic hand.

## Component Overview

The middle finger is the longest and most central digit of the hand, consisting of:
- **Proximal Phalanx** (`middle_pp.stl`) - Connected to the metacarpal via the MCP joint
- **Intermediate Phalanx** (`middle_ip.stl`) - Middle segment connected via the PIP joint
- **Distal Phalanx** (`middle_dp.stl`) - Fingertip segment connected via the DIP joint

## Design Features

### Anatomical Proportions

The middle finger is designed with accurate biomimetic proportions:
- Total length: ~85mm (longest of all fingers)
- Segment proportions follow the golden ratio approximation:
  - Distal: 1 unit
  - Intermediate: 1.6 units
  - Proximal: 2.6 units

### Joint Mechanisms

- **MCP Joint**: Ball-and-socket design allowing 2-DOF movement
  - Flexion/Extension: 0° to 90°
  - Abduction/Adduction: ±15°
  
- **PIP Joint**: Pin joint with 1-DOF
  - Flexion/Extension: 0° to 110°
  
- **DIP Joint**: Pin joint with 1-DOF
  - Flexion/Extension: 0° to 90°

### Tendon Routing

The middle finger has specialized tendon pathways:
- Primary flexion tendon channel along the palmar aspect
- Extension tendon channel along the dorsal aspect
- Abduction/adduction tendon routing at the MCP joint
- Termination points at each phalanx for proper actuation

### Specialized Features

- Reinforced structure for increased durability (as middle finger experiences highest loads)
- Biomimetic fingertip pulp area for improved grasping
- Extended tendon termination points for better torque distribution
- Improved bearing pockets for smoother joint rotation

## Printing Recommendations

- **Layer Height**: 0.10mm for optimal joint surfaces
- **Orientation**:
  - Proximal: Print with MCP socket facing upward
  - Intermediate: Print with joint axes horizontal
  - Distal: Print with fingerpad down, with supports
- **Material**: PETG recommended for durability
- **Infill**: 40-50% with 3+ perimeters for strength

## Assembly Notes

1. Ensure all support material is removed from joint surfaces
2. Install 3mm bearings into the MCP joint socket
3. Use 2mm pins for the PIP and DIP joints
4. Route tendons through channels before securing joints
5. Attach to middle metacarpal with proper alignment
6. Verify smooth motion through full range before tendon tensioning
