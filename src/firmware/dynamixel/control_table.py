# ADD control table for different Dynamixel models

# TEMPLATE
# CONTROL_TABLE_{MODEL} = {
#   'VAR': {'ADDR': val, 'LEN': val},
# }

CONTROL_TABLE_XC_330 = {
    'MODEL_NUMBER':           {'ADDR': 0,    'LEN': 2},    # Model Number:       Unique identifier for the servo model
    'MODEL_INFORMATION':      {'ADDR': 2,    'LEN': 4},    # Model Information:  Detailed information about the model
    'FIRMWARE_VERSION':       {'ADDR': 6,    'LEN': 1},    # Firmware Version:   Current firmware version of the servo
    'ID':                     {'ADDR': 7,    'LEN': 1},    # ID:                 Unique identifier for the servo
    'BAUD_RATE':              {'ADDR': 8,    'LEN': 1},    # Baud Rate:          Communication speed
    'RETURN_DELAY_TIME':      {'ADDR': 9,    'LEN': 1},    # Return Delay Time:  Delay before sending data back (in microseconds)
    'DRIVE_MODE':             {'ADDR': 10,   'LEN': 1},    # Drive Mode:         Operation mode of the servo
    'OPERATING_MODE':         {'ADDR': 11,   'LEN': 1},    # Operating Mode:     Mode in which the servo operates
    'SECONDARY_ID':           {'ADDR': 12,   'LEN': 1},    # Secondary (Shadow) ID: Used for shadow ID purposes
    'PROTOCOL_TYPE':          {'ADDR': 13,   'LEN': 1},    # Protocol Type:      Communication protocol version
    'HOMING_OFFSET':          {'ADDR': 20,   'LEN': 4},    # Homing Offset:      Offset for homing the servo (in pulses)
    'MOVING_THRESHOLD':       {'ADDR': 24,   'LEN': 4},    # Moving Threshold:   Speed threshold for movement detection (in rev/min)
    'TEMPERATURE_LIMIT':      {'ADDR': 31,   'LEN': 1},    # Temperature Limit:  Maximum allowable temperature (in °C)
    'MAX_VOLTAGE_LIMIT':      {'ADDR': 32,   'LEN': 2},    # Max Voltage Limit:  Maximum allowable voltage (in V)
    'MIN_VOLTAGE_LIMIT':      {'ADDR': 34,   'LEN': 2},    # Min Voltage Limit:  Minimum allowable voltage (in V)
    'PWM_LIMIT':              {'ADDR': 36,   'LEN': 2},    # PWM Limit:          Maximum PWM value (in percentage)
    'CURRENT_LIMIT':          {'ADDR': 38,   'LEN': 2},    # Current Limit:      Maximum current (in mA)
    'VELOCITY_LIMIT':         {'ADDR': 44,   'LEN': 4},    # Velocity Limit:     Maximum velocity (in rev/min)
    'MAX_POSITION_LIMIT':     {'ADDR': 48,   'LEN': 4},    # Max Position Limit: Maximum position limit (in pulses)
    'MIN_POSITION_LIMIT':     {'ADDR': 52,   'LEN': 4},    # Min Position Limit: Minimum position limit (in pulses)
    'STARTUP_CONFIGURATION':  {'ADDR': 60,   'LEN': 1},    # Startup Configuration: Initial setup parameters
    'PWM_SLOPE':              {'ADDR': 62,   'LEN': 1},    # PWM Slope:          PWM slope rate (in mV/msec)
    'SHUTDOWN':               {'ADDR': 63,   'LEN': 1},    # Shutdown:           Shutdown mode control
    'TORQUE_ENABLE':          {'ADDR': 64,   'LEN': 1},    # Torque Enable:      0 = Off, 1 = On
    'LED':                    {'ADDR': 65,   'LEN': 1},    # LED Control:        0 = Off, 1 = On
    'STATUS_RETURN_LEVEL':    {'ADDR': 68,   'LEN': 1},    # Status Return Level: 0 = No Return, 1 = Read-only, 2 = All
    'REGISTERED_INSTRUCTION': {'ADDR': 69,   'LEN': 1},    # Registered Instruction: 0 = No, 1 = Yes
    'HARDWARE_ERROR_STATUS':  {'ADDR': 70,   'LEN': 1},    # Hardware Error Status: Bit flags for error status
    'BUS_WATCHDOG':           {'ADDR': 98,   'LEN': 1},    # Bus Watchdog Timeout: Range 1 ~ 127 (in 20ms increments)
    'GOAL_PWM':               {'ADDR': 100,  'LEN': 2},    # Goal PWM:           Desired PWM Output: Range -PWM Limit ~ PWM Limit (in 0.113%)
    'GOAL_CURRENT':           {'ADDR': 102,  'LEN': 2},    # Goal Current:       Desired Current Output: Range -Current Limit ~ Current Limit (in 1.0mA)
    'GOAL_VELOCITY':          {'ADDR': 104,  'LEN': 4},    # Goal Velocity:      Desired Velocity: Range -Velocity Limit ~ Velocity Limit (in 0.229 rev/min)
    'PROFILE_ACCELERATION':   {'ADDR': 108,  'LEN': 4},    # Profile Acceleration: Acceleration Profile: Range 0 ~ 32767 (in 214.577 rev/min^2, 1ms intervals)
    'PROFILE_VELOCITY':       {'ADDR': 112,  'LEN': 4},    # Profile Velocity:   Velocity Profile: Range 0 ~ 32767 (in 0.229 rev/min)
    'GOAL_POSITION':          {'ADDR': 116,  'LEN': 4},    # Goal Position:      Desired Position: Range Min Position Limit ~ Max Position Limit (in 1 pulse)
    'REALTIME_TICK':          {'ADDR': 120,  'LEN': 2},    # Realtime Tick:      Timer Tick (Read-only): Range 0 ~ 32767 (in 1ms intervals)
    'MOVING':                 {'ADDR': 122,  'LEN': 1},    # Moving:             Moving Status: 0 = No, 1 = Yes (Read-only)
    'MOVING_STATUS':          {'ADDR': 123,  'LEN': 1},    # Moving Status:      Detailed Moving Status (Read-only)
    'PRESENT_PWM':            {'ADDR': 124,  'LEN': 2},    # Present PWM:        Current PWM Output (Read-only): Unit in 0.113%
    'PRESENT_CURRENT':        {'ADDR': 126,  'LEN': 2},    # Present Current:    Current Output (Read-only): Unit in 1.0mA
    'PRESENT_VELOCITY':       {'ADDR': 128,  'LEN': 4},    # Present Velocity:   Current Velocity (Read-only): Unit in 0.229 rev/min
    'PRESENT_POSITION':       {'ADDR': 132,  'LEN': 4},    # Present Position:   Current Position (Read-only): Unit in 1 pulse
    'VELOCITY_TRAJECTORY':    {'ADDR': 136,  'LEN': 4},    # Velocity Trajectory: Velocity Trajectory (Read-only): Unit in 0.229 rev/min
    'POSITION_TRAJECTORY':    {'ADDR': 140,  'LEN': 4},    # Position Trajectory: Position Trajectory (Read-only): Unit in 1 pulse
    'PRESENT_INPUT_VOLTAGE':  {'ADDR': 144,  'LEN': 2},    # Present Input Voltage: Current Input Voltage (Read-only): Unit in 0.1V
    'PRESENT_TEMPERATURE':    {'ADDR': 146,  'LEN': 1},    # Present Temperature: Current Temperature (Read-only): Unit in °C
    'BACKUP_READY':           {'ADDR': 147,  'LEN': 1},    # Backup Ready:       Backup Ready Status: 0 = No, 1 = Yes
}
