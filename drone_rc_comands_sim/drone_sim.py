import numpy as np
import matplotlib
from dataclasses import dataclass
import sys

# === Use TkAgg backend for interactive plotting ===
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from drone_instance import DroneInstance

class DroneSim:
    # === Simulation Constants ===
    @dataclass(frozen=True)
    class Constants:
        GRAVITY: float = -9.81
        TIME_STEP: float = 0.1
        NEUTRAL: int = 1500
        THROTTLE_NEUTRAL: int = 1000
        YAW_SCALE = np.pi
        RC_SCALE: float = 0.005
        DRAG: float = 0.9

    colors = ['red', 'orange', 'green', 'blue','yellow']
    drones = []

    def __init__(self, logs):
        # === Initialize Canvas ===
        self.init_plot_setup()

        # === Initialize Drone Instances ===
        # if len(logs) <= 5:
        #     for i, log in enumerate(logs):
        #         self.drones.append(DroneInstance(self.colors[i], self.canvas, self.Constants, i))
        # else:
        #     print("Error: too many log inputs")

        # === for testing ===
        if int(logs) <= 5:
            for i in range(int(logs)):
                self.drones.append(DroneInstance(self.colors[i], self.canvas, self.Constants, i))
        else:
            print("Error: too many drones")

    # === 3D Plotting Setup ===
    def init_plot_setup(self):
        self.fig = plt.figure()
        self.canvas = self.fig.add_subplot(111, projection='3d')

    # === Animation Frame Update ===
    def animate(self,i,_drone):
        _drone.update_physics(i)
        # === Extract Current Position ===
        x, y, z = _drone.positions[-1]

        # === Update Drone Dot and Path ===
        _drone.drone_dot.set_data([x], [y])
        _drone.drone_dot.set_3d_properties(z)

        path = np.array(_drone.positions)
        _drone.path_line.set_data(path[:, 0], path[:, 1])
        _drone.path_line.set_3d_properties(path[:, 2])

        # === Dynamic Axis Expansion ===
        padding = 1.0
        x_min, x_max = self.canvas.get_xlim()
        y_min, y_max = self.canvas.get_ylim()
        z_min, z_max = self.canvas.get_zlim()

        if x < x_min or x > x_max:
            self.canvas.set_xlim(min(x_min, x - padding), max(x_max, x + padding))
        if y < y_min or y > y_max:
            self.canvas.set_ylim(min(y_min, y - padding), max(y_max, y + padding))
        if z < z_min or z > z_max:
            self.canvas.set_zlim(min(z_min, z - padding), max(z_max, z + padding))
        # -------------------------------

        return _drone.drone_dot, _drone.path_line
    
    def multi_animate(self,i):
        for drone in self.drones:
            self.animate(i, drone)

    # === Initialize Plot Axes ===
    def init_plot(self):
        self.canvas.set_xlim(-5, 5)
        self.canvas.set_ylim(-5, 5)
        self.canvas.set_zlim(0, 10)
        self.canvas.set_xlabel("X")
        self.canvas.set_ylabel("Y")
        self.canvas.set_zlabel("Z")
        # return self.drone.drone_dot, self.drone.path_line

    def run(self):
        # === Run Animation ===
        ani = FuncAnimation(
            self.fig,
            self.multi_animate,
            init_func=self.init_plot,
            # frames=len(rc_sequence),
            interval=100,
            blit=False,
            repeat=False  # <<< prevent looping
        )

        plt.title("RC Command Drone Simulator")
        plt.show() 









