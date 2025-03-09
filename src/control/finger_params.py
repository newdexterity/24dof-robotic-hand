
params = {
    "thumb": {
        
        'mcp': {
            'id': 2,
            'min': 2200,
            'int': 2200,
            'max': 5000, # max flex
            'min_deg': 0,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        },
        
        'mcp_abd': {
            'id': 10,
            'min': 3500,
            'max': 5500,
            'int': 1300, # -1 if either min, or max is the middle point
            'min_deg': -20,
            'max_deg': 20, 
            'reverse': True,
            'offset': 0

        },

        'pip': {
            'id': 14,
            'min': 3400,
            'int': 3400,
            'max': 5500,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        },
        
        'dip': {
            'id': 18,
            'min': 3600,
            'int': 3600,
            'max': 6000,
            'min_deg': 0,
            'max_deg': 100, 
            'reverse': True,
            'offset': 0
        }
    },

    "index": {

        'mcp': {
            'id': 6,
            'min': 3600,
            'int': 3600,
            'max': 6500,
            'min_deg': 0,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        },

        'mcp_abd': {
            'id': 9,
            'min': 2100,
            'int': 2100, # -1 if either min, or max is the middle point
            'max': 4000, # 4500
            'min_deg': -15,
            'max_deg': 15, 

            'reverse': True,
            'offset': 0
        },

        'pip': { # to calibrate
            'id': 13,
            'min': 1900,
            'int': 1900,
            'max': 5000,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        },

        'dip': {
            'id': 17,
            'min': 3000,
            'int': 3000,
            'max': 5500,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        }
    },

    "middle": {

        'mcp': {
            'id': 4,
            'min': 3600,
            'int': 3600,
            'max': 6300, # 5500
            'min_deg': 0,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        },

        'mcp_abd': {
            'id': 8,
            'min': 2500,
            'int': 2500, # -1 if either min, or max is the middle point
            'max': 4500,
            'min_deg': -15,
            'max_deg': 15, 
            'reverse': True,
            'offset': 0
        },

        'pip': {
            'id': 12,
            'min':3400,
            'int': 3400,
            'max': 5700,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        },

        'dip': {
            'id': 16,
            'min': 180,
            'int': 180,
            'max': 3000,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        }
    },

    "ring": {
        'mcp': {
            'id': 3,
            'min': 1800,
            'int': 1800,
            'max': 4800,
            'min_deg': 0,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        },

        'mcp_abd': {
            'id': 7,
            'min': 3600,
            'int': 3600, # -1 if either min, or max is the middle point
            'max': 6500,
            'min_deg': -15,
            'max_deg': 15, 
            'reverse': True,
            'offset': 0
        },

        'pip': {
            'id': 15,
            'min': 1700,
            'int': 1700,
            'max': 5500,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        },
        
        'dip': {
            'id': 20,
            'min': 1000,
            'int': 1000,
            'max': 3000,
            'min_deg': 0,
            'max_deg': 90, 
            'reverse': True,
            'offset': 0
        }
    },

    "pinky": {
        'mcp': {
            'id': 1,
            'min': 2500,
            'int': 2500,
            'max': 5000, # 8200
            'min_deg': -5,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        },

        'mcp_abd': {
            'id': 5,
            'min': 1500,
            'int': 1500, # -1 if either min, or max is the middle point
            'max': 3000,
            'min_deg': -15,
            'max_deg': 15, 
            'reverse': True,
            'offset': 0
        },

        'pip': {
            'id': 11,
            'min': 1100,
            'int': 1100,
            'max': 4000,
            'min_deg': 0,
            'max_deg': 75, 
            'reverse': True,
            'offset': 0
        },

        'dip': {
            'id': 19,
            'min': 1400,
            'int': 1400,
            'max': 4800,
            'min_deg': -5,
            'max_deg': 80, 
            'reverse': True,
            'offset': 0
        }
    },

    "abduction": {
        'thumb_abd': {
            'id': 23,
            'min': 700,
            'int': 700,
            'max': 3000,
            'min_deg': 0,
            'max_deg': 40, 
            'reverse': True,
            'offset': 0
        },
        'pinky_abd': {
            'id': 22,
            'min': 3200,
            'int': 3200,
            'max': 4200,
            'min_deg': 0,
            'max_deg': 15, 
            'reverse': True,
            'offset': 0
        },
    },

    "wrist": {
        'wrist_vertical': {
            'id': 21,
            'min': 200,
            'int': 200,
            'max': 6500,
            'min_deg': -45,
            'max_deg': 45, 
            'reverse': False,
            'offset': 0
        },
        'wrist_horizontal': {
            'id': 24,
            'min': 2500,
            'int': 215,
            'max': 4500,
            'min_deg': -30,
            'max_deg': 15, 
            'reverse': false,
            'offset': 0
        },
    },
}