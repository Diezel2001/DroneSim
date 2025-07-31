from dataclasses import dataclass

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Orientation:
    roll: float
    pitch: float
    yaw: float


@dataclass(frozen=True)
class LogEntry:
    timestamp_ms: int
    accel: Vector3
    gyro: Vector3
    mag: Vector3
    kinematics: Orientation
    altitude: float
    
def print_log_entry(entry):
    print(f"{entry.timestamp_ms:.2f},{entry.accel.x:.3f},{entry.accel.y:.3f},{entry.accel.z:.3f},"
          f"{entry.mag.x:.3f},{entry.mag.y:.3f},{entry.mag.z:.3f},"
          f"{entry.gyro.x:.3f},{entry.gyro.y:.3f},{entry.gyro.z:.3f},"
          f"{entry.kinematics.pitch:.2f},{entry.kinematics.roll:.2f},{entry.kinematics.yaw:.2f},"
          f"{entry.altitude:.2f}")
    