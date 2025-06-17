import PySimpleGUI as sg
import pandas as pd
import ast
from Hand import Hand
import time, os, csv
import socket
import select
import threading




class Hand_GUI:

    def __init__(self) -> None:
        self.torque = False
        self.hand = Hand()
        self.hand.set_torque(self.torque)
        self.t = 2000 # Default time profile
        self.current_waypoint = 0
        self.replay = 0
        self.folder_path = "./data"
        self.csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
        self.selected_file = ""
        self.recording_file = ""
        self.param = self.hand.finger_parameters    
        self.auto_mode = False
        self.max_waypoint = 0
        self.connect_matlab = False

        self.layout = [
            [sg.TabGroup([
                [sg.Tab("Control", self._control_layout()), sg.Tab("Calibration", self._calibration_layout())]
            ])]
        ]

        self.finger_keys = ["THUMB", "INDEX", "MIDDLE", "RING", "PINKY"]
        self.finger_joint_keys = ['THUMB_MCP', 'THUMB_MCP_ABD', 'THUMB_PIP', 'THUMB_DIP',
            'INDEX_MCP', 'INDEX_MCP_ABD', 'INDEX_PIP', 'INDEX_DIP',
            'MIDDLE_MCP', 'MIDDLE_MCP_ABD', 'MIDDLE_PIP', 'MIDDLE_DIP',
            'RING_MCP', 'RING_MCP_ABD', 'RING_PIP', 'RING_DIP',
            'PINKY_MCP', 'PINKY_MCP_ABD', 'PINKY_PIP', 'PINKY_DIP',
            "WRIST_HORIZONTAL", "WRIST_VERTICAL", "ABDUCTION_THUMB_ABD", "ABDUCTION_PINKY_ABD"]
        self.calibration_keys = [
            "THUMB_MCP_M",      "THUMB_MCP_P",      "THUMB_MCP_ABD_M",  "THUMB_MCP_ABD_P",  "THUMB_PIP_M",  "THUMB_PIP_P",  "THUMB_DIP_M",  "THUMB_DIP_P",
            "INDEX_MCP_ABD_M",  "INDEX_MCP_ABD_P",  "INDEX_MCP_M",      "INDEX_MCP_P",      "INDEX_PIP_M",  "INDEX_PIP_P",  "INDEX_DIP_M",  "INDEX_DIP_P",
            "MIDDLE_MCP_ABD_M", "MIDDLE_MCP_ABD_P", "MIDDLE_MCP_M",     "MIDDLE_MCP_P",     "MIDDLE_PIP_M", "MIDDLE_PIP_P", "MIDDLE_DIP_M", "MIDDLE_DIP_P",
            "RING_MCP_ABD_M",   "RING_MCP_ABD_P",   "RING_MCP_M",       "RING_MCP_P",       "RING_PIP_M",   "RING_PIP_P",   "RING_DIP_M",   "RING_DIP_P",
            "PINKY_MCP_ABD_M",  "PINKY_MCP_ABD_P",  "PINKY_MCP_M",      "PINKY_MCP_P",      "PINKY_PIP_M",  "PINKY_PIP_P",  "PINKY_DIP_M",  "PINKY_DIP_P",
            "ABDUCTION_THUMB_ABD_M", "ABDUCTION_THUMB_ABD_P", "ABDUCTION_PINKY_ABD_M", "ABDUCTION_PINKY_ABD_P",
            "WRIST_HORIZONTAL_M", "WRIST_HORIZONTAL_P", "WRIST_VERTICAL_M", "WRIST_VERTICAL_P"]
        
        # Create the window
        self.window = sg.Window("Robot Hand Control", self.layout, finalize=True)
        sg.theme('DarkAmber')
        
        if self.connect_matlab:
            self.host = 'localhost'
            self.port = 5000
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(0.1)
            self.s.connect((self.host, self.port))
        
            # Connect to the server
            self.matlab_thread = MatlabConnection(server=self.s, port=self.port, host=self.host)
            self.matlab_thread.start()

    def _calibration_layout(self):
        
        row_title = ["FINGER", "MCP_ABD/ADD", "MCP", "PIP", "DIP"]
        calibration_layout = [
                [sg.Text(title,size=(15,1),justification='center') for title in row_title],
                self.finger_calibration_layout('thumb', ['mcp_abd', 'mcp', 'pip', 'dip']),
                self.finger_calibration_layout('index', ['mcp_abd', 'mcp', 'pip', 'dip']),
                self.finger_calibration_layout('middle', ['mcp_abd', 'mcp', 'pip', 'dip']),
                self.finger_calibration_layout('ring', ['mcp_abd', 'mcp', 'pip', 'dip']),
                self.finger_calibration_layout('pinky', ['mcp_abd', 'mcp', 'pip', 'dip']),
                self.finger_calibration_layout('abduction', ['thumb_abd', 'pinky_abd']),
                self.finger_calibration_layout('wrist', ['horizontal', 'vertical']),

                [sg.Button("Torque", key="TORQUE_TOGGLE"), sg.Text(f"{'On' if self.torque else 'Off'}",key='TORQUE_1'), sg.Button("Close",key="CLOSE_2")], 
        ]
        return calibration_layout

    def _control_layout(self):
        row_title = ["FINGER", "MOVE ALL JOINTS", "MCP_ABD/ADD", "MCP", "PIP", "DIP"]
        control_layout = [
            # [sg.Text("Text here")],
            # [sg.InputText()],
            [sg.Text("Time  ",size=(15,1)), 
             sg.Slider(range=(50, 5000),default_value=2000,resolution=50,orientation='horizontal',enable_events=True,key="TIME")],
            
            [sg.Text(title,size=(15 if title == "FINGER" else 20,1),justification='center') for title in row_title],
            self.finger_control_layout('thumb', ['mcp_abd', 'mcp', 'pip', 'dip']),
            self.finger_control_layout('index', ['mcp_abd', 'mcp', 'pip', 'dip']),
            self.finger_control_layout('middle', ['mcp_abd', 'mcp', 'pip', 'dip']),
            self.finger_control_layout('ring', ['mcp_abd', 'mcp', 'pip', 'dip']),
            self.finger_control_layout('pinky', ['mcp_abd', 'mcp', 'pip', 'dip']),

            [sg.Text("THUMB_ABD/ADD",size=(15,1),justification="center"), 
             sg.Slider(range=(0, 100),default_value=0,resolution=5,orientation='horizontal',enable_events=True,key="ABDUCTION_THUMB_ABD"),
             sg.Text("PINKY_ABD/ADD",size=(15,1),justification="center"), 
             sg.Slider(range=(0, 100),default_value=0,resolution=5,orientation='horizontal',enable_events=True,key="ABDUCTION_PINKY_ABD")],
            
            [sg.Text("WRIST_HORIZONTAL",size=(15,1),justification="center"), 
             sg.Slider(range=(0, 100),default_value=0,resolution=5,orientation='horizontal',enable_events=True,key="WRIST_HORIZONTAL"),
             sg.Text("WRIST_VERTICAL",size=(15,1),justification="center"), 
             sg.Slider(range=(0, 100),default_value=0,resolution=5,orientation='horizontal',enable_events=True,key="WRIST_VERTICAL")],
            [sg.Text("Create a Recording (enter file name): "), 
             sg.InputText(key="FILENAME"),
             sg.Text(f"{self.recording_file}",key="Recording: {}"),
             sg.Button("Create")],
            [sg.Text("Select a CSV File:"), sg.Combo(self.csv_files, size=(30, 1), key="CSV_FILE"), 
             sg.Text(f"{self.selected_file}",key="FILE"), sg.Button("Load"), sg.Button("Unload"), sg.Button("Refresh")],
            [sg.Button("PREVIOUS"), sg.Text(f"{self.current_waypoint}",key="WAYPOINT"), sg.Button("NEXT",key="NEXT")], 
            [sg.Button("Torque"), sg.Text(f"{'On' if self.torque else 'Off'}",key='TORQUE'), sg.Button("Close",key="CLOSE_1"), 
             sg.Button("Record",key="RECORD"), sg.Text(f"{self.recording_file}",key="RECORD_FILE"), sg.Button("Capture Frame",key="CAPTURE"), 
             sg.Button("Stop Capture",key="STOP_CAPTURE"), sg.Text("Auto Mode"), sg.Button("Auto Mode", key='AUTO'),sg.Text(f"{'On' if self.auto_mode else 'Off'}",key='AUTO_TEXT')], 
            
        ]
        return control_layout

    def _finger_joint_callback(self, event, values):
        parts = event.split("_")
        finger = parts[0].lower()
        joint = "_".join(parts[1:]).lower()
        joint_val = self.convert_to_joint_angle(finger=finger, joint_name=joint, param=self.param, val=values[event])
        self.hand.update_finger_joint(finger_name=finger, param={joint: joint_val})
        self.hand.move_finger([finger], t_exec=self.t)

    def _finger_callback(self, event, values):
        finger = event.lower()
        val = values[event]
        mcp = self.convert_to_joint_angle(finger=finger, joint_name='mcp', param=self.param, val=val)
        pip = self.convert_to_joint_angle(finger=finger, joint_name='pip', param=self.param, val=val)
        dip = self.convert_to_joint_angle(finger=finger, joint_name='dip', param=self.param, val=val)
        self.hand.update_finger_joint(finger_name=finger, param={'mcp': mcp, 'pip': pip, 'dip': dip})
        self.hand.move_finger([finger], t_exec=self.t)

    def _replay_callback(self, event):
        if self.selected_file == "": return
        if event == "PREVIOUS":
            self.current_waypoint = self.current_waypoint - 1 if self.current_waypoint >= 1 else 0
        else: 
            self.current_waypoint += 1
        data, waypoint = self._reconstruct_data(file_path=self.selected_file, waypoint=self.current_waypoint)
        
        self.current_waypoint = waypoint
        self.window["WAYPOINT"].update(value=f'{self.current_waypoint}');
        print(f"Waypoint: {self.current_waypoint}")
        fingers_to_move = []
        if data is not None: 
            self.hand.set_hand_states(data)
            fingers_to_move = [finger for finger in data.keys()]
        

        self.hand.move_finger(fingers_to_move, t_exec=self.t)
        # Output the resulting dictionary
        self._update_window(data)

    def _update_window(self, data):
        for finger in data.keys():
            for joint in data[finger].keys():
                key = finger.upper() + "_" + joint.upper()
                joint_angle = data[finger][joint]['joint_angle']
                val = int(100*(joint_angle - self.param[finger][joint]['min_deg']) / (self.param[finger][joint]['max_deg'] - self.param[finger][joint]['min_deg']))
                self.window[key].update(value=val)

    def _capture_frame(self):
        self.s.sendall(("capture\n").encode())  # Append newline (\n) to message
    
    def _stop_capture_frame(self):
        self.s.sendall(("q\n").encode())  # Append newline (\n) to message

    def _reconstruct_data(self, file_path='file.csv', waypoint=0):

        df = pd.read_csv(f"./data/{file_path}")
        # Select the first row (or any row) to convert
        self.max_waypoint = len(df)
        if self.max_waypoint == 0: return None, 0
        if waypoint >= len(df): 
            waypoint = len(df) - 1

        row_data = df.iloc[waypoint].to_dict()

        if len(row_data) == 0: 
            print('Empty File')
            return None

        # Initialize the output dictionary structure
        data = {
            'thumb': {}, 'index': {}, 'middle': {}, 'ring': {}, 'pinky': {}, 
            'abduction': {}, 'wrist': {}
        }

        # Map data into nested dictionaries
        for key, value in row_data.items():
            if key == 'waypoint':  # Skip or handle this if necessary
                continue
            # Split key into categories
            parts = key.split('#')
            if len(parts) == 2:
                finger, joint = parts[0], parts[1]
                # Parse the value safely from string to dictionary
                joint_data = ast.literal_eval(value)
                if finger in data:
                    data[finger][joint] = joint_data
        return data, waypoint
    
    def _record_data(self):
        try: 
            data = self.hand.get_hand_states()
            joint_positions = [] # increment counts
            self.current_waypoint += 1

            for finger, joints in data.items():
                for joint in joints.keys():
                    joint_positions.append(data[finger][joint])

            file_exists = os.path.isfile(self.recording_file)
            if not file_exists: 
                print("no recording file")

            with open(self.recording_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(joint_positions)
        except: 
            return
    
    def _load_data(self, values):
        csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
        self.selected_file = values["CSV_FILE"]
        if not self.selected_file in csv_files:
            return
        self.window['FILE'].update(value=f"Selected: {self.selected_file}")
    
    def _create_recording(self, values):
        filename = values["FILENAME"]
        self.current_waypoint = 0

        if filename:           # Ensure the filename ends with .csv
            if not filename.endswith('.csv'):
                filename += '.csv'
            self.recording_file = './data/' + filename

            # Create an empty CSV file
            if not os.path.exists(self.recording_file):
                data = self.hand.get_hand_states()

                with open(self.recording_file, 'w', newline='') as file:
                    data = self.hand.get_hand_states()
                    joint_names = []
                    for finger, joints in data.items():
                        for joint in joints.keys():
                            joint_names.append(f"{finger}#{joint}") 

                    writer = csv.writer(file)
                    writer.writerow(joint_names)
                    # Optionally, you could write a header here if needed
                    # writer.writerow(['Column1', 'Column2', 'Column3'])
                sg.popup(f"CSV file '{self.recording_file}' created successfully!")
            else:
                sg.popup(f"File '{self.recording_file}' already exists.")
        else:
            sg.popup("Please enter a valid filename!")
        self.window["RECORD_FILE"].update(value=f'{self.recording_file}')

    def _calibration_callback(self, event, increment_val=100):
        sign = 1 if event[-2:] == "_P" else -1 # find the sign
        event = event[:-2].lower() # remove _P or _M
        parts = event.split("_")
        finger = parts[0]
        joint = "_".join(parts[1:])

        offset = self.hand.fingers[finger].params[joint]['offset']# get current offset
        self.hand.set_calibration_offset(finger, joint, offset + sign * increment_val)
        self.hand.fingers[finger].move_joint(joint, t_exec=self.t)
        print(event.upper() + "_TEXT")
        self.window[event.upper() + "_TEXT"].update(value=f"{self.param[finger][joint]['offset']}")

    @staticmethod
    def convert_to_joint_angle(finger, joint_name, param, val):
        finger = finger.lower()
        result = int((param[finger][joint_name]['max_deg'] - param[finger][joint_name]['min_deg']) * val/100 + param[finger][joint_name]['min_deg'])
        return result

    def finger_control_layout(self, finger, joints):
        layout = []
        FINGER = finger.upper()
        layout.append(sg.Text(FINGER, size=(15, 1)))
        layout.append(sg.Slider(range=(0,   100),default_value=0,resolution=10,orientation='horizontal',enable_events=True,key=f"{FINGER}"),)

        for joint in joints:
            JOINT = joint.upper()
            layout.append(sg.Slider(range=(0,   100),default_value=0,resolution=10,orientation='horizontal',enable_events=True,key=f"{FINGER}_{JOINT}"))
            
        return layout

    def finger_calibration_layout(self, finger, joints):
        layout = []
        FINGER = finger.upper()
        layout.append(sg.Text(FINGER, key=f"{FINGER}_TEXT", size=(15, 1)))

        for joint in joints:
            JOINT = joint.upper()
            layout.append(sg.Button("-", key=f"{FINGER}_{JOINT}_M", size=(2, 1)))
            layout.append(sg.Text(f"{self.param[finger][joint]['offset']}", key=f"{FINGER}_{JOINT}_TEXT", size=(5, 1)))
            layout.append(sg.Button("+", key=f"{FINGER}_{JOINT}_P", size=(2, 1)))
            
        return layout
    
    def run_gui(self):

        # Event loop to process "events"and get the "values" of hte inputs
        while True: 

            event, values = self.window.read()
            # If user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == "CLOSE" or event == "CLOSE_1" or event == "CLOSE_2": break

            if event == "TIME":
                self.t = int(values["TIME"])
            
            if event in self.finger_keys:
                self._finger_callback(event, values)    

            if event in self.finger_joint_keys:
                self._finger_joint_callback(event, values)
            
            if event == "Torque":
                self.torque = not self.torque
                self.hand.set_torque(self.torque)
                self.window["TORQUE"].update(value=f'{"On" if self.torque else "Off"}');

            if event in ["NEXT", "PREVIOUS"]:
                # time.sleep(5)
                self._replay_callback(event)

            if event == "RECORD":
                self._record_data()

            if event == "Load":
                self._load_data(values) 

            if event == "Unload":
                self.selected_file = ""
                self.window['FILE'].update(value=f"Selected: {self.selected_file}")

            if event == "Refresh":
                csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
                self.window["CSV_FILE"].update(values=csv_files, size=(30, 10),)

            if event == "Create":
                self._create_recording(values)

            if event == "CAPTURE":
                if self.selected_file == "": continue

                if self.connect_matlab:
                    self._capture_frame()
                    if self.auto_mode:
                        if self.current_waypoint >= self.max_waypoint-1:
                            self.current_waypoint = -1
                        time.sleep(0.5)
                        self._replay_callback("NEXT")

            if event == "STOP_CAPTURE": 
                if self.connect_matlab:
                    self._stop_capture_frame() 

            if event in self.calibration_keys:
                self._calibration_callback(event)
             
            if event == "AUTO":
                self.auto_mode = not self.auto_mode
                self.window['AUTO_TEXT'].update(value=f"{'On' if self.auto_mode else 'Off'}")
        
        if self.connect_matlab:
            self.matlab_thread.stop()
            self.matlab_thread.join()

    def __def__(self):
        self.hand.set_torque(False)
        self.hand.__del__()
        self.window.close()

    def main(self):
        self.run_gui()


class MatlabConnection(threading.Thread):
    def __init__(self, server, port=5000, host='localhost'):
        super().__init__()
        
        # for MATLAB communication
        self.host = host
        self.port = port
        self.server = server
        self.stop_event = threading.Event()

    def run(self):
        print("Thread started.")

        while not self.stop_event.is_set():
            try:
                response = self.server.recv(1024).decode()
                print(response,end="")
            except ConnectionAbortedError:
                print("Connection was aborted. Attempting to reconnect...")
                self.reconnect()  # Implement a reconnect function
            except ConnectionResetError:
                print("Connection reset by peer. The server might have closed the connection.")
                time.sleep(1)
            except socket.timeout:
                pass
        print("Thread stopped.")
        self.server.close()

    def stop(self):
        self.stop_event.set()  # Signal thread to stop

    def reconnect(self):
        while True:
            try:
                print("Reconnecting...")
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.connect((self.host, self.port))
                print("Reconnected successfully!")
                break
            except socket.error:
                print("Reconnect failed. Retrying in 5 seconds...")
                time.sleep(5)

if __name__ == "__main__":
    hand_gui = Hand_GUI()
    hand_gui.main()
    hand_gui.__def__()
    print("DONE")
