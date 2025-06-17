# Thumb Components for 24-DOF Robotic Hand

This directory contains the specialized 3D model files for the thumb components of the 24-DOF anthropomorphic robotic hand.

## Thumb Anatomy

The thumb design differs significantly from the other fingers to accurately replicate human anatomy:

- **Carpometacarpal (CMC) Joint** - A saddle joint allowing opposition movement
- **Metacarpophalangeal (MCP) Joint** - Simplified ball and socket joint
- **Interphalangeal (IP) Joint** - Single pin joint (equivalent to PIP in other fingers)

## Degrees of Freedom

The thumb incorporates 4 degrees of freedom:
1. CMC Flexion/Extension
2. CMC Abduction/Adduction (for opposition movement)
3. MCP Flexion/Extension
4. IP Flexion/Extension

## Component Files

- **thumb_meta.stl** - Thumb metacarpal component
- **thumb_pp.stl** - Proximal phalanx
- **thumb_ip.stl** - Intermediate phalanx
- **thumb_dp.stl** - Distal phalanx

## Design Features

### Opposition Movement
The design allows for true opposition movement, critical for precision and power grasps. The CMC joint has been carefully designed to enable the thumb to reach across the palm to contact all fingertips.

### Tendon Routing
The thumb includes specialized tendon routing channels to accommodate its unique motion requirements:
- Primary flexion tendon
- Extension tendon
- Abduction/adduction tendons

### Range of Motion
The thumb joints are designed to achieve the following approximate ranges:
- CMC Flexion/Extension: 0-60°
- CMC Abduction/Adduction: 0-70°
- MCP Flexion: 0-55°
- IP Flexion: 0-85°

## Assembly Notes

1. The CMC joint connects to the trapezium in the carpal bone assembly
2. Special attention should be paid to tendon routing at the CMC joint
3. Ensure smooth motion through the full range of opposition movement
4. Recommended hardware includes 3mm bearings for the MCP joint
5. Use 2mm pins for the IP joint

## Printing Recommendations

- **Layer Height**: 0.10mm for joint surfaces
- **Orientation**: Print the metacarpal component on its side for best joint surface quality
- **Support**: Required for the metacarpal component
- **Material**: PETG recommended for improved durability at joint surfaces
