#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import GPSRAW
import json
data=[]

def gps_callback(msg, data):
    latitude = msg.latitude
    longitude = msg.longitude
    data.append([longitude, latitude])

def gps_callback_mavros1(msg1, data):
    latitude1 = msg1.lat
    longitude1 = msg1.lon
    data.append([longitude1, latitude1])

def gps_callback_mavros2(msg2, data):
    latitude2 = msg2.lat
    longitude2 = msg2.lon
    data.append([longitude2, latitude2])

def extract_gps_data():
    #data = []
    # data1 = []
    # data2 = []

    rospy.Subscriber('/vehicle/gps', NavSatFix, callback=lambda msg: gps_callback(msg, data))
    rospy.Subscriber('/mavros/gpsstatus/gps1/raw', GPSRAW, callback=lambda msg1: gps_callback_mavros1(msg1, data))
    rospy.Subscriber('/mavros/gpsstatus/gps2/raw', GPSRAW, callback=lambda msg2: gps_callback_mavros2(msg2, data))

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()

        if data:
            features = []

            #if data:
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
            features.append(feature)

            # if data1:
            #     feature1 = {
            #         "type": "Feature",
            #         "geometry": {
            #             "type": "LineString",
            #             "coordinates": data1,
            #         },
            #         "properties": {
            #             "time": rospy.get_time()
            #         }
            #     }
            #     features.append(feature1)

            # if data2:
            #     feature2 = {
            #         "type": "Feature",
            #         "geometry": {
            #             "type": "LineString",
            #             "coordinates": data2,
            #         },
            #         "properties": {
            #             "time": rospy.get_time()
            #         }
            #     }
            #     features.append(feature2)

        with open('maindata.json', "w") as json_file:
                json.dump(features, json_file, indent=2)
                rospy.loginfo_once("JSON created successfully")
                json_file.close()

if __name__ == '__main__':
    try:
        rospy.init_node('gps_data_extractor')
        extract_gps_data()
        rospy.signal_shutdown("Shutting down")
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
