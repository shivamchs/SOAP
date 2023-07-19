from typing import Union

from fastapi import APIRouter, FastAPI, Response
from pydantic import BaseModel, HttpUrl
import requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx



import zmq
import time
import subprocess

port="54848"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind("tcp://*:%s" % port)
time.sleep(1)

socket1 = context.socket(zmq.REP)
socket1.connect("tcp://10.168.161.241:54846")



app = FastAPI()



@app.get('/call/{flag}')
def get_data( flag: bool, callback_url: Union[HttpUrl, None] = None ):
    if flag:
        response=requests.get(callback_url)
        return response.text
    else:
        socket.send_string(callback_url)
        message = socket1.recv()
        return f"Received reply  [ {message} ]"