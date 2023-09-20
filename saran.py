#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import NavSatFix
import json

data = []

def vehicle_data(msg):
    longitude = msg.longitude
    latitude = msg.latitude
    data.append([longitude, latitude])

def extract_gps():
    rospy.Subscriber("/vehicle/gps", NavSatFix, callback=vehicle_data)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": data,
         },
        "properties": {
            "time": rospy.get_time()
        }
    }

    with open('maindata3.json', "w") as json_file:
        json.dump(feature, json_file, indent=2)
        rospy.loginfo("json file is created")

if __name__ == '__main__':
    try:
        rospy.init_node("gps_tracker")
        extract_gps()
        rospy.signal_shutdown("shutdownig")
    except rospy.ROSInterruptException:
        pass
