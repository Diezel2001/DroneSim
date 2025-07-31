import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import numpy as np
import os
import csv
from datatypes import Vector3, Orientation, LogEntry, print_log_entry

class App3D:
    def __init__(self):
        self.drone_log_count = 0
        self.drone_instance = []
        self.containers = []

        gui.Application.instance.initialize()

        self.window = gui.Application.instance.create_window("Open3D 3D Viewer", 1024, 768)
        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(self.window.renderer)

        self._setup_layout()
        # self._add_3d_data()
        self._add_main_panel_controls()

    def _setup_layout(self):
        em = self.window.theme.font_size
        margin = 0.5 * em

        self.panel = gui.Vert(0.5 * em, gui.Margins(margin))
        self.window.add_child(self.scene)
        self.window.add_child(self.panel)

        def on_layout(layout_context):
            r = self.window.content_rect
            panel_width = 17 * em
            self.panel.frame = gui.Rect(r.get_right() - panel_width, r.y, panel_width, r.height)
            self.scene.frame = gui.Rect(r.x, r.y, r.width - panel_width, r.height)
            self.scene.scene.set_background([0, 0, 0, 1])

        self.window.set_on_layout(on_layout)

    def _add_3d_data(self):
        # Example: Point cloud
        np_points = np.random.uniform(-1, 1, size=(1000, 3))
        pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np_points))
        pcd.paint_uniform_color([0.2, 0.8, 0.2])

        material = rendering.MaterialRecord()
        material.shader = "defaultUnlit"
        self.scene.scene.add_geometry("random_points", pcd, material)
        bounds = pcd.get_axis_aligned_bounding_box()
        self.scene.setup_camera(60, bounds, bounds.get_center())

    def _add_main_panel_controls(self):
        label = gui.Label("Upload Drone Logs")

        # Editable Text Box
        self.logpath_input = gui.TextEdit()
        self.logpath_input.text_value = ""  # Start empty
        self.logpath_input.placeholder_text = "Input LogPath"

        # Button
        self.add_log_button = gui.Button("Add Log")
        self.add_log_button.set_on_clicked(self._on_add_log_button_click)
        self.panel.add_child(self.add_log_button)

        self.toggle_axes = gui.Checkbox("Show Axes")
        self.toggle_axes.set_on_checked(self._toggle_axes)

        self.panel.add_child(label)
        self.panel.add_child(self.logpath_input)
        self.panel.add_child(self.add_log_button)
        self.panel.add_fixed(5)
        self.panel.add_child(self.toggle_axes)
        self.panel.add_fixed(5)

    def _toggle_axes(self, checked):
        # self.scene.scene.show_axes(checked)
        if(checked):
            pos, neg = create_axes_lines()
            self.scene.scene.add_geometry("axes", pos, make_material())
            self.scene.scene.add_geometry("axes1", neg, make_material())
        else:
            self.scene.scene.remove_geometry("axes")
            self.scene.scene.remove_geometry("axes1")
        
    
    def _on_add_log_button_click(self):
        logpath = self.logpath_input.text_value
        valid = validate_log_path(logpath)
        valid = True

        if(valid and self.drone_log_count < 2):
            self.drone_log_count += 1
            gui.Application.instance.post_to_main_thread(
                self.window,
                lambda: self._safe_add_drone(logpath)
            )

    def _safe_add_drone(self, logpath):
        new_drone = droneInstance(
            self.drone_log_count,
            logpath,
            self.scene
        )

        self.drone_instance.append(new_drone)

        # The panel is added to a Widget layout (e.g., self.panel), which should be a Layout widget like VGrid or VertWithMargin
        panel_widget = new_drone._get_drone_panel()

        container = gui.Vert(0.5)
        container.add_child(panel_widget)

        self.containers.append(container)

        self.panel.add_child(container)
        self.window.set_needs_layout()
        print("drone added")

    def run(self):
        gui.Application.instance.run()

class droneInstance:
    def __init__(self, _id, _logpath, _scene):
        self.id = _id
        self.logpath = _logpath
        self.scene = _scene

        self.drone_radius = 5
        self.drone_position = [0,0,0]
        self.drone_orientation = [0,0,0]
        self.log_entries = []
        self.current_index = 0

        self._make_drone()
        self._make_drone_panel()
        
        for entry in self.log_entries:
            print_log_entry(entry)

    def _make_drone(self):
        self._parse_log()
        self.drone_model = create_drone()

        self._setup_camera()

    def _setup_camera(self):
        min_bound = np.array([-1.0, -1.0, -0.5])
        max_bound = np.array([1.0, 1.0, 0.5])

        min_bound = np.array([-2.0, -2.0, -1.0])
        max_bound = np.array([2.0, 2.0, 1.0])

        # Create AABB from bounds
        bounds = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)
        self.scene.setup_camera(60, bounds, bounds.get_center())

    def _parse_log(self) -> list:
        print("parsing csv logs")
        with open(self.logpath, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                entry = LogEntry(
                    timestamp_ms=int(float(row["timestamp_ms"])),
                    accel=Vector3(
                        x=float(row["accel_x"]),
                        y=float(row["accel_y"]),
                        z=float(row["accel_z"])
                    ),
                    gyro=Vector3(
                        x=float(row["gyro_x"]),
                        y=float(row["gyro_y"]),
                        z=float(row["gyro_z"])
                    ),
                    mag=Vector3(
                        x=float(row["mag_x"]),
                        y=float(row["mag_y"]),
                        z=float(row["mag_z"])
                    ),
                    kinematics=Orientation(
                        roll=float(row["roll"]),
                        pitch=float(row["pitch"]),
                        yaw=float(row["yaw"])
                    ),
                    altitude=float(row["altitude"])
                )
                self.log_entries.append(entry)
    
    def _make_drone_panel(self):
        self.label = gui.Label(f"Drone {self.id}")
        # slider to move through log time
        self.time_slider = gui.Slider(gui.Slider.DOUBLE)
        self.time_slider.set_limits(0.0, 1.0)
        self.time_slider.double_value = 0
        self.time_slider.set_on_value_changed(self._set_timestamp)

        self.time_slider_label = gui.Label("Time Slider")

        # toggle drone visibility
        self.toggle_drone = gui.Checkbox("Show Drone")
        self.toggle_drone.set_on_checked(self._toggle_drone)

        # toggle drone trajectory
        self.toggle_trajectory = gui.Checkbox("Show Trajectory")
        self.toggle_trajectory.set_on_checked(self._toggle_trajectory)

        # Create play and pause buttons
        self.play_button = gui.Button("Play")
        self.play_button.set_on_clicked(self._play_button_pressed)
        self.pause_button = gui.Button("Pause")
        self.pause_button.set_on_clicked(self._pause_button_pressed)

        # Add the buttons side by side using a horizontal layout
        self.button_row = gui.Horiz(5)  # 5px spacing between buttons
        self.button_row.add_child(self.play_button)
        self.button_row.add_child(self.pause_button)


        self.subpanel = gui.Vert(0.5)
        self.subpanel.add_child(self.label)
        self.subpanel.add_child(self.time_slider)
        self.subpanel.add_child(self.time_slider_label)
        self.subpanel.add_child(self.toggle_drone)
        self.subpanel.add_child(self.toggle_trajectory)
        self.subpanel.add_child(self.button_row)

    def _get_drone_panel(self):
        return self.subpanel

    def _set_timestamp(self, val):
        self.current_index = min(int(val * len(self.log_entries)), 49)


    def _toggle_drone(self, checked):
        print("drone togggled")
        if checked:
            self.scene.scene.add_geometry("model", self.drone_model, make_material_v2())
        else:
            self.scene.scene.remove_geometry("model")

    def _toggle_trajectory(self, checked):
        pass

    def _play_button_pressed(self):
        pass
    def _pause_button_pressed(self):
        pass

    def _add_3d_data(self):
        # Example: Point cloud
        np_points = np.random.uniform(-1, 1, size=(1000, 3))
        pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np_points))
        pcd.paint_uniform_color([0.2, 0.8, 0.2])

        material = rendering.MaterialRecord()
        material.shader = "defaultUnlit"
        self.scene.scene.add_geometry("random_points", pcd, material)
        bounds = pcd.get_axis_aligned_bounding_box()
        self.scene.setup_camera(60, bounds, bounds.get_center())

def create_axes_lines():
    # Define axis length
        axis_len = 50

        # Points at origin and along each axis
        points = np.array([
            [0, 0, 0],            # 0: origin
            [axis_len, 0, 0],     # 1: X
            [0, axis_len, 0],     # 2: Y
            [0, 0, axis_len],     # 3: Z
        ])

        points1 = np.array([
            [0, 0, 0],            # 0: origin
            [-axis_len, 0, 0],     # 1: X
            [0, -axis_len, 0],     # 2: Y
            [0, 0, -axis_len],     # 3: Z
        ])

        # Define lines: each is a pair of point indices
        lines = [
            [0, 1],  # X
            [0, 2],  # Y
            [0, 3],  # Z
        ]

        # Custom colors: white for X, black for Y, white for Z
        colors = [
            [1, 1, 1],  # X - white
            [1, 1, 1],  # Y - black
            [1, 1, 1],  # Z - white
        ]

        # Create the LineSet
        axis_lset = o3d.geometry.LineSet()
        axis_lset.points = o3d.utility.Vector3dVector(points)
        axis_lset.lines = o3d.utility.Vector2iVector(lines)
        axis_lset.colors = o3d.utility.Vector3dVector(colors)

        # Create the LineSet
        axis1_lset = o3d.geometry.LineSet()
        axis1_lset.points = o3d.utility.Vector3dVector(points1)
        axis1_lset.lines = o3d.utility.Vector2iVector(lines)
        axis1_lset.colors = o3d.utility.Vector3dVector(colors)

        return axis_lset, axis1_lset

def make_material():
    """Create a default unlit material for rendering geometry like lines or axes."""
    mat = rendering.MaterialRecord()
    mat.shader = "unlitLine"
    return mat

def make_material_v2():
    """Create a default unlit material for rendering geometry like lines or axes."""
    material = rendering.MaterialRecord()
    material.shader = "defaultLit"  # options: "defaultLit", "defaultUnlit", "normals", etc.
    material.base_color = [0.2, 0.2, 0.8, 1.0]  # RGBA (0-1 scale)
    return material


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

def create_sphere(radius, color):
    mesh = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    mesh.paint_uniform_color(color)
    mesh.compute_vertex_normals()
    return mesh

def create_drone():
    parts = []

    # Main body (sphere)
    body = create_sphere(radius=0.1, color=[0.2, 0.2, 0.8])

    return body

if __name__ == "__main__":
    app = App3D()
    app.run()