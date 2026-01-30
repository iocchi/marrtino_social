#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ROS node for recording a video from a camera topic (Python 2, MP4 output).

Features:
- Python 2 compatible
- MP4 (H.264) output, fallback to AVI
- Corrects color channels
- Can specify video filename with -savevideo
- Can record fixed duration with -record_time
- Supports manual stop (Ctrl+C) if -record_time not set
- Can show live preview with --show
- Works with /takevideo topic for start/stop/send commands
"""

from __future__ import print_function
import os
import sys
import time
import socket
import argparse
import numpy as np
import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image

ROS_NODE_NAME = 'takevideo'
TAKEVIDEO_TOPIC = '/takevideo'
PARAM_video_folder = '%s/videofolder' % ROS_NODE_NAME
PARAM_result = '%s/videoresult' % ROS_NODE_NAME


def autoImageTopic():
    topics = rospy.get_published_topics()
    for t in topics:
        if t[1] == 'sensor_msgs/Image' and 'depth' not in t[0] and '/ir/' not in t[0] and 'image_rect' not in t[0]:
            return t[0]
    return None


class TakeVideo(object):
    def __init__(self, img_topic=None, takevideo_topic=None):
        self.bridge = CvBridge()
        self.image_received = False
        self.image = None
        self.recording = False
        self.video_writer = None
        self.frame_size = (640, 480)
        self.fps = 20.0
        self.video_file = None

        if img_topic is None:
            img_topic = autoImageTopic()

        if img_topic is None:
            rospy.logerr("Cannot find any image topic! Aborting.")
            sys.exit(0)

        rospy.loginfo("Image topic: %s" % img_topic)
        self.image_sub = rospy.Subscriber(img_topic, Image, self.image_cb)

        if takevideo_topic is not None:
            rospy.loginfo("TakeVideo topic: %s" % takevideo_topic)
            rospy.Subscriber(takevideo_topic, String, self.take_video_cb)

        self.video_folder = '.'
        if rospy.has_param(PARAM_video_folder):
            self.video_folder = rospy.get_param(PARAM_video_folder)

        rospy.loginfo("Save video folder: %s" % self.video_folder)

        self.server_ip = 'localhost'
        self.server_port = 9250
        rospy.loginfo("Default send video server: %s:%d" % (self.server_ip, self.server_port))

    def image_cb(self, data):
        try:
            # Force conversion to BGR for consistent color
            cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
            self.image_received = True
            self.image = cv_image
            if self.recording and self.video_writer is not None:
                self.video_writer.write(cv_image)
        except CvBridgeError as e:
            rospy.logerr("CvBridge error: %s" % e)

    def start_recording(self, filename=None, fps=20.0):
        if not self.image_received:
            rospy.logwarn("No image received yet. Cannot start recording.")
            return False

        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(self.video_folder, "%s_video.mp4" % timestamp)

        if not os.path.exists(self.video_folder):
            os.makedirs(self.video_folder)

        h, w, _ = self.image.shape
        self.frame_size = (w, h)
        self.fps = fps
        self.video_file = filename
        rospy.loginfo("Recording video to %s" % self.video_file)

        # Try MP4 H.264 codec
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.video_writer = cv2.VideoWriter(self.video_file, fourcc, self.fps, self.frame_size)
        if not self.video_writer.isOpened():
            rospy.logwarn("H.264 codec not available, falling back to MJPG.")
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.video_file = self.video_file.replace(".mp4", ".avi")
            self.video_writer = cv2.VideoWriter(self.video_file, fourcc, self.fps, self.frame_size)

        self.recording = True
        return True

    def stop_recording(self):
        if not self.recording:
            rospy.logwarn("Not currently recording.")
            return
        self.recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        rospy.loginfo("Stopped recording. Saved video: %s" % self.video_file)

    def send_video(self):
        if not self.video_file or not os.path.exists(self.video_file):
            rospy.logwarn("No video file to send.")
            return

        try:
            rospy.set_param(PARAM_result, '')
            sock = socket.socket()
            sock.connect((self.server_ip, self.server_port))
            rospy.loginfo("Sending video file %s to %s:%d" % (self.video_file, self.server_ip, self.server_port))

            f = open(self.video_file, 'rb')
            while True:
                data = f.read(1024)
                if not data:
                    break
                sock.sendall(data)
            f.close()
            sock.shutdown(socket.SHUT_WR)
            response = sock.recv(4096)
            response_str = response.decode('utf-8', 'ignore')
            rospy.set_param(PARAM_result, response_str)
            rospy.loginfo("Server response: %s" % response_str)
            sock.close()
        except Exception as e:
            rospy.logerr("Error sending video: %s" % str(e))
            try:
                rospy.set_param(PARAM_result, 'ERROR: Video send failed')
            except Exception:
                pass

    def take_video_cb(self, msg):
        command = msg.data.strip().split()
        rospy.loginfo("Received command: %s" % str(command))

        if len(command) == 0:
            return

        if command[0] == "record":
            if len(command) > 1 and command[1] == "start":
                filename = os.path.join(self.video_folder, "%s_video.mp4" % time.strftime("%Y%m%d-%H%M%S"))
                self.start_recording(filename)
            elif len(command) > 1 and command[1] == "stop":
                self.stop_recording()
            else:
                rospy.logwarn("Usage: 'record start' or 'record stop'")
        elif command[0] == "send":
            if len(command) >= 3:
                self.server_ip = command[1]
                self.server_port = int(command[2])
            self.send_video()

    def waitForImage(self):
        while not self.image_received and not rospy.is_shutdown():
            rospy.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-image_topic", type=str, default=None,
                        help="Image topic (default: auto detect)")
    parser.add_argument("-takevideo_topic", type=str, default=TAKEVIDEO_TOPIC,
                        help="Topic name for TakeVideo subscriber (default: %s)" % TAKEVIDEO_TOPIC)
    parser.add_argument("-record_time", type=int, default=None,
                        help="Record for N seconds (default: None)")
    parser.add_argument("-savevideo", type=str, default=None,
                        help="Save video with specific filename (e.g. myvideo.mp4)")
    parser.add_argument("--show", action="store_true",
                        help="Show camera feed during recording")

    args = parser.parse_args()
    rospy.init_node(ROS_NODE_NAME, anonymous=False)

    camera = TakeVideo(args.image_topic, args.takevideo_topic)
    camera.waitForImage()

    if args.savevideo:
        filename = os.path.join(camera.video_folder, args.savevideo)
        rospy.loginfo("Recording video to %s" % filename)
        if camera.start_recording(filename):
            if args.record_time:
                # Fixed duration recording
                t_end = time.time() + args.record_time
                while time.time() < t_end and not rospy.is_shutdown():
                    if args.show and camera.image_received:
                        cv2.imshow("Video Feed", camera.image)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    rospy.sleep(0.01)
                camera.stop_recording()
            else:
                # Manual stop
                rospy.loginfo("Press CTRL+C to stop recording manually.")
                try:
                    while not rospy.is_shutdown():
                        if args.show and camera.image_received:
                            cv2.imshow("Video Feed", camera.image)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        rospy.sleep(0.01)
                except KeyboardInterrupt:
                    pass
                camera.stop_recording()

    elif args.record_time:
        rospy.loginfo("Recording for %d seconds..." % args.record_time)
        filename = os.path.join(camera.video_folder, "%s_video.mp4" % time.strftime("%Y%m%d-%H%M%S"))
        if camera.start_recording(filename):
            t_end = time.time() + args.record_time
            while time.time() < t_end and not rospy.is_shutdown():
                if args.show and camera.image_received:
                    cv2.imshow("Video Feed", camera.image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                rospy.sleep(0.01)
            camera.stop_recording()
        rospy.loginfo("Done.")

    else:
        rospy.loginfo("Waiting for /takevideo topic commands...")
        rospy.spin()


if __name__ == '__main__':
    main()

