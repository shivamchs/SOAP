import sys
import zmq
import json
import requests
import time

port = "5520"

context = zmq.Context()
socket = context.socket(zmq.SUB)


socket.connect ("tcp://localhost:%s" % port)
print( "Collecting updates from server...")

port1="5521"
socket1 = context.socket(zmq.PUB)
socket1.bind("tcp://*:%s" % port1)

time.sleep(1)


while(True):
    topicfilter = "c1"

    socket.setsockopt(zmq.SUBSCRIBE,topicfilter.encode())

    # socket.setsockopt(zmq.SUBSCRIBE, b'c1')
    [topic,msg] = socket.recv_multipart()

    dict=json.loads(msg.decode())
    url=dict["url"]

    task=dict["id"]

    res=requests.get(url)

    
    res=res.json()
    #print((res.json()))
    print(task)




    socket1.send_multipart([b'c1',task.encode(),json.dumps(res).encode()])

