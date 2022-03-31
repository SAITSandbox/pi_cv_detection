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
    time_limit=20)

number_of_files = len(listdir('not_sent'))
if number_of_files > 0:
    """run wifi hotspot scripts"""
    listener = ClientListener()
    listener.listen_for_client()
    # call(["shutdown", "-h", "now"])
    pass

if len(listdir('not_sent')) == 0:
    """shutdown the pi for later"""
    print('No more files to send')
    # call(["shutdown", "-h", "now"])
    pass
