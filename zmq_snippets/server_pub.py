import sys
import time

from random import randint

import zmq

def main(url=None):
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5558")
    if url:
        publisher.bind(url)
    else:
        publisher.bind("tcp://*:5557")
    # Ensure subscriber connection has time to complete
    time.sleep(1)
    
    subscription = b"%03d" % 2
    
    subscriber.setsockopt(zmq.SUBSCRIBE, subscription)

    # Send out all 1,000 topic messages
    for i in range(10):
        #print (b"%03d" % 1)
        publisher.send_multipart([
            b"%03d" % 1,
            b"Save Roger",
        ])

    while True:
        # Send one random update per second
        try:
            time.sleep(1)
            publisher.send_multipart([
                b"%03d" % 2,
                b"Off with his head!",
            ])
            topic, data = subscriber.recv_multipart()
            #print(topic)
            assert topic == subscription
            print (data)
        except KeyboardInterrupt:
            print ("interrupted")
            break

if _name_ == '_main_':
    main(sys.argv[1] if len(sys.argv) > 1 else None)