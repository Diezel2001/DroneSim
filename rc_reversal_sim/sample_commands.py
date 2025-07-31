
rc_commands = []

# === RC Command Sequence ===
# Format: [throttle, pitch, roll, yaw]
#
# throttle: min=1000, max=2000
# pitch, roll, yaw: neutral=1500

rc_commands1 = [
    [1100, 1500, 1500, 1500],  # up
    [1100, 1600, 1500, 1500],  # up + forward
    [1100, 1500, 1600, 1500],  # up + right
    [1100, 1500, 1500, 1500],  # down
    [1000, 1400, 1500, 1500],  # pitch back
    [1000, 1500, 1400, 1500],  # roll left
    [1000, 1500, 1500, 1500],  # hover
]

rc_commands2 = [
    [1100, 1600, 1500, 1700],  # ascend with slight forward + left + yaw
    [1100, 1600, 1500, 1700],
    [1100, 1600, 1500, 1700],
    [1100, 1600, 1500, 1700],
    [1100, 1600, 1500, 1700],
    [1100, 1600, 1500, 1700],
    [1100, 1600, 1500, 1700],  # hover
]

rc_commands3 = [
    [1100, 1600, 1400, 1500],  # forward-right
    [1200, 1600, 1600, 1500],  # forward-left
    [1100, 1600, 1400, 1500],  # forward-right
    [1000, 1600, 1600, 1500],  # forward-left
    [1100, 1600, 1400, 1500],
    [1200, 1600, 1600, 1500],
    [1000, 1500, 1500, 1500],  # hover
]

rc_commands4 = [
    [1050, 1500, 1600, 1500],  # ascend + right strafe
    [1075, 1500, 1600, 1500],
    [1100, 1500, 1600, 1500],
    [1125, 1500, 1600, 1500],
    [1100, 1500, 1600, 1500],
    [1075, 1500, 1600, 1500],
    [1000, 1500, 1500, 1500],  # hover
]


rc_commands.append(rc_commands1)
rc_commands.append(rc_commands2)
rc_commands.append(rc_commands3)
rc_commands.append(rc_commands4)