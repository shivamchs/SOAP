import sys
import time

from random import randint

import zmq

def main(url=None):
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    if url is None:
        url = "tcp://localhost:5557"
    subscriber.connect(url)
    
    
    publisher=ctx.socket(zmq.PUB)
    publisher.bind("tcp://localhost:5558")

    subscription = b"%03d" % 1
    print(subscription)
    subscriber.setsockopt(zmq.SUBSCRIBE, subscription)

    while True:
        topic, data = subscriber.recv_multipart()
        print(topic)
        assert topic == subscription
        print (data)
        time.sleep(1)
        publisher.send_multipart([
                b"%03d" % 2,
                b"Off with his head!",
            ])
if _name_ == '_main_':
    main(sys.argv[1] if len(sys.argv) > 1 else None)