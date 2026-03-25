import rospy
import pandas as pd
from datetime import datetime
from mavros_msgs.msg import State
from sensor_msgs.msg import NavSatFix, Imu

class TelemetryProcessor:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('telemetry_processor_node', anonymous=True)
        
        # Data storage
        self.data_log = []
        self.current_state = "UNKNOWN"
        
        # Subscriptions for processing incoming telemetry
        rospy.Subscriber("/mavros/state", State, self.stateCB)
        rospy.Subscriber("/mavros/global_position/global", NavSatFix, self.gpsCB)
        rospy.Subscriber("/mavros/imu/data", Imu, self.imuCB)
        
        # Ensure data is saved on shutdown
        rospy.on_shutdown(self.saveData)
        rospy.loginfo("Infrastructure Node: Telemetry Logger Initialized.")

    # Callbacks for processing telemetry data
    def stateCB(self, msg):
        self.current_state = msg.mode

    # GPS callback to log position data
    def gpsCB(self, msg):
        # Processing GPS data
        entry = {
            'timestamp': datetime.now().strftime('%H:%M:%S.%f'),
            'mode': self.current_state,
            'lat': msg.latitude,
            'lon': msg.longitude,
            'alt': msg.altitude
        }
        self.data_log.append(entry)

    def imuCB(self, msg):
        #TODO: Implement orientation and acceleration logging 
        pass

    # Function for saving logged data to a CSV file on shutdown
    def saveData(self):
        rospy.loginfo("Shutting down... Exporting telemetry.")
        if self.data_log:
            df = pd.DataFrame(self.data_log)
            filename = f"flight_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            print(f"\n[✔] Logged {len(df)} telemetry points to {filename}")

if __name__ == '__main__':
    try:
        processor = TelemetryProcessor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass