# global imports
from subprocess import call
from cv.detect import run
from txrx.file_transmitter import ClientListener
from os import listdir

"""run computer vision scripts"""
run(model="cv/truck.tflite",
    camera_id=0,
    width=640,
    height=480,
    num_threads=4,
    enable_edgetpu=False,
    time_limit=10)

if len(listdir('not_sent')) > 0:
    """run wifi hotspot scripts"""
    # listener = ClientListener()
    # listener.listen_for_client()
    pass
else:
    """shutdown the pi for later"""
    # call(["shutdown", "-h", "now"])
    pass
