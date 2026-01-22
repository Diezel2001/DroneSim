import sys
import drone_sim
from drone_sim import DroneSim

if __name__ == "__main__":

    args = sys.argv[1:]

    app = DroneSim(args[0])
    app.run()