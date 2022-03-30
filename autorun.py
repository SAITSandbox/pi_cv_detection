# global imports
from subprocess import call
from cv.detect import run

# run computer vision scripts
run(model="cv/truck.tflite",
    camera_id=0,
    width=640,
    height=480,
    num_threads=4,
    enable_edgetpu=False)


# run wifi hotspot scripts


# shutdown the pi for later
#call(["shutdown", "-h", "now"])
