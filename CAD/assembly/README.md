# Complete Assembly Files for 24-DOF Robotic Hand

This directory contains the complete assembly files for the 24-DOF anthropomorphic robotic hand.

## Directory Structure

- **step/** - STEP format assembly files compatible with most CAD software
  - `robot_hand_assembly.step` - Complete hand assembly in STEP format
  
- **stl/** - STL format assembly files for visualization and 3D printing
  - `robot_hand_assembly.stl` - Complete hand assembly in STL format

## Assembly Overview

The complete assembly integrates all components of the robotic hand:
- All five finger assemblies (thumb, index, middle, ring, pinky)
- Palm structure with metacarpals and carpal bones
- Wrist mechanism with 2-DOF joint
- Tendon routing pathways throughout the system

## Technical Specifications

### Complete Hand
- **Total Weight**: Approximately 1.45 kg (excluding actuation unit)
- **Overall Dimensions**: 200mm (length) × 100mm (width) × 30mm (depth)
- **Total Parts**: ~80 3D printed components
- **Fasteners**: ~120 screws, nuts, pins, and bearings

### Degrees of Freedom
- **Fingers**: 20 DOF (4 per finger)
- **Wrist**: 2 DOF (flexion/extension and abduction/adduction)
- **Additional**: 2 DOF (specialized abduction/adduction)
- **Total**: 24 DOF

## CAD Software Compatibility

The STEP files can be imported into:
- SolidWorks
- Fusion 360
- Onshape
- FreeCAD
- AutoCAD
- Inventor
- Most modern CAD packages

## Assembly References

For detailed assembly instructions, refer to:
- `/docs/assembly_instructions/` directory for step-by-step guides
- `/docs/images/assembly_steps/` for visual assembly references
- `/docs/BOM.md` for the complete bill of materials

## Modification Guidelines

When modifying the assembly:
1. Always work with the STEP files for parametric changes
2. Export to STL after modifications are complete
3. Maintain tendon routing channel alignment
4. Preserve joint mechanisms and ranges of motion
5. Test kinematic behavior after significant changes
