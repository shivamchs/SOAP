from cache_config import cache_region as cr
import zmq
import random
import sys
import time
import asyncio
import json


port = "5520"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
time.sleep(1)


port1="5521"
socket1 = context.socket(zmq.SUB)
socket1.connect("tcp://localhost:%s"% port1)

compensate = False


def getvalue(key):
    a=cr.get(key, expiration_time=None, ignore_expiration=False)
    return a

data=(cr.backend._cache)

async def recv():
    topicfilter = "c1"
    socket1.setsockopt(zmq.SUBSCRIBE,topicfilter.encode())

    [topic,task,msg] = socket1.recv_multipart()
    #print(msg.decode())
    k=task.decode()
    print(k, "\n")
    lst=getvalue(k)
    lst["status"]="complete"
    lst["out"]=json.loads(msg.decode())
    print(data)
    cr.set(k,lst)
    return

async def call(key):
     lst=getvalue(key)
     type=lst.get("type")
     lst1=[];
     for l in lst.get("param"):
          try:
            exec(l)
          except:
            return 
     lst["param"]=lst1
     lst["status"]="in process"
     cr.set(key,lst)
     value=json.dumps(lst)
     socket.send_multipart([type.encode(),value.encode()])
     return
     



while(True):
    for key in data:
            lst=getvalue(key)
            if lst.get("status")=="pending":
                lst2=lst.get("parent")
                if(lst2):
                    for l in lst2:
                        dict2=getvalue(l)
                        if dict2.get("status")!="complete":
                            break
                    if l==lst2[-1]:
                        asyncio.run(call(key))
                else:      
                    asyncio.run(call(key))
                        
            asyncio.run(recv()) 
        
    
    
# def ready_comp_tasks():
#     for key in data:
#         lst=getvalue(key)
#         for t in lst.get("parent"):
            
#         if lst.get("parent")==[] and lst.get("status")=="pending":
#             #print(key)
#             asyncio.run(call(key))
       
        


    
        
        
while(True):
    recv()
    
