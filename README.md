# rtdpipeline
small mqtt pipeline project w/ rtd denver data

rtd denver provides some data in the open related to their services. the data can be found here: https://www.rtd-denver.com/business-center/open-data/gtfs-developer-guide

the data i'm working with is protobuf files that they publish for vehicle positions. i'm calculating speed for vehicles. i saw someone do this as data pipeline project in java w/ elk. i'm doing this in python w/ mqtt and nodered.

### the design:
mqtt has two topics. one for raw events and one for speed events

producer gets data every 1 min from rtd denver, parses it, publishes each vehicle entity event/object to mqtt raw topic

consumer gets vehicle id, position, and timestamp and compares against old cache and determines speed then publishes that to mqtt speed topic

nodered consumes from mqtt speed topic and plots data to a map