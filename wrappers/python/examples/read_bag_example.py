#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
import datetime
import time
from PIL import Image

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
parser.add_argument("-o", "--output", type=str, help="Path to the save frames")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    #cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer()

    output_path = str(args.output)
    print('output_path',output_path)

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()

        color_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        color_frame_image = np.asanyarray(color_frame.get_data())

        frame_timestamp = frames.get_timestamp()
        frame_tt = frame_timestamp / 1000
        frame_datetime = datetime.datetime.fromtimestamp(frame_tt)

        #print(frame_datetime)
        #im = Image.fromarray(color_frame_image)

        f_datetime = str(frame_datetime)
        f_datetime = f_datetime.replace('.','_')
        f_datetime = f_datetime.replace(' ','_')
        f_datetime = f_datetime.replace('-','')
        f_datetime = f_datetime.replace(':','')
        
        color_save_path = os.path.join(output_path,'color',f_datetime+'_color.jpeg')
        depth_save_path = os.path.join(output_path,'depth',f_datetime+'_depth.jpeg')
        print(color_save_path)
        #im.save(r'G:\JaimeMorales\Codes\openlogi\RealSense\filename.jpeg')

        cv2.imwrite(depth_save_path, depth_color_image)
        cv2.imwrite(color_save_path, color_frame_image)

        # Render image in opencv window
        #cv2.imshow("Depth Stream", depth_color_image)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            #cv2.destroyAllWindows()
            break

finally:
    pass
