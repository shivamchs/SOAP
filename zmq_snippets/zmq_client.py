import zmq
import subprocess

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.168.161.241:54840")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending request {request} …")
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")