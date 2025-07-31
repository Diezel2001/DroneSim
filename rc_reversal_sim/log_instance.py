from collections import deque
import os

class DroneLog:

    def __init__(self, _logpath = None):
        self.load_logpath(_logpath)
        
    def load_logpath(self, _logpath):
        if validate_log_path(_logpath):
            self.logpath = _logpath
        else:
            print("Warning: logpath invalid")
            self.logpath = None

    def parse_log(self):
        if self.load_logpath is None:
            print("Error: Unable to parse log, logpath invalid")
            return
        
        # === Parse logpath ===
        

    

def validate_log_path(logpath):
    # Check if the path exists and is a file
    if not os.path.isfile(logpath):
        print("❌ Not a valid file path.")
        return False

    # Check if filename ends with "_log.txt"
    if not logpath.endswith("_log.csv"):
        print("❌ File does not end with '_log.txt'.")
        return False

    print("✅ Valid log path.")
    return True