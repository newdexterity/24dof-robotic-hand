import time
import sys
import DynamixelSDKWrapper as dynamixel
import logging
import json

class Hand:
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] : %(message)s",
        datefmt="[%X]")
    
    # dxl = dynamixel.DynamixelSDKWrapper(port='/dev/ttyUSB0', baudrate=115200)
    dxl = dynamixel.DynamixelSDKWrapper(port='COM4', baudrate=115200)
    fingers = {}
    states = {}
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky', 'abduction', 'wrist']

    param_file_path = './params/finger_params.json'
    finger_parameters = {}

    def __init__(self) -> None:
        self.load_hand_params(self.param_file_path) 
        # Instantiate fingers and abduction/adduction
        self.fingers['thumb'] = Finger(finger_name='thumb', finger_params=self.finger_parameters["thumb"], servos=self.dxl)
        self.fingers['index'] = Finger(finger_name='index', finger_params=self.finger_parameters["index"], servos=self.dxl)
        self.fingers['middle'] = Finger(finger_name='middle', finger_params=self.finger_parameters["middle"], servos=self.dxl)
        self.fingers['ring'] = Finger(finger_name='ring', finger_params=self.finger_parameters["ring"], servos=self.dxl)
        self.fingers['pinky'] = Finger(finger_name='pinky', finger_params=self.finger_parameters["pinky"], servos=self.dxl)
        self.fingers['abduction'] = Finger(finger_name='abduction', finger_params=self.finger_parameters["abduction"], servos=self.dxl)
        self.fingers['wrist'] = Finger(finger_name='wrist', finger_params=self.finger_parameters["wrist"], servos=self.dxl)
        self.states = self.get_joint_states()
        self.logger = logging.getLogger(__name__)

    def __del__(self):    
        self.dxl.close_port()

    def get_joint_states(self):
        pass

    def update_finger_joint(self, finger_name: str, param: dict):
        if finger_name in self.fingers.keys():
            self.fingers[finger_name].update_finger_state(param)


    def move_finger(self, finger_name, t_exec: int=1000):
        
        if isinstance(finger_name, str):
            finger_name = [finger_name]
        for finger in finger_name:
            if finger in self.fingers.keys():
                self.fingers[finger].move_finger(t_exec)


    def move_finger_joint(self, finger_name: str, joint_name: str, val: int, t_exec: int=1000):
        if finger_name in self.fingers.keys():
            return self.fingers[finger_name].move_joint(joint_name, val, t_exec)
        else:
            return False
    
    # Set torque for all fingers
    def set_torque(self, enable=False):
        for finger in self.fingers.keys():
            # print(f'[{finger}] Set torque: {enable}')
            self.fingers[finger].set_torque(enable)
    
    def get_hand_states(self):
        self.states = {finger_name: self.fingers[finger_name].finger_state for finger_name in self.fingers.keys()}
        return self.states
    
    def get_hand_params(self):
        self.states = {finger_name: self.fingers[finger_name].params for finger_name in self.fingers.keys()}
        return self.states
    
    def save_hand_params(self):
        data = self.get_hand_params()

        with open(self.param_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def set_hand_states(self, hand_states):
        for finger_name in hand_states.keys():
            self.logger.info(f"{finger_name}, {hand_states[finger_name]}")
            self.fingers[finger_name].finger_state = hand_states[finger_name]
    
    def load_hand_params(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                self.finger_parameters = json.load(json_file)  # data is now a dictionary
                print(self.finger_parameters)
        except FileNotFoundError:
            raise

        # update finger instances
        

    def set_calibration_offset(self, finger_name: str, joint_name: str, servo_offset: int):
        self.fingers[finger_name].set_calibration_offset(joint_name, servo_offset)
        self.logger.info(f'{finger_name}-{joint_name}: offset set to {servo_offset}')
        self.save_hand_params() # save the param file
        # self.load_hand_states(self.param_file_path) # reload param file

class Finger:

    def __init__(self, finger_name: str, finger_params: dict, servos) -> None:
        self.params = finger_params
        self.finger_name = finger_name 
        self.servos = servos
        self.finger_state = {joint_name: {'joint_angle': finger_params[joint_name]['min_deg'], 'servo_pos': finger_params[joint_name]['min']} for joint_name in finger_params.keys()}
        self.servo_params = {
            joint_name: {
                'id': self.params[joint_name]['id'], 
                'model': 'XC330', 
                'op_mode': 'extended_pos', 
                'reverse_mode': self.params[joint_name]['reverse']
            } for joint_name in finger_params.keys()
        }

        self.servos.add_servo(self.servo_params)
        

    def map_to_servo(self, joint_name: str, joint_angle: int): # 0 when 180 for the servo

        # Conventions
        # Position zero @ servo == 180 deg
        # Flex = +ve
        # Extension: -ve
        # Right (from palmar side): +ve

        # Linear mapping
        m = (self.params[joint_name]['max'] - self.params[joint_name]['min']) / (self.params[joint_name]['max_deg'] - self.params[joint_name]['min_deg']) 
        c = self.params[joint_name]['max'] - m * self.params[joint_name]['max_deg']
        val = m * joint_angle + c
        print(val)
        if val > max(self.params[joint_name]['max'], self.params[joint_name]['min']): val = max(self.params[joint_name]['max'], self.params[joint_name]['min']) 
        if val < min(self.params[joint_name]['max'], self.params[joint_name]['min']): val = min(self.params[joint_name]['max'], self.params[joint_name]['min'])
        return int(val)


    def move_joint(self, joint='dip', t_exec=1000):
        if joint not in self.finger_state.keys():
            return False
        
        pos = self.finger_state[joint]['servo_pos'] + self.params[joint]['offset']
        self.servos.set_torque(self.params[joint]['id'], 1)
        return self.servos.set_goal_pos(self.params[joint]['id'], goal_pos=pos, duration_ms=t_exec)
    
    def move_finger(self, t_exec) -> bool:
        success = True
        ids, goal_pos, t = [], [], []
        for joint in self.finger_state.keys():
            if joint not in self.finger_state.keys():
                return False
            # print(joint, self.finger_state[joint])
            ids.append(self.params[joint]['id'])
            goal_pos.append(self.finger_state[joint]['servo_pos'] + self.params[joint]['offset'])
            t.append(t_exec)
            # success &= self.move_joint(joint, self.finger_state[joint], t_exec)
        self.servos.set_goal_pos_sync(ids, goal_pos, t)
        print(ids, goal_pos, t)
        return success

    def update_finger_state(self, joint_angle: dict={'mcp':None, 'mcp_abd':None, 'pip':None, 'dip':None, 'thumb_abd': None, 'pinky_abd': None}):
        for joint in joint_angle.keys():
            print(f'{joint}: {joint_angle[joint]}')
            if joint in self.finger_state.keys() and joint_angle[joint] is not None:
                self.finger_state[joint]['joint_angle'] = joint_angle[joint]
                self.finger_state[joint]['servo_pos'] = self.map_to_servo(joint, joint_angle[joint])
    
    
    def set_torque(self, enable):
        ids = []
        for servo in self.servo_params.keys():
            ids.append(self.servo_params[servo]['id'])
        self.servos.set_torque(ids, enable)

    def set_calibration_offset(self, joint_name: str, servo_offset: int):
        self.params[joint_name]['offset'] = servo_offset




