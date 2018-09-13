"""
# coding *- utf-8
# this is the first official version
# this program help you to get label-images in labelimg form with the help of medianflow
# Instructions: change the global parameter to accept your environment and run this program.
#
#
"""
from xml_saver import XMLSever
import cv2
from math import *
import os

# global parameters
video_path = 'D:\Holy_cc\Label_demo\VID_20180612_203442'
video_name = video_path+'.mp4'
folder_name = 'VID_20180612_203442'
label_name = ["write", "write", "write", "write"]
skip_frame = 20
window_name = "label-frame"
frame_width = 1280
frame_height = 720
# end

# some variables that the program need and will be changed automatically
mouse_flag = False
save_flag = False
exit_flag = False
frame_degree = 0
frame_count = 1  # save frame count that will be used in the file name
save_count = 0  # count to skip_frame and save file
new_folder_count = 1
point1 = [-1, -1]
point2 = [-2, -2]
frame = None
tracker = cv2.MultiTracker_create()
# end


def rot_image(image, degree):
    """
    # rotate an image at an angle
    :param image:
    :param degree:
    :return:
    """
    height, width = image.shape[:2]
    # shape after rot
    height_new = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    width_new = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

    mat_rotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)

    mat_rotation[0, 2] += (width_new - width) / 2
    mat_rotation[1, 2] += (height_new - height) / 2

    r_frame = cv2.warpAffine(frame, mat_rotation, (width_new, height_new), borderValue=(255, 255, 255))
    return r_frame


def mouse_callback(event, x, y, flags, param):
    """
    # the callback function of mouse
    :param event:
    :param x:
    :param y:
    :param flags:
    :param param:
    :return:
    """
    global point1, point2
    if mouse_flag:
        frame_copy = frame.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            point1 = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(frame_copy, point1, (x, y), (0, 255, 0), 2)
            cv2.imshow(window_name, frame_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            point2 = (x, y)
            cv2.rectangle(frame_copy, point1, point2, (0, 0, 255), 2)
            cv2.imshow(window_name, frame_copy)


def key_callback(key):
    """
    # callback function of keyboard
    :param key:
    :return:
    """
    global exit_flag, mouse_flag, save_flag, tracker, point1, point2, frame_degree
    if key == 32:
        if mouse_flag is False:
            mouse_flag = True
            save_flag = False
            tracker = cv2.MultiTracker_create()
        else:
            mouse_flag = False
            save_flag = True
    elif key == ord('a'):
        if mouse_flag is True:
            bbox = (point1[0], point1[1], point2[0] - point1[0], point2[1] - point1[1])
            tracker.add(cv2.TrackerMedianFlow_create(), frame, bbox)
    elif key == ord('s'):
        mouse_flag = False
        save_flag = False
    elif key == ord('r'):
        frame_degree = (frame_degree + 90) % 360
    elif key == 27:
        exit_flag = True


if __name__ == "__main__":
    cap = cv2.VideoCapture(video_name)
    success, frame = cap.read()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)
    while True:
        try:
            os.mkdir(video_path)
            break
        except FileExistsError:
            video_path += '_%d' % new_folder_count
            new_folder_count += 1
    while success:
        key = cv2.waitKey(1) & 0xff
        key_callback(key)
        if exit_flag:
            break
        if mouse_flag is False:
            success, frame = cap.read()
            frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            frame = rot_image(frame, frame_degree)
            track_ok, boxes = tracker.update(frame)
            if save_flag:
                save_count += 1
                if save_count > skip_frame:
                    print(folder_name + "_%d.jpg" % frame_count)
                    cv2.imwrite(video_path + '/' + folder_name + "_%d.jpg" % frame_count, frame)
                    xml_saver = XMLSever(folder_name, folder_name + "_%d" % frame_count,
                                         video_path + '/' + folder_name + "_%d.jpg" % frame_count,
                                         frame_width, frame_height, 3)
                    for i in range(boxes.__len__()):
                        xml_saver.add_object(label_name[i], int(boxes[i][0]), int(boxes[i][1]),
                                             int(boxes[i][0] + boxes[i][2]), int(boxes[i][1] + boxes[i][3]))
                    xml_saver.save()
                    save_count = 0
                    frame_count += 1
            if track_ok:
                for new_box in boxes:
                    p1 = (int(new_box[0]), int(new_box[1]))
                    p2 = (int(new_box[0] + new_box[2]), int(new_box[1] + new_box[3]))
                    cv2.rectangle(frame, p1, p2, (0, 0, 255), 2)
            cv2.imshow(window_name, frame)
    cv2.destroyAllWindows()
    cap.release()

