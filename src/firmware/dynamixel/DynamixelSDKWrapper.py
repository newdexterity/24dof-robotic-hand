
"""
This module provides a wrapper for the Dynamixel SDK to simplify communication with Dynamixel servos.
It supports multiple servo models by utilizing their control tables.
"""

from dynamixel_sdk import (
    PacketHandler,
    PortHandler,
    Protocol2PacketHandler,
    GroupBulkWrite,
    GroupBulkRead,
    GroupSyncWrite,
    GroupSyncRead,
    COMM_SUCCESS,
    DXL_LOWORD,
    DXL_HIWORD,
    DXL_LOBYTE,
    DXL_HIBYTE,
    group_bulk_read,
    # reboot,
)
import control_table
import logging
import time
from typing import Dict, List, Union, Optional
from dataclasses import dataclass, field

@dataclass
class Servo:
    """
    Represents an individual Dynamixel servo with its specific parameters and control table.

    Attributes:
        id (int): The unique identifier for the servo.
        model (str): The model name of the servo.
        control_table (dict): The control table specific to the servo model.
        position_limits (dict): The minimum and maximum position limits of the servo.
        voltage_limits (dict): The minimum and maximum voltage limits of the servo.
        velocity_limit (int): The maximum velocity limit of the servo.
        operating_mode (str): The operating mode of the servo.
        drive_mode (str): The drive mode of the servo.
        secondary_id (int): The secondary (shadow) ID of the servo.
        torque_status (Optional[bool]): The current torque status of the servo.
    """
    id_: int
    model: str
    control_table: dict
    firmware_ver: int = 0
    position_limits: dict = field(default_factory=lambda: {'min': -1048575, 'max': 1048575})
    voltage_limits: dict = field(default_factory=lambda: {'min': 5.5, 'max': 14.0})
    velocity_limit: int = 320
    operating_mode: str = 'extended_pos'
    drive_mode: str = 'time'
    secondary_id: int = 255
    torque_status: bool = False

    def __repr__(self):
        repr = f"Servo ID: {self.id_}\n"
        repr += f"Model: {self.model}\n"
        repr += f"Control Table: {self.control_table}\n"
        repr += f"Firmware Version: {self.firmware_ver}\n"
        repr += f"Position Limits: {self.position_limits}\n"
        repr += f"Voltage Limits: {self.voltage_limits}\n"
        repr += f"Velocity Limit: {self.velocity_limit}\n"
        repr += f"Operating Mode: {self.operating_mode}\n"
        repr += f"Drive Mode: {self.drive_mode}\n"
        repr += f"Secondary ID: {self.secondary_id}\n"
        repr += f"Torque Status: {self.torque_status}\n"
        return repr


class DynamixelSDKWrapper:
    """
    A wrapper class for the Dynamixel SDK to manage communication with multiple servos.

    Attributes:
        CONTROL_TABLES (dict): A dictionary containing control tables for supported servo models.
        SUPPRESS_ERROR_MSG (bool): Flag to suppress error messages from the SDK.
        INVALID_INT_VAL (int): A constant representing an invalid integer value.
    """
   
    CONTROL_TABLES = {
        'XC330': control_table.CONTROL_TABLE_XC_330,
        # Add more models as needed
    } 

    SUPPRESS_ERROR_MSG = True # by default don't show error from SDK
    INVALID_INT_VAL = -1

    def __init__(self, port: str, protocol: float = 2.0, baudrate: int = 115200):
        """
        Initializes the DynamixelSDKWrapper.

        Args:
            port (str): The serial port to which the servos are connected.
            protocol (float, optional): The communication protocol version. Defaults to 2.0.
            baudrate (int, optional): The baud rate for communication. Defaults to 57600.
        """
        self.port: str = port
        self.protocol: float = protocol
        self.baudrate: int = baudrate
        self.port_handler: PortHandler = PortHandler(port)
        self.packet_handler: PacketHandler = PacketHandler(protocol)
        self.protocol_handler: Protocol2PacketHandler = Protocol2PacketHandler()
        self.groupBulkWrite: GroupBulkWrite = GroupBulkWrite(self.port_handler, self.packet_handler)
        self.groupBulkRead: GroupBulkRead = GroupBulkRead(self.port_handler, self.packet_handler)
        self._groupSyncWrite: GroupSyncWrite = GroupSyncWrite(self.port_handler, self.packet_handler, 0, 0)
        self._groupSyncRead: GroupSyncRead = GroupSyncRead(self.port_handler, self.packet_handler, 0, 0)
        self.servos = {}
        self.protocol_version = 2

        # Instantiate logger
        # logging.basicConfig(level=logging.INFO)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] : %(message)s",
            datefmt="[%X]")

        self.logger = logging.getLogger(__name__)
        
        # Open and configure serial port
        self.open_port()
        self.set_baudrate()


    def __del__(self):
        """Closes the port when the instance is destroyed."""
        self.close_port()

    def add_servo(self, servos: dict) -> None:
        """
        Adds and configures servos based on the provided dictionary.

        Args:
            servos (dict): A dictionary containing servo configurations.

        Example:
            servos = {
                'servo 1': {'id': 3, 'model': 'XC330', 'op_mode': 'position'},
                'servo 2': {'id': 10, 'model': 'XM540', 'op_mode': 'velocity'}
            }
        """

        # Unsuppress error messages
        self.suppress_error_msg(suppress=False)
         
        # Configure each servo
        for key in servos.keys():
            success = True
            id_, model = servos[key]['id'], servos[key]['model']

            print(f'------------------------------------------------')
            self.logger.info(f'ID: {id_}')

            # Check if ID already exists
            if self._is_servo_registered(id_):
                self.logger.error(f' - (ID: {id_}) Already exists')
                success &= False
                continue

            # Check if model is supported
            if model.upper() in self.CONTROL_TABLES and success:
                self.logger.info(f'- Model: {model.upper()}')
            else:
                self.logger.error(f" - Unsupported model ({model.upper()})")
                # self.logger.error('-- Supported models are (', end=' ')
                # [print(f'{model}', end=' ') for model in self.CONTROL_TABLES.keys()]
                # print(')')
                success &= False       

            # --------------- Assign control table ---------------
            
            # Create servo
            if success:
                control_table = self.CONTROL_TABLES[model.upper()] 
                self.servos[id_] = Servo(id_, model, control_table) 
                # print(self.servos.keys()) 
            # If no reponse, ignore ID
            fw = self.read_FW_version(id_)
            if fw != self.INVALID_INT_VAL and success:
                self.logger.info(f'- FW Version: {fw}')
                self.firmware_ver = fw
            else: 
                self.logger.error(f"- Device does not exist")
                success &= False
            
            # --------------- Restore previous configuration ---------------
            if self.startup_config(id_, restore_ram=True, torque_enable=False)and success:
                self.logger.info(f'- Restored previous configuation')
            else: 
                self.logger.error(f"- Could not restore configration")
                success &= False
            
            # --------------- Set operation mode ---------------
            op_mode = servos[key]['op_mode'] if 'op_mode' in servos[key].keys() else 'position'

            if self.set_operating_mode(id_, op_mode) and success:
                self.logger.info(f"- Operating Mode: {op_mode}")
            else:
                self.logger.error(f"- Set operating mode failed: {op_mode}")
                success &= False

            # --------------- Set reverse mode if needed ---------------
            if 'reverse_mode' in servos[key].keys(): 
                if self.set_reverse_mode(id_, reverse=servos[key]['reverse_mode']) and success:
                    self.logger.info(f"- Reverse Mode: {servos[key]['reverse_mode']}")
                else:
                    self.logger.error(f"- Set reverse mode failed: {servos[key]['reverse_mode']}")
                    success &= False

            
            # --------------- Set position limits ---------------
            # if servos[key]['op_mode'] is not 'extended_pos':
            if servos[key]['op_mode'] != 'extended_pos':
                min_pos, max_pos = servos[key]['pos_limit'][0], servos[key]['pos_limit'][1]
                if self.set_pos_limits(id_, min_pos, max_pos) and success:
                    self.logger.info(f"- Limits: {min_pos} <-> {max_pos}")
                else:
                    self.logger.error(f"- Set Position failed: {min_pos} <-> {max_pos}")
                    success &= False

                 
            # --------------- Set drive mode to time-based ---------------
            if self.enable_time_based_profile(id_, time_profile=True) and success:
                self.logger.info(f"- Driving Mode: Time-based")
            else:
                self.logger.error(f"- Set driving mode failed: Time-based")
                success &= False

            
            # --------------- Set secondary ID ---------------
            if self.set_secondary_id(id_, secondary_id=252) and success:
                self.logger.info(f"- Secondary ID: {252}")
            else:
                self.logger.error(f"- Set secondary ID failed: {252}")
                success &= False


            # # --------------- Disable torque ---------------
            # if self.set_torque(id, enable=0) and success:
            #     print(f"- Torque: Off")
            # else:
            #     print(f"- [ERROR] Set Torque failed: OFF")
            #     success &= False

            # --------------- Check Temperature ---------------
            temp = self.read_temperature(id_)
            if temp is not None:
                self.logger.info(f"- Temperature: {temp}")
            else:
                self.logger.error(f"- Read temperature failed")
                success &= False

            # --------------- Final Check ---------------

            if success: 
                self.logger.info(f'- [STATUS] SUCCESSFULLY CONFIGURED')
            elif not success and id_ in self.servos.keys(): 
                del self.servos[id_]
                self.logger.error(f'- CONFIGURATION FAILED')
            else: 
                self.logger.error(f'- CONFIGURATION FAILED')

        print(f'------------------------------------------------')

    def servo_set_pos_limits(self, id_: int, min_pos: int=0, max_pos: int=4095) -> bool:
        """
        Sets the position limits of the servo.

        Args:
            id_ (int): The servo ID.
            min_pos (int, optional): The minimum position limit. Defaults to 0.
            max_pos (int, optional): The maximum position limit. Defaults to 4095.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._is_servo_registered(id_):
            return False

        servo = self._get_servo(id_)
        dxl_comm_result_1, dxl_error_1 = self._writeTxRx(id_, servo.control_table['MAX_POSITION_LIMIT'], max_pos)
        dxl_comm_result_2, dxl_error_2 = self._writeTxRx(id_, servo.control_table['MIN_POSITION_LIMIT'], min_pos)
        
        # Check communication results
        if self._check_communication(id_, 'MAX_POSITION_LIMIT', dxl_comm_result_1, dxl_error_1, max_pos) and \
            self._check_communication(id_, 'MIN_POSITION_LIMIT', dxl_comm_result_2, dxl_error_2, min_pos):

            servo.position_limits = {'min': min_pos, 'max': max_pos}   # Update servo positions
            return True
        else: 
            return False

    def read_current_pos(self, id_) -> int:
        """
        Reads the current position of the servo.

        Args:
            id_ (int): The servo ID.

        Returns:
            int: The current position, or INVALID_INT_VAL if an error occurs.
        """
        if not self._is_servo_registered(id_): # Check if servo(id) exists
            return self.INVALID_INT_VAL 
        servo = self._get_servo(id_)

        dxl_present_position, dxl_comm_result, dxl_error = self._readTxRx(id_, servo.control_table['PRESENT_POSITION'])

        # Check communication result
        if self._check_communication(id_, 'PRESENT_POSITION', dxl_comm_result, dxl_error, val=dxl_present_position):
            # print(f"POSITION (ID: {id}): {dxl_present_position}")
            return dxl_present_position
        return self.INVALID_INT_VAL
    
    def read_FW_version(self, id_):
        """
        Reads the firmware version of the servo.

        Args:
            id_ (int): The servo ID.

        Returns:
            int: The firmware version, or INVALID_INT_VAL if an error occurs.
        """
        if not self._is_servo_registered(id_): # Check if servo(id) exists
            return self.INVALID_INT_VAL 
        servo = self._get_servo(id_)

        fw_version, dxl_comm_result, dxl_error = self._readTxRx(id_, servo.control_table['FIRMWARE_VERSION'])

        # Check communication result
        if self._check_communication(id_, 'FIRMWARE_VERSION', dxl_comm_result, dxl_error, val=fw_version):
            return fw_version
        return self.INVALID_INT_VAL 

    def read_voltage(self, id_):
        """
        Reads the current input voltage of the servo.

        Args:
            id_ (int): The servo ID.

        Returns:
            int: The voltage in 0.1V units, or INVALID_INT_VAL if an error occurs.
        """
        if not self._is_servo_registered(id_): # Check if servo(id) exists
            return self.INVALID_INT_VAL 
        servo = self._get_servo(id_)

        voltage, dxl_comm_result, dxl_error = self._readTxRx(id_, servo.control_table['PRESENT_INPUT_VOLTAGE'])
        if self._check_communication(id_, 'PRESENT_INPUT_VOLTAGE', dxl_comm_result, dxl_error, val=f"{voltage} V"):
            # print(f"INPUT VOLTAGE (ID: {id}): {voltage * 0.1} V")
            return voltage
        return self.INVALID_INT_VAL 

    def read_pos_limits(self, id_) -> list[int]:
        """
        Reads the position limits of the servo.

        Args:
            id_ (int): The servo ID.

        Returns:
            List[int]: [max_position_limit, min_position_limit], or [INVALID_INT_VAL, INVALID_INT_VAL] if an error occurs.
        """
        if not self._is_servo_registered(id_): # Check if servo(id) exists
            return [self.INVALID_INT_VAL, self.INVALID_INT_VAL]
        
        servo = self._get_servo(id_)

        max_pos, dxl_comm_result_1, dxl_error_1 = self._readTxRx(id_, servo.control_table['MAX_POSITION_LIMIT'])
        min_pos, dxl_comm_result_2, dxl_error_2 = self._readTxRx(id_, servo.control_table['MIN_POSITION_LIMIT'])

        if self._check_communication(id_, 'MAX_POSITION_LIMIT', dxl_comm_result_1, dxl_error_1, val=max_pos) and \
            self._check_communication(id_, 'MIN_POSITION_LIMIT', dxl_comm_result_2, dxl_error_2, val=min_pos):
            # print(f"MAX POS (ID: {id}): {max_pos}")
            # print(f"MIN POS (ID: {id}): {min_pos}")
            return [max_pos, min_pos] 
        
        return [self.INVALID_INT_VAL, self.INVALID_INT_VAL]

    def set_pos_limits(self, id_: int, min_pos: int = 0, max_pos: int = 4095) -> bool:
        """
        Sets the position limits of the servo.

        Args:
            id_ (int): The servo ID.
            min_pos (int, optional): The minimum position limit. Defaults to 0.
            max_pos (int, optional): The maximum position limit. Defaults to 4095.

        Returns:
            bool: True if successful, False otherwise.
        """
        if min_pos is None or max_pos is None:
            return False
        if not self._is_servo_registered(id_):
            return False

        if min_pos < 0:
            min_pos = 0

        if max_pos > 4095:
            max_pos = 4095

        servo = self._get_servo(id_)

        # Send limits
        dxl_comm_result_1, dxl_error_1 = self._writeTxRx(id_, servo.control_table['MAX_POSITION_LIMIT'], max_pos)
        dxl_comm_result_2, dxl_error_2 = self._writeTxRx(id_, servo.control_table['MIN_POSITION_LIMIT'], min_pos)

        # Check communication
        if self._check_communication(id_, 'MAX_POSITION_LIMIT', dxl_comm_result_1, dxl_error_1, val=max_pos) and \
           self._check_communication(id_, 'MIN_POSITION_LIMIT', dxl_comm_result_2, dxl_error_2, val=min_pos):
            servo.position_limits['min'] = min_pos
            servo.position_limits['max'] = max_pos
            return True

        return False

    def read_temperature(self, ids: Union[int, List[int]]) -> Dict[int, int]:
        """
        Reads the current temperature of the servo(s).

        Args:
            ids (int or List[int]): The servo ID or a list of IDs.

        Returns:
            Dict[int, int]: A dictionary with servo IDs as keys and temperatures as values.
        """
        if isinstance(ids, int):
            ids = [ids]
        
        return {
            id_: self._read_temperature(id_)
            for id_ in ids
            if self._is_servo_registered(id_)
        }

    def _read_temperature(self, id: int) -> int:
        """
        Reads the current temperature of the servo.

        Args:
            id (int): The servo ID.

        Returns:
            Temperature(int): Temperature.
        """

        servo = self._get_servo(id)
        temperature, dxl_comm_result, dxl_error = self._readTxRx(id, servo.control_table['PRESENT_TEMPERATURE'])

        if self._check_communication(id, 'PRESENT_TEMPERATURE', dxl_comm_result, dxl_error, val=f"{temperature} °C"):
            return temperature
        else:
            return self.INVALID_INT_VAL

    def set_baudrate(self):
        """
        Sets the baud rate of the serial port.
        """
        if self.port_handler.setBaudRate(self.baudrate):
            self.logger.info(f"Port {self.port} Baudrate set to {self.baudrate}")
        else:
            self.logger.error(f"Port {self.port} Failed to set baudrate to {self.baudrate}")
            quit()

    def set_goal_pos(self, id_: int, goal_pos: int = 2047, duration_ms: int = 1000) -> bool:
        """
        Sets the goal position of the servo.

        Args:
            id_ (int): The servo ID.
            goal_pos (int, optional): The desired position. Defaults to 2047.
            duration_ms (int, optional): The movement duration in milliseconds. Defaults to 1000.

        Returns:
            bool: True if successful, False otherwise.
        """
        self.set_profile_time(id_, duration_ms)

        if not self._is_servo_registered(id_):
            return False
        servo = self._get_servo(id_)

        if servo.position_limits['min'] <= goal_pos <= servo.position_limits['max']:
            dxl_comm_result, dxl_error = self._writeTxRx(id_, servo.control_table['GOAL_POSITION'], goal_pos)
            return self._check_communication(id_, 'GOAL_POSITION', dxl_comm_result, dxl_error, val=goal_pos)
        else:
            return False

    def set_goal_pos_sync(self, ids: List[int], goal_positions: List[int], durations: List[int]) -> bool:
        """
        Sets the goal positions of multiple servos synchronously.

        Args:
            ids (int or List[int]): The servo ID or a list of IDs.
            goal_positions (int or List[int]): The desired positions corresponding to the IDs.
            durations (int or List[int]): The movement durations in milliseconds corresponding to the IDs.

        Returns:
            bool: True if successful, False otherwise.
        """

        # Check if the data lengths match
        if len(ids) != len(goal_positions) or len(ids) != len(durations):
            return False

        pos_to_send = {}
        duration_to_send = {}

        for i in range(len(ids)):
            id_, pos, duration = ids[i], goal_positions[i], durations[i]

            # if not self._is_servo_registered(id_):
            #     return False
            servo = self._get_servo(id_)

            if servo.position_limits['min'] <= pos <= servo.position_limits['max']:
                # self.set_profile_time(id_, duration)
                pos_to_send[id_] = self._convert_to_bytes(pos, servo.control_table['GOAL_POSITION']['LEN'])
            duration_to_send[id_] = self._convert_to_bytes(duration, servo.control_table['PROFILE_VELOCITY']['LEN'])

        # Sync write duration and goal positions
        result_1 = self._sync_write('PROFILE_VELOCITY', duration_to_send)
        result_2 = self._sync_write('GOAL_POSITION', pos_to_send)

        if self._check_communication(id=255, cmd='PROFILE_VELOCITY', dxl_comm_result=result_1) and \
                self._check_communication(id=255, cmd='GOAL_POSITION', dxl_comm_result=result_2):
            return True
        else:
            return False

    def set_operating_mode(self, ids: Union[int, List[int]], op_mode: str = 'position') -> bool:
        """
        Sets the operating mode of the servo(s).

        Args:
            ids (int or List[int]): The servo ID or a list of IDs.
            op_mode (str, optional): The desired operating mode. Defaults to 'position'.

        Returns:
            bool: True if successful, False otherwise.
        """
        mode_mapping = {
            'current': 0,
            'velocity': 1,
            'position': 3,
            'extended_pos': 4,
            'current_pos': 5,
            'pwm': 16
        }
        op_mode_value = mode_mapping.get(op_mode)

        if isinstance(ids, int):
            ids = [ids]

        for id_ in ids:
            if not self._is_servo_registered(id_):
                continue

            servo = self._get_servo(id_)
            dxl_comm_result, dxl_error = self._writeTxRx(id_, servo.control_table['OPERATING_MODE'], op_mode_value)

            if self._check_communication(id_, 'OPERATING_MODE', dxl_comm_result, dxl_error, val=op_mode_value):
                servo.operating_mode = op_mode

            servo.operating_mode = op_mode

        return True
    
    def set_profile_time(self, id_: int, duration_ms: int = 1000) -> bool:
        """
        Sets the profile time of the servo.

        Args:
            id_ (int): The servo ID.
            duration_ms (int, optional): The profile time in milliseconds. Defaults to 1000.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._is_servo_registered(id_):
            return False
        servo = self._get_servo(id_)

        dxl_comm_result, dxl_error = self._writeTxRx(id_, servo.control_table['PROFILE_VELOCITY'], duration_ms)

        if servo.drive_mode == 'time':
            return self._check_communication(id_, 'PROFILE_TIME', dxl_comm_result, dxl_error, val=duration_ms)
        else:
            return False

    def set_torque(self, ids: Union[int, List[int]], enable: int = 0) -> bool:
        """
        Enables or disables the torque of the servo(s).

        Args:
            ids (int or List[int]): The servo ID or a list of IDs.
            enable (int, optional): 1 to enable torque, 0 to disable. Defaults to 0.

        Returns:
            bool: True if successful, False otherwise.
        """
        if isinstance(ids, int):
            ids = [ids]
        if len(ids) == 0:
            return False

        success = True

        data = {}
        servo = None

        for id_ in ids:
            if not self._is_servo_registered(id_):
                continue
            servo = self._get_servo(id_)
            data_len = servo.control_table['TORQUE_ENABLE']['LEN']
            # Construct dict to send
            data[id_] = self._convert_to_bytes(enable, data_len)

        # Sync write data
        result = self._sync_write('TORQUE_ENABLE', data)

        if self._check_communication(id=255, cmd='TORQUE_ENABLE', dxl_comm_result=result, val=enable):
            success &= True
        else:
            success &= False

        return success        # success = True 
        # if isinstance(ids, int):
        #     ids = [ids]
        #
        # for id in ids:
        #     if not self._is_servo_registered(id): # Check if servo(id) exists
        #         continue
        #     servo = self._get_servo(id)
        #
        #     dxl_comm_result, dxl_error = self._writeTxRx(id, servo.control_table['TORQUE_ENABLE'], enable)
        #     if self._check_communication(id, 'TORQUE_ENABLE', dxl_comm_result, dxl_error, val=enable):
        #         servo.torque_status = enable
        #         success &= True
        #     else: 
        #         success &= False

    def _convert_to_bytes(self, data, data_len):
        """
        Converts data to a list of bytes based on the data length.

        Args:
            data (int): The data to convert.
            data_len (int): The length of the data in bytes.

        Returns:
            List[int]: The data converted into a list of bytes.
        """
        if data_len == 4:
            data = [DXL_LOBYTE(DXL_LOWORD(data)), 
                    DXL_HIBYTE(DXL_LOWORD(data)), 
                    DXL_LOBYTE(DXL_HIWORD(data)), 
                    DXL_HIBYTE(DXL_HIWORD(data))]

        elif data_len == 2:
            data = [DXL_LOBYTE(DXL_LOWORD(data)),DXL_HIBYTE(DXL_LOWORD(data))]

        elif data_len == 1:
            data  = [DXL_LOBYTE(data)]

        else:
            return

        return data

    def enable_time_based_profile(self, id: int=1, time_profile: bool=True) -> bool:
        """
        Enables time-based profile for the servo.

        Args:
            id_ (int, optional): The servo ID. Defaults to 1.
            time_profile (bool, optional): True to enable time-based profile. Defaults to True.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._set_drive_mode(id, mode='profile', val=time_profile)
    
    def set_reverse_mode(self, id: int=1, reverse: bool=False) -> bool:
        """
        Args:
            id_ (int, optional): The servo ID. Defaults to 1.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._set_drive_mode(id, mode='reverse_mode', val=reverse) # velocity based profile is true when set to 0

    def enable_vel_based_profile(self, id: int=1, velocity_profile: bool=False) -> bool:
        """
        Enables velocity-based profile for the servo.

        Args:
            id_ (int, optional): The servo ID. Defaults to 1.
            velocity_profile (bool, optional): True to enable velocity-based profile. Defaults to False.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._set_drive_mode(id, mode='profile', val= not velocity_profile) # velocity based profile is true when set to 0

    def torque_on_by_goal_update(self, id: int=1, torque_on: bool=False) -> bool:
        """
        Sets the torque to be enabled by goal update.

        Args:
            id_ (int, optional): The servo ID. Defaults to 1.
            torque_on (bool, optional): True to enable torque on goal update. Defaults to False.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._set_drive_mode(id, mode='torque', val=torque_on)

    def set_secondary_id(self, ids, secondary_id=252) -> bool:
        """
        Sets the secondary ID for the servo(s).

        Args:
            ids (int or List[int]): The servo ID or a list of IDs.
            secondary_id (int, optional): The secondary ID to set. Defaults to 252.

        Returns:
            bool: True if successful, False otherwise.
        """
        success = True
        if isinstance(ids, int):
            ids = [ids]

        for id_ in ids:
            if not self._is_servo_registered(id_): # Check if servo(id) exis
                continue
            servo = self._get_servo(id_)
            
            dxl_comm_result, dxl_error = self._writeTxRx(id_, servo.control_table['SECONDARY_ID'], secondary_id)
            success &= self._check_communication(id_, 'SECONDARY_ID', dxl_comm_result, dxl_error, val=secondary_id)
        return success

    def close_port(self):
        """
        Closes the serial port.
        """
        self.port_handler.closePort()
        self.logger.info(f'\n------------------------------------------------')
        self.logger.info(f"[STATUS] Port {self.port} : Closed")
        self.logger.info(f'\n------------------------------------------------')

    def open_port(self):
        """
        Opens the serial port.
        """
        if self.port_handler.openPort():
            self.logger.info(f"Port {self.port} opened successfully.")
        else:
            self.logger.error(f"Failed to open port {self.port}.")
            # raise IOError(f"Cannot open port {self.port}")
            quit()

    def suppress_error_msg(self, suppress: bool):
        """
        Sets the suppression of error messages.

        Args:
            suppress (bool): True to suppress error messages, False otherwise.
        """
        self.SUPPRESS_ERROR_MSG = suppress
    
    def ping(self, id_):
        """
        Pings the servo to check its existence.

        Args:
            id_ (int): The servo ID.

        Returns:
            int: The model number if successful, INVALID_INT_VAL otherwise.
        """
        model_number, result, error = self.protocol_handler.ping(self.port, id_)
        if self._check_communication(id_, 'PING', result, error, val=model_number):
            return model_number
        else:
            return self.INVALID_INT_VAL

    def _check_communication(self, id, cmd, dxl_comm_result, dxl_error=0, val=None):
        """
        Checks the communication result and handles errors.

        Args:
            id_ (int): The servo ID.
            cmd (str): The command name.
            dxl_comm_result (int): The communication result code.
            dxl_error (int, optional): The error code from the servo. Defaults to 0.
            val (Optional[Union[int, str]], optional): The value associated with the command. Defaults to None.

        Returns:
            bool: True if communication was successful, False otherwise.
        """
        if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
            error_msg = f'[ERROR] ID: {id} CMD: {cmd} VAL: {val}\n'
            error_msg += f'{self.packet_handler.getTxRxResult(dxl_comm_result)}\n'
            error_msg += f'{self.packet_handler.getRxPacketError(dxl_error)}'
            if not self.SUPPRESS_ERROR_MSG:
                self.logger.error(error_msg)
        return True

    def _set_drive_mode(self, id: int=1, mode: str="profile", val: bool=False) -> bool:
        """
        Sets the drive mode of the servo.

        Args:
            id_ (int, optional): The servo ID. Defaults to 1.
            mode (str, optional): The drive mode to set. Options are 'normal mode', 'profile', 'torque'. Defaults to "profile".
            val (bool, optional): The value to set for the mode. Defaults to False.

        Returns:
            bool: True if successful, False otherwise.
        """ 
        
        # Check if servo(id) exists
        if not self._is_servo_registered(id): 
            return False
        servo = self._get_servo(id)
        
        # Different modes
        NORMAL_REVERSE_MODE = 0
        PROFILE_CONFIG = 2
        TORQUE_ON_BY_GOAL_UPDATE = 3

        if mode == 'reverse_mode':
            bit_pos = NORMAL_REVERSE_MODE
        elif mode == 'profile':
            bit_pos = PROFILE_CONFIG
        elif mode == 'torque':
            bit_pos = TORQUE_ON_BY_GOAL_UPDATE
        else:
            return False
         
        current_mode, dxl_comm_result, dxl_error = self._readTxRx(id, servo.control_table['DRIVE_MODE'])
        # new_mode = current_mode & ~(1 << bit_pos) if val else current_mode | (1 << bit_pos) # Set bit pos
        if val:
            new_mode = current_mode | (1 << bit_pos)
        else:
            new_mode = current_mode & ~(1 << bit_pos)
            
        dxl_comm_result, dxl_error = self._writeTxRx(id, servo.control_table['DRIVE_MODE'], new_mode)
        self.logger.info(f"{new_mode}")
        return self._check_communication(id, 'DRIVE_MODE', dxl_comm_result, dxl_error, current_mode) 
   
    def _get_servo(self, id):
        """
        Retrieves the Servo instance for the given ID.

        Args:
            id_ (int): The servo ID.

        Returns:
            Servo: The Servo instance.
        """
        # if id not in self.servos.keys():
        #     print(f"Servo ID {id} not found")
        #     raise
        servo = self.servos[id]
        return servo

    def _is_servo_registered(self, id_):
        """
        Checks if a servo is registered.

        Args:
            id_ (int): The servo ID.

        Returns:
            bool: True if the servo is registered, False otherwise.
        """
        return id_ in self.servos.keys()

    # Simplified packet handler for: Read Rx
    def _readRx(self, id_, cmd: dict):
        if cmd['LEN'] == 1:     data_read, result, error = self.protocol_handler.read1ByteRx(self.port_handler, id_)
        elif cmd['LEN'] == 2:   data_read, result, error = self.protocol_handler.read2ByteRx(self.port_handler, id_)
        else: data_read, result, error = self.protocol_handler.read4ByteRx(self.port_handler, id_)
        return data_read, result, error

    # Simplified packet handler for: Read Tx
    def _readTx(self, id_, cmd: dict):
        result = self.protocol_handler.readTx(self.port_handler, id_, cmd['ADDR'], cmd['LEN'])
        return result

    # Simplified packet handler for: Read TX/RX
    def _readTxRx(self, id_, cmd: dict):
        if cmd['LEN'] == 1:     data_read, result, error = self.protocol_handler.read1ByteTxRx(self.port_handler, id_, cmd['ADDR'])
        elif cmd['LEN'] == 2:   data_read, result, error = self.protocol_handler.read2ByteTxRx(self.port_handler, id_, cmd['ADDR'])
        else: data_read, result, error = self.protocol_handler.read4ByteTxRx(self.port_handler, id_, cmd['ADDR'])
        return data_read, result, error

    # Simplified packet handler for: Write TX Only
    def _writeTx(self, id_, cmd: dict, data):
        if cmd['LEN'] == 1:     result = self.protocol_handler.write1ByteTxOnly(self.port_handler, id_, cmd['ADDR'], data)
        elif cmd['LEN'] == 2:   result = self.protocol_handler.write2ByteTxOnly(self.port_handler, id_, cmd['ADDR'], data)
        else: result = self.protocol_handler.write4ByteTxOnly(self.port_handler, id_, cmd['ADDR'], data)
        return result

    # Simplified packet handler for: Write TX/RX
    def _writeTxRx(self, id_, cmd: dict, data):
        if cmd['LEN'] == 1:     result, error = self.protocol_handler.write1ByteTxRx(self.port_handler, id_, cmd['ADDR'], data)
        elif cmd['LEN'] == 2:   result, error = self.protocol_handler.write2ByteTxRx(self.port_handler, id_, cmd['ADDR'], data)
        else: result, error = self.protocol_handler.write4ByteTxRx(self.port_handler, id_, cmd['ADDR'], data)
        return result, error

    def add_bulk_param(self, id_, cmd: dict, data) -> bool:
        return self.groupBulkWrite.addParam(id_, cmd['ADDR'], cmd['LEN'], data)
    
    def remove_bulk_param(self, id_):
        return self.groupBulkWrite.removeParam(id_)

    def clear_bulk_param(self):
        self.groupBulkWrite.clearParam()

    def startup_config(self, id_, restore_ram=True, torque_enable=False) -> bool:
        
        # Check if servo(id_) exists
        if not self._is_servo_registered(id_): 
            return False
        servo = self._get_servo(id_)
        
        # Different modes
        STARTUP_TORQUE_ON = 0
        RAM_RESTORE = 1

        current_config, del_comm_result, dxl_error = self._readTxRx(id_, servo.control_table['STARTUP_CONFIGURATION'])

        # new_mode = current_mode & ~(1 << bit_pos) if val else current_mode | (1 << bit_pos) # Set bit pos
        if torque_enable:
            current_config = current_config | (1 << STARTUP_TORQUE_ON)
        else:
            current_config = current_config & ~(1 << STARTUP_TORQUE_ON)
            
        if restore_ram:
            current_config = current_config | (1 << RAM_RESTORE)
        else:
            current_config = current_config & ~(1 << RAM_RESTORE)

        dxl_comm_result, dxl_error = self._writeTxRx(id_, servo.control_table['STARTUP_CONFIGURATION'], current_config)

        return self._check_communication(id_, 'DRIVE_MODE', dxl_comm_result, dxl_error, current_config) 
    
    def _sync_write(self, cmd_name: str, data: dict):
        self._groupSyncWrite.clearParam()
        models = {}
        # モデルごとにデータをグループ化
        for id_ in data.keys():
            servo = self._get_servo(id_)
            model = servo.model
            if model not in models:
                models[model] = []
            models[model].append((id_, data[id_]))
        # 各モデルグループごとにsync writeを実行
        for model in models:
            first_servo = self._get_servo(models[model][0][0])
            cmd = first_servo.control_table[cmd_name]
            self._groupSyncWrite.start_address = cmd['ADDR']
            self._groupSyncWrite.data_length = cmd['LEN']
            for id_, param_data in models[model]:
                self._groupSyncWrite.addParam(id_, param_data)
            result = self._groupSyncWrite.txPacket()
            self._groupSyncWrite.clearParam()
            if result != COMM_SUCCESS:
                return result
        return COMM_SUCCESS

    def _bulk_write(self) -> bool:
        return self.groupBulkWrite.txPacket()
        # if self.groupBulkWrite.txPacket(): 
        #     self.clear_bulk_param()
        #     return True
        # else: 
        #     return False
        #
    
    def _bulk_read(self, data: dict):
        """
        data = {
                id: cmd
                }
        """
        for id_ in data.keys():
            cmd = data[id_]
            add_param_result = self.groupBulkRead.addParam(dxl_id=id_, start_address=cmd["ADDR"], data_length=cmd["LEN"])
            if add_param_result != True: self.logger.error(f"ID {id_}: Add param failed")
        
        dxl_comm_result = self.groupBulkRead.txRxPacket()
        if dxl_comm_result != True: 
            self.logger.error(f"Bulk read failed")
        
        for id_ in data.keys():
            cmd = data[id_]
            if self.groupBulkRead.isAvailable(id, cmd["ADDR"], cmd["LEN"]):
                result = self.groupBulkRead.getData(id, cmd["ADDR"], cmd["LEN"])
                print(result)

    def reboot(self, id):
        """
        Reboots the servo.

        Args:
            id (int): The servo ID.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._is_servo_registered(id):
            return False
        result, error = self.packet_handler.reboot(self.port_handler, self.protocol_version, id)
        return self._check_communication(id, 'REBOOT', result, error)
# dxl = DynamixelSDKWrapper(port='COM4')
#
# servos = {
#         'servo 1': {'id': 1, 'model': 'XC330', 'op_mode': 'extended_pos', 'reverse_mode': True},
#             'servo 2': {'id': 3, 'model': 'XC330', 'op_mode': 'extended_pos', 'reverse_mode': True},
# }
#
#
# dxl.add_servo(servos)
#
# # dxl.torque_enable(3, 1)
# # # dxl.torque_enable(9, 1)
# dxl.set_torque([1,3], 1)
#
# # data = {1: {'ADDR': 132,  'LEN': 4},
# #         2: {'ADDR': 132,  'LEN': 4}}
#
# # for i in range(10):
# #     print(dxl._bulk_read(data))
# #     time.sleep(1)
# t = 1000
# # dxl.set_goal_pos_syc(ids=[1, 3], goal_positions=[5000, 5000], durations=[t, t])
#
# dxl.set_goal_pos(id_=1, goal_pos=5000, duration_ms=t)
#
# time.sleep(t//1000)
# dxl.set_torque([1,3], 0)
# dxl.close_port()




