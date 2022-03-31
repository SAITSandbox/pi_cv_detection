# global imports
from subprocess import call
from cv.detect import run
from txrx.file_transmitter import ClientListener
from os import listdir
from time import sleep

"""run computer vision scripts"""
run(model="cv/model.tflite",
    camera_id=0,
    width=640,
    height=480,
    num_threads=4,
    enable_edgetpu=False,
    time_limit=60)

print('sleeping for 3 seconds')
sleep(1)
print('sleeping for 2 seconds')
sleep(1)
print('sleeping for 1 second')
sleep(1)

number_of_files = len(listdir('not_sent'))
if number_of_files > 0:
    """run wifi hotspot scripts"""
    print(f'{number_of_files} file(s) to send...')
    listener = ClientListener()
    listener.listen_for_client()
    # call(["shutdown", "-h", "now"])
    pass

if len(listdir('not_sent')) == 0:
    """shutdown the pi for later"""
    print('No more files to send')
    # call(["shutdown", "-h", "now"])
    pass

