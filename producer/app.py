import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import json
import paho.mqtt.client as mqtt

cron = "* * * * *"

url = "https://www.rtd-denver.com/files/gtfs-rt/VehiclePosition.pb"

topic = "rtddenver/raw"

broker = "mosquitto"

client = mqtt.Client("producer")

client.connect(broker, keepalive=120)

def scan():
    r = requests.get(url)
    if r.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(r.content)
        vehicles = protobuf_to_dict(feed)['entity']
        for vehicle in vehicles:
            client.publish(topic, json.dumps(vehicle))

scheduler = BlockingScheduler()
scheduler.add_job(scan, CronTrigger.from_crontab(cron, 'UTC'))
print(scheduler.print_jobs())
scheduler.start()

