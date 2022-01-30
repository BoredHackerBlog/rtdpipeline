import json
import paho.mqtt.client as mqtt
from datetime import datetime
import diskcache as dc
from geopy import distance

topic = "rtddenver/raw"
topic2 = "rtddenver/speed"

broker = "mosquitto"

cache = dc.Cache('tmp')

def calc_speed(old_pos, old_ts, new_pos, new_ts):
    miles = distance.distance(old_pos, new_pos).miles
    old_dt = datetime.fromtimestamp(old_ts)
    new_dt = datetime.fromtimestamp(new_ts)
    diff_time = new_dt - old_dt
    diff_hours = diff_time.seconds / 60 / 60
    speed = miles / diff_hours
    return speed

def on_message(client, userdata, message):
    json_str = message.payload.decode()
    vehicle_data = json.loads(json_str)['vehicle']
    vehicle_label = vehicle_data['vehicle']['label']
    new_pos = (vehicle_data['position']['latitude'], vehicle_data['position']['longitude'])
    new_ts = vehicle_data['timestamp']

    try:
        if cache[vehicle_label]:
            old_pos = cache[vehicle_label][0]
            old_ts = cache[vehicle_label][1]

            cur_speed = calc_speed(old_pos, old_ts, new_pos, new_ts)

            vehicle_speed = {"vehicle_label": vehicle_label, "position": {"lat": new_pos[0], "long": new_pos[1]}, "mph":cur_speed}

            client.publish(topic2, json.dumps(vehicle_speed))
    except:
        cache[vehicle_label] = new_pos, new_ts

client = mqtt.Client("consumer")
client.on_message = on_message

client.connect(broker, keepalive=120)

client.subscribe(topic)

client.loop_forever()
