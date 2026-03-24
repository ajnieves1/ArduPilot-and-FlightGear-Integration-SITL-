import collections
if not hasattr(collections, 'MutableMapping'):
    import collections.abc
    collections.MutableMapping = collections.abc.MutableMapping
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the SITL 
print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

# Function that arms the drone and takes it to a specified altitude
def arm_and_takeoff(target_altitude):
    print("Pre arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Execute simple takeoff to 10 meters
arm_and_takeoff(10)

print("Hovering for 5 seconds...")
time.sleep(5)

print("Setting Land mode...")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()
print("Mission Complete")