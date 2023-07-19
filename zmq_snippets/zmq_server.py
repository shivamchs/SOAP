import time
import zmq
import requests

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.168.161.241:54848")


socket1 = context.socket(zmq.REP)
socket1.connect("tcp://10.168.161.241:54846")


while True:
    #  Wait for next request from client
    print(f"Received request")

    url = socket.recv()
    print(f"Received request: {url}")

    #  Do some 'work'
    time.sleep(1)
    resp=requests.get(url)
    

    #  Send reply back to client
    socket1.send_string(resp.text)