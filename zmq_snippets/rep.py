import zmq
import time
import requests

port = "54848"

context = zmq.Context()
socket = context.socket(zmq.REP)


socket.connect ("tcp://localhost:%s" % port)
print( "Collecting updates from server...")



port1="54846"
socket1 = context.socket(zmq.REQ)
socket1.bind("tcp://*:%s" % port1)

time.sleep(1)


while(True):
    url=socket.recv()
    res=requests.get(url)

    
    res=res.text
    socket1.send_string(res)





