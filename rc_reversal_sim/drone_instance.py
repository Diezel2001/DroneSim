import sample_commands
from sample_commands import rc_commands
import numpy as np

class DroneInstance:
    def __init__(self, _color, _canvas, _constants, logs):

        # === Input variables ===
        self.color = _color
        self.canvas = _canvas
        self.constants = _constants
        
        self.yaw = 0.0  # in radians
        self.yaw_rate = 0.0

        # === Drone State Initialization ===
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.positions = []
    
        self.drone_dot, = self.canvas.plot([], [], [], color=self.color, marker='o', markersize=8)
        self.path_line, = self.canvas.plot([], [], [], color=self.color, linestyle='--', linewidth=1)

        # === Log Init ===
        self.rc_inputs = []
        print(f'logs :{logs}')
        print(rc_commands[logs])
        for cmd in rc_commands[logs]:
            self.rc_inputs += [cmd] * 50  # hold each command for 50 timesteps

    # === Physics Simulation ===
    def update_physics(self, frame_index):

        if frame_index <=  len(self.rc_inputs) - 1:
            throttle, pitch, roll, yaw = self.rc_inputs[frame_index]

            # === RC Input to Acceleration Mapping ===
            acc_y = -(roll - self.constants.NEUTRAL) * self.constants.RC_SCALE * 10      # left-right
            acc_x = (pitch - self.constants.NEUTRAL) * self.constants.RC_SCALE * 10       # forward-backward
            acc_z = ((throttle - self.constants.THROTTLE_NEUTRAL) * self.constants.RC_SCALE * 30) + self.constants.GRAVITY  # up-down

            # === Update yaw ===
            yaw_input_normalized = (yaw - self.constants.NEUTRAL) * self.constants.RC_SCALE
            yaw_rate = yaw_input_normalized * self.constants.YAW_SCALE
            self.yaw += yaw_rate * self.constants.TIME_STEP
            self.yaw = (self.yaw + np.pi) % (2 * np.pi) - np.pi  # normalize to [-π, π]

            # === Rotate local X/Y acceleration by yaw into global frame ===
            cos_yaw = np.cos(self.yaw)
            sin_yaw = np.sin(self.yaw)

            acc_x_global = acc_x * cos_yaw - acc_y * sin_yaw
            acc_y_global = acc_x * sin_yaw + acc_y * cos_yaw

            acceleration = np.array([acc_x_global, acc_y_global, acc_z])

            # acceleration = np.array([acc_x, acc_y, acc_z])

            # === Euler Integration with Damping ===
            self.velocity[:] += acceleration * self.constants.TIME_STEP
            self.velocity[:] *= self.constants.DRAG
            self.position[:] += self.velocity * self.constants.TIME_STEP

            # === Clamp to Ground (Z >= 0) ===
            if self.position[2] < 0:
                self.position[2] = 0
                if self.velocity[2] < 0:
                    self.velocity[2] = 0

            # === Store Updated Position ===
            self.positions.append(self.position.copy())
    
    def upload_log(self):
        pass
