"""Main script to run the object detection routine."""
import argparse
import sys
import time
import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import datetime
import base64
import json
from tracker import *

# Initialize Tracker
tracker = EuclideanDistTracker()


def run(model: str, camera_id: int, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:

    """Continuously run inference on images acquired from the camera.
    Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.7,
        max_results=3,
        enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)

    # Continuously capture images from the camera and run inference
    output_list = []

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, 1)

        # Run object detection estimation using the model.
        detections = detector.detect(image)

        for detection in detections:
            left, top, right, bottom = detection.bounding_box
            if left < 0:
                left = 0
            if top < 0:
                top = 0
            if right < 0:
                right = 0
            if bottom < 0:
                bottom = 0
            w = 640
            h = 480
            #crop_image = image[int(left):int(w), int(top):int(h)]
            #cv2.imshow("still_image", crop_image)
            date_time = str(datetime.datetime.now())

            output_dict = {
                    "id": str(datetime.datetime.now()),
                    "timestamp": str(datetime.datetime.now()),
                # "image": base64.b64encode(image),
                    "class": str(detection.categories[0].label),
                    "confidence": str(detection.categories[0].score),
                    "lattiude": str(35.812296),
                    "longtiude": str(38.074243)
                }

            output_list.append(output_dict)

            #if (detection.categories[0].label) == "person":
                #cv2.imwrite("/home/pi/examples/lite/examples/object_detection/raspberry_pi/images/people/" + date_time + ".jpeg", crop_image)

            #if (detection.categories[0].label) == "keyboard":
                #cv2.imwrite("/home/pi/examples/lite/examples/object_detection/raspberry_pi/images/bottles/" + date_time + ".jpeg", crop_image)

            #time.sleep(2)


            # Draw keypoints and edges on input image
            image = utils.visualize(image, detections)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('object_detector', image)


        

    cap.release()
    print("Started writing JSON data into a file")
    with open("test.json", "w") as write_file:
        json.dump(output_list, write_file) # encode dict into JSON
    print("Done writing JSON data into .json file")

    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    args = parser.parse_args()

    run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
        int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
