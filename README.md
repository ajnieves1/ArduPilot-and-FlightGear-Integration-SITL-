The pipeline consists of four decoupled layers:

    Flight Controller (SITL): Runs the ArduCopter firmware simulating Navio2 hardware.

    Communication Gateway (MAVProxy): Multiplexes MAVLink packets and forwards streams via UDP.

    Abstraction Layer (MAVROS): Translates MAVLink protocol into ROS Topics.

    Data Node: A Python based ROS node that ingests telemetry and serializes data for analysis.

# How to run on your system:

** NOTE ** 
You also need to clone the official ardupilot repo: https://github.com/Ardupilot/ardupilot

1. Clone this repo
2. run "pixi install" 
3. run "pixi run -e noetic setup-datasets"
4. Open terminal 1 and run: cd "ardupilot/ArduCopter" & "../build/sitl/bin/arducopter --model + --defaults ../Tools/autotest/default_params/copter.parm"
5. Open terminal 2 and run: "python3 -m MAVProxy.mavproxy --master=tcp:127.0.0.1:5760 --out=udp:127.0.0.1:14550 --map --console"
6. Open terminal 3 and run: "pixi run -e noetic roslaunch mavros apm.launch fcu_url:=udp://127.0.0.1:14550@"
7. Open terminal 4 and run: pixi run -e noetic python TelemetryProcessor.py


# PIXI
# ---------------

Install pixi: 
    curl -fsSL https://pixi.sh/install.sh | bash

Install RoboStack using Pixi:
    pixi init robostack
    cd robostack

Open 'pixi.toml' and paste the following: 
    [workspace]
name = "robostack"
description = "Development environment for RoboStack ROS packages"
channels = ["https://prefix.dev/conda-forge"]
platforms = ["linux-64"]



[target.unix.activation]
# For activation scripts, we use bash for Unix-like systems
scripts = ["install/setup.bash"]
env = { GEOGRAPHICLIB_DATA = "/home/andrewnieves/Other/codingprojects/robostack/datasets" }

# To build you can use - `pixi run -e <ros distro> build <Any other temporary args>`

[feature.build.target.unix.tasks]
build = "colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DPython_FIND_VIRTUALENV=ONLY -DPython3_FIND_VIRTUALENV=ONLY"

# Dependencies used by all environments
[dependencies]
python = "*"
# Build tools
compilers = "*"
cmake = "*"
pkg-config = "*"
make = "*"
ninja = "*"
# ROS specific tools
rosdep = "*"
colcon-common-extensions = "*"

[target.linux.dependencies]
libgl-devel = "*"

# Define all the different ROS environments
# Each environment corresponds to a different ROS distribution
# and can be activated using the `pixi run/shell -e <environment>` command.
[environments]
noetic = { features = ["noetic", "build"] }
humble = { features = ["humble", "build"] }
jazzy = { features = ["jazzy", "build"] }
kilted = { features = ["kilted", "build"] }

### ROS Noetic ####
[feature.noetic]
channels = ["https://prefix.dev/robostack-noetic"]

[feature.noetic.dependencies]
ros-noetic-desktop = "*"
ros-noetic-mavros = "*"          
ros-noetic-mavros-extras = "*"   
catkin_tools = "*"

[feature.noetic.tasks]
setup-gps = "wget -qO- https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh | bash"
bridge = "roslaunch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760"
monitor = "python telemetryNode.py" 
start-sim = { depends-on = ["bridge", "monitor"] }

### ROS Humble ####
[feature.humble]
channels = ["https://prefix.dev/robostack-humble"]

[feature.humble.dependencies]
ros-humble-desktop = "*"

### ROS Jazzy ####
[feature.jazzy]
channels = ["https://prefix.dev/robostack-jazzy"]

[feature.jazzy.dependencies]
ros-jazzy-desktop = "*"

### ROS Kilted ####
[feature.kilted]
channels = ["https://prefix.dev/robostack-kilted"]

[feature.kilted.dependencies]
ros-kilted-desktop = "*"

# Save and exit pixi.toml
    pixi install

# You can start an environment with the desired robostack distribution below:

# ROS noetic
pixi
 shell -e noetic

# ROS humble
pixi
 shell -e humble

# ROS jazzy
pixi
 shell -e jazzy

# ROS kilted
pixi
 shell -e kilted