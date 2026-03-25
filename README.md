1. Initialize venv:
    python3 -m venv drone_env
    source drone_env/bin/activate
    pip install dronekit pymavlink

2. You need 3 concurrent terminal sessions open

3. Start the ArduCopter SITL (Terminal 1)
    cd ~/path/to/ardupilot/ArduCopter
    ../build/sitl/bin/arducopter --model + --defaults ../Tools/autotest/default_params/copter.parm

4. Start MAVProxy (Terminal 2)
    source drone_env/bin/activate
    python3 -m MAVProxy.mavproxy --master=tcp:127.0.0.1:5760 --out=udp:127.0.0.1:14550 --map --console

5. Initiate navigation (Terminal 3)
    python3 params.py