# CAD Files for 24-DOF Anthropomorphic Robotic Hand

This directory contains all the 3D CAD files for the 24-DOF anthropomorphic robotic hand.

## Directory Structure

- **fingers/** - All finger components
  - **distal/** - Distal phalanx designs for each finger
  - **middle/** - Middle (intermediate) phalanx designs
  - **proximal/** - Proximal phalanx designs
  - **thumb/** - Specialized thumb components
  
- **palm/** - Palm structure components
  - **carpal_bones/** - Simplified carpal bone structures
  - **metacarpals/** - Metacarpal designs for each finger
  
- **wrist/** - Wrist joint components and connection to forearm
  
- **actuation_unit/** - Components for the motor housing and actuation system
  
- **assembly/** - Complete assembly files
  - **step/** - STEP format assembly files for CAD software
  - **stl/** - STL format files for 3D printing

## Design Features

- **Anthropomorphic Design**: The hand closely mimics human hand anatomy with appropriate bone structures and joint placements.

- **Joint Types**:
  - Ball and socket joints for MCPs and CMCs (multi-DOF)
  - Pin joints for PIPs and DIPs (1-DOF)
  
- **Tendon Routing System**: Includes channels and pathways for proper tendon routing through each finger.

- **Modular Design**: Components can be assembled, disassembled, and replaced individually.

## Printing Recommendations

- **Resolution**: 0.1-0.15mm layer height recommended for joints and detailed parts
- **Material**: PLA+ or PETG recommended for most components
- **Infill**: 30-40% for most parts, 60%+ for high-stress components
- **Support**: Required for overhangs, particularly in joint areas

## File Formats

- **.STL** - 3D printable mesh files
- **.STEP** - CAD assembly files compatible with most CAD software
- **.SLDPRT/.SLDASM** - Original SolidWorks source files (where applicable)
