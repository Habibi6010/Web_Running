from ultralytics import YOLO
import mediapipe as mp
import numpy as np
import pandas as pd
import cv2
from tools import tools


class drawing:
    global yolo_model, pose

    def __init__(self) -> None:
        # load an official YOLO model
        self.yolo_model = YOLO('yolov8l-pose.pt')
        # load and Initialize mediapipe pose class.
        mp_pose = mp.solutions.pose
        self.pose = mp_pose.Pose(
            static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def mediapipe_landmark_detection(self, frame):
        # Mediapipe detection
        person_crop_in_RGB = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        mediapipe_pose_result = self.pose.process(person_crop_in_RGB)
        if mediapipe_pose_result.pose_landmarks:
            landmarks = mediapipe_pose_result.pose_landmarks.landmark
        else:
            landmarks = 0
        if landmarks:
            # draw landmarks in frame
            mediapipe_landmarks = [
                [landmark.x, landmark.y, landmark.z,landmark.visibility] for landmark in landmarks]
        else:
            mediapipe_landmarks = []
        return mediapipe_landmarks

    def yolo_landmark_detection(self, frame):

        # YOLO Detection
        yolo_pose_result = self.yolo_model(frame)
        yolo_landmarks = yolo_pose_result[0].keypoints.data.cpu(
        ).numpy().astype(float)
        yolo_boxs = yolo_pose_result[0].boxes.data.cpu().numpy().astype(float)
        return yolo_landmarks, yolo_boxs

    def foot_ground_angle_mediapipe(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left=0
        x_degree_right=0
        if mediapipe_landmarks:
            x_degree_left = tools.calculate_angle_with_x_axis(
                mediapipe_landmarks[31], mediapipe_landmarks[29])
            cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[31][0]*w)+5, int(
                mediapipe_landmarks[31][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.line(frame, (int(mediapipe_landmarks[31][0]*w), int(mediapipe_landmarks[31][1]*h)), (int(
                mediapipe_landmarks[29][0]*w), int(mediapipe_landmarks[29][1]*h)), color, 2)

            x_degree_right = tools.calculate_angle_with_x_axis(
                mediapipe_landmarks[32], mediapipe_landmarks[30])
            cv2.putText(frame, f'{x_degree_right:.2f}',  (int(mediapipe_landmarks[32][0]*w)+5, int(
                mediapipe_landmarks[32][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.line(frame, (int(mediapipe_landmarks[32][0]*w), int(mediapipe_landmarks[32][1]*h)), (int(
                mediapipe_landmarks[30][0]*w), int(mediapipe_landmarks[30][1]*h)), color, 2)
        return x_degree_left, x_degree_right

    def mediapipe_knee_joint_angle(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle(
            mediapipe_landmarks[23], mediapipe_landmarks[25], mediapipe_landmarks[27])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[25][0]*w)+5, int(
            mediapipe_landmarks[25][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[23][0]*w), int(mediapipe_landmarks[23][1]*h)), (int(
            mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), (int(
            mediapipe_landmarks[27][0]*w), int(mediapipe_landmarks[27][1]*h)), color, 2)

        x_degree_right = tools.calculate_angle(
            mediapipe_landmarks[24], mediapipe_landmarks[26], mediapipe_landmarks[28])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(mediapipe_landmarks[26][0]*w)+5, int(
            mediapipe_landmarks[26][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[24][0]*w), int(mediapipe_landmarks[24][1]*h)), (int(
            mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), (int(
            mediapipe_landmarks[28][0]*w), int(mediapipe_landmarks[28][1]*h)), color, 2)
        return x_degree_left, x_degree_right

    def yolo_knee_joint_angle(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_angle(
            yolo_landmarks[11], yolo_landmarks[13], yolo_landmarks[15])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(yolo_landmarks[13][0])+5, int(
            yolo_landmarks[13][1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[11][0]), int(yolo_landmarks[11][1])), (int(
            yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), (int(
            yolo_landmarks[15][0]), int(yolo_landmarks[15][1])), color, 2)

        x_degree_right = tools.calculate_angle(
            yolo_landmarks[12], yolo_landmarks[14], yolo_landmarks[16])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(yolo_landmarks[14][0])+5, int(
            yolo_landmarks[14][1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[12][0]), int(yolo_landmarks[12][1])), (int(
            yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), (int(
            yolo_landmarks[16][0]), int(yolo_landmarks[16][1])), color, 2)
        return x_degree_left, x_degree_right

    def mediapipe_between_thigh_angle(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        mid_hip_mediapipe = [(mediapipe_landmarks[23][0]+mediapipe_landmarks[24][0])/2,
                             (mediapipe_landmarks[23][1] +
                              mediapipe_landmarks[24][1])/2,
                             (mediapipe_landmarks[23][2]+mediapipe_landmarks[24][2])/2]
        x_degree_left = tools.calculate_angle(
            mediapipe_landmarks[25], mid_hip_mediapipe, mediapipe_landmarks[26])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(
            mid_hip_mediapipe[0]*w)+5, int(mid_hip_mediapipe[1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), (int(
            mid_hip_mediapipe[0]*w), int(mid_hip_mediapipe[1]*h)), color, 2)
        cv2.line(frame, (int(mid_hip_mediapipe[0]*w), int(mid_hip_mediapipe[1]*h)), (int(
            mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), color, 2)
        return x_degree_left
    
    def yolo_between_thigh_angle(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        mid_hip_yolo = []
        if (yolo_landmarks[12][2] > .7 and yolo_landmarks[11][2] < .7):
            mid_hip_yolo = yolo_landmarks[12]
        elif (yolo_landmarks[12][2] < .7 and yolo_landmarks[11][2] > .7):
            mid_hip_yolo = yolo_landmarks[11]
        else:
            mid_hip_yolo = [(yolo_landmarks[12][0]+yolo_landmarks[11][0])/2,
                            (yolo_landmarks[12][1]+yolo_landmarks[11][1])/2,
                            (yolo_landmarks[12][2]+yolo_landmarks[11][2])/2]
        x_degree_left = tools.calculate_angle(
            yolo_landmarks[13], mid_hip_yolo, yolo_landmarks[14])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(
            mid_hip_yolo[0])+5, int(mid_hip_yolo[1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), (int(
            mid_hip_yolo[0]), int(mid_hip_yolo[1])), color, 2)
        cv2.line(frame, (int(mid_hip_yolo[0]), int(mid_hip_yolo[1])), (int(
            yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), color, 2)
        return x_degree_left

    def mediapipe_knee_toe_angle(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[32], mediapipe_landmarks[26])
        x_mid_line = int(
            (int(mediapipe_landmarks[32][0]*w)+int(mediapipe_landmarks[26][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[32][1]*h)+int(mediapipe_landmarks[26][1]*h))/2)
        cv2.putText(frame, f'{x_degree_left:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[32][0]*w), int(mediapipe_landmarks[32][1]*h)), (int(
            mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), color, 2)
        x_degree_right = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[31], mediapipe_landmarks[25])
        x_mid_line = int(
            (int(mediapipe_landmarks[31][0]*w)+int(mediapipe_landmarks[25][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[31][1]*h)+int(mediapipe_landmarks[25][1]*h))/2)
        cv2.putText(frame, f'{x_degree_right:.2f}',  (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[31][0]*w), int(mediapipe_landmarks[31][1]*h)), (int(
            mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), color, 2)
        return x_degree_left, x_degree_right

    def mediapipe_elbow_joint_angle(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle(
            mediapipe_landmarks[11], mediapipe_landmarks[13], mediapipe_landmarks[15])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[11][0]*w)+10, int(
            mediapipe_landmarks[11][1]*h)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[13][0]*w)+5, int(mediapipe_landmarks[13][1]*h)), (int(
            mediapipe_landmarks[15][0]*w)+5, int(mediapipe_landmarks[15][1]*h)), color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[11][0]*w)+5, int(mediapipe_landmarks[11][1]*h)), (int(
            mediapipe_landmarks[13][0]*w)+5, int(mediapipe_landmarks[13][1]*h)), color, 2)

        x_degree_right = tools.calculate_angle(
            mediapipe_landmarks[12], mediapipe_landmarks[14], mediapipe_landmarks[16])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(mediapipe_landmarks[16][0]*w)+10, int(
            mediapipe_landmarks[16][1]*h)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[14][0]*w)+5, int(mediapipe_landmarks[14][1]*h)), (int(
            mediapipe_landmarks[16][0]*w)+5, int(mediapipe_landmarks[16][1]*h)), color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[14][0]*w)+5, int(mediapipe_landmarks[14][1]*h)), (int(
            mediapipe_landmarks[12][0]*w)+5, int(mediapipe_landmarks[12][1]*h)), color, 2)
        return x_degree_left, x_degree_right

    def yolo_elbow_joint_angle(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_angle(
            yolo_landmarks[6], yolo_landmarks[8], yolo_landmarks[10])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(yolo_landmarks[10][0])+10, int(
            yolo_landmarks[10][1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[8][0])+5, int(yolo_landmarks[8][1])), (int(
            yolo_landmarks[10][0])+5, int(yolo_landmarks[10][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[8][0])+5, int(yolo_landmarks[8][1])), (int(
            yolo_landmarks[6][0])+5, int(yolo_landmarks[6][1])), color, 2)

        x_degree_right = tools.calculate_angle(
            yolo_landmarks[5], yolo_landmarks[7], yolo_landmarks[9])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(yolo_landmarks[5][0])+10, int(
            yolo_landmarks[5][1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[7][0])+5, int(yolo_landmarks[7][1])), (int(
            yolo_landmarks[9][0])+5, int(yolo_landmarks[9][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[7][0])+5, int(yolo_landmarks[7][1])), (int(
            yolo_landmarks[5][0])+5, int(yolo_landmarks[5][1])), color, 2)
        return x_degree_left, x_degree_right

    def mediapipe_forearm_x_axis(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[13], mediapipe_landmarks[15])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[13][0]*w)+5, int(
            mediapipe_landmarks[13][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[13][0]*w), int(mediapipe_landmarks[13][1]*h)), (int(
            mediapipe_landmarks[15][0]*w), int(mediapipe_landmarks[15][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[13][0]*w))-20, int(mediapipe_landmarks[13][1]*h)), ((
            int(mediapipe_landmarks[13][0]*w))+20, int(mediapipe_landmarks[13][1]*h)), color, 1)

        x_degree_right = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[14], mediapipe_landmarks[16])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(mediapipe_landmarks[14][0]*w)+5, int(
            mediapipe_landmarks[14][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[14][0]*w), int(mediapipe_landmarks[14][1]*h)), (int(
            mediapipe_landmarks[16][0]*w), int(mediapipe_landmarks[16][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[14][0]*w))-20, int(mediapipe_landmarks[14][1]*h)), ((
            int(mediapipe_landmarks[14][0]*w))+20, int(mediapipe_landmarks[14][1]*h)), color, 1)
        return x_degree_left, x_degree_right
    
    def yolo_forearm_x_axis(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_angle_with_x_axis(
            yolo_landmarks[8], yolo_landmarks[10])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(yolo_landmarks[8][0])+5, int(
            yolo_landmarks[8][1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[8][0]), int(yolo_landmarks[8][1])), (int(
            yolo_landmarks[10][0]), int(yolo_landmarks[10][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[8][0])-20, int(yolo_landmarks[8][1])), (int(
            yolo_landmarks[8][0])+20, int(yolo_landmarks[8][1])), color, 1)

        x_degree_right = tools.calculate_angle_with_x_axis(
            yolo_landmarks[7], yolo_landmarks[9])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(yolo_landmarks[7][0])+5, int(
            yolo_landmarks[7][1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[7][0]), int(yolo_landmarks[7][1])), (int(
            yolo_landmarks[9][0]), int(yolo_landmarks[9][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[7][0])-20, int(yolo_landmarks[7][1])), (int(
            yolo_landmarks[7][0])+20, int(yolo_landmarks[7][1])), color, 1)
        return x_degree_left, x_degree_right
    
    def mediapipe_flexion_foot(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle(
            mediapipe_landmarks[31], mediapipe_landmarks[29], mediapipe_landmarks[25])
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[29][0]*w)+5, int(
            mediapipe_landmarks[29][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, ((int(mediapipe_landmarks[31][0]*w)), int(mediapipe_landmarks[31][1]*h)), ((
            int(mediapipe_landmarks[29][0]*w)), int(mediapipe_landmarks[29][1]*h)), color, 1)
        cv2.line(frame, ((int(mediapipe_landmarks[29][0]*w)), int(mediapipe_landmarks[29][1]*h)), ((
            int(mediapipe_landmarks[25][0]*w)), int(mediapipe_landmarks[25][1]*h)), color, 1)

        x_degree_right = tools.calculate_angle(
            mediapipe_landmarks[32], mediapipe_landmarks[30], mediapipe_landmarks[26])
        cv2.putText(frame, f'{x_degree_right:.2f}',  (int(mediapipe_landmarks[30][0]*w)+5, int(
            mediapipe_landmarks[30][1]*h)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, ((int(mediapipe_landmarks[32][0]*w)), int(mediapipe_landmarks[32][1]*h)), ((
            int(mediapipe_landmarks[30][0]*w)), int(mediapipe_landmarks[30][1]*h)), color, 1)
        cv2.line(frame, ((int(mediapipe_landmarks[30][0]*w)), int(mediapipe_landmarks[30][1]*h)), ((
            int(mediapipe_landmarks[26][0]*w)), int(mediapipe_landmarks[26][1]*h)), color, 1)
        return x_degree_left, x_degree_right
    
    def mediapipe_shin_x_axis(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[27], mediapipe_landmarks[25])
        x_mid_line = int(
            (int(mediapipe_landmarks[27][0]*w)+int(mediapipe_landmarks[25][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[27][1]*h)+int(mediapipe_landmarks[25][1]*h))/2)
        cv2.putText(frame, f'{x_degree_left:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), (int(
            mediapipe_landmarks[27][0]*w), int(mediapipe_landmarks[27][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[27][0]*w))-30, int(mediapipe_landmarks[27][1]*h)), ((
            int(mediapipe_landmarks[27][0]*w))+30, int(mediapipe_landmarks[27][1]*h)), color, 1)

        x_degree_right = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[28], mediapipe_landmarks[26])
        x_mid_line = int(
            (int(mediapipe_landmarks[28][0]*w)+int(mediapipe_landmarks[26][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[28][1]*h)+int(mediapipe_landmarks[26][1]*h))/2)
        cv2.putText(frame, f'{x_degree_right:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), (int(
            mediapipe_landmarks[28][0]*w), int(mediapipe_landmarks[28][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[28][0]*w))-30, int(mediapipe_landmarks[28][1]*h)), ((
            int(mediapipe_landmarks[28][0]*w))+30, int(mediapipe_landmarks[28][1]*h)), color, 1)
        return x_degree_left, x_degree_right
    
    def mediapipe_thigh_x_axis(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        x_degree_left = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[26], mediapipe_landmarks[24])
        x_mid_line = int(
            (int(mediapipe_landmarks[26][0]*w)+int(mediapipe_landmarks[24][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[26][1]*h)+int(mediapipe_landmarks[24][1]*h))/2)
        cv2.putText(frame, f'{x_degree_left:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[24][0]*w), int(mediapipe_landmarks[24][1]*h)), (int(
            mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[26][0]*w))-30, int(mediapipe_landmarks[26][1]*h)), ((
            int(mediapipe_landmarks[26][0]*w))+30, int(mediapipe_landmarks[26][1]*h)), color, 1)

        x_degree_right = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[25], mediapipe_landmarks[23])
        x_mid_line = int(
            (int(mediapipe_landmarks[25][0]*w)+int(mediapipe_landmarks[23][0]*w))/2)
        y_mid_line = int(
            (int(mediapipe_landmarks[25][1]*h)+int(mediapipe_landmarks[23][1]*h))/2)
        cv2.putText(frame, f'{x_degree_right:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), (int(
            mediapipe_landmarks[23][0]*w), int(mediapipe_landmarks[23][1]*h)), color, 2)
        cv2.line(frame, ((int(mediapipe_landmarks[25][0]*w))-30, int(mediapipe_landmarks[25][1]*h)), ((
            int(mediapipe_landmarks[25][0]*w))+30, int(mediapipe_landmarks[25][1]*h)), color, 1)
        return x_degree_left, x_degree_right
    
    def yolo_shin_x_axis(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_angle_with_x_axis(
            yolo_landmarks[15], yolo_landmarks[13])
        x_mid_line = int(
            (int(yolo_landmarks[15][0])+int(yolo_landmarks[13][0]))/2)
        y_mid_line = int(
            (int(yolo_landmarks[15][1])+int(yolo_landmarks[13][1]))/2)
        cv2.putText(frame, f'{x_degree_left:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[15][0]), int(yolo_landmarks[15][1])), (int(
            yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[15][0])-20, int(yolo_landmarks[15][1])), (int(
            yolo_landmarks[15][0])+20, int(yolo_landmarks[15][1])), color, 1)

        x_degree_right = tools.calculate_angle_with_x_axis(
            yolo_landmarks[16], yolo_landmarks[14])
        x_mid_line = int(
            (int(yolo_landmarks[16][0])+int(yolo_landmarks[14][0]))/2)
        y_mid_line = int(
            (int(yolo_landmarks[16][1])+int(yolo_landmarks[14][1]))/2)
        cv2.putText(frame, f'{x_degree_right:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[16][0]), int(yolo_landmarks[16][1])), (int(
            yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[16][0])-20, int(yolo_landmarks[16][1])), (int(
            yolo_landmarks[16][0])+20, int(yolo_landmarks[16][1])), color, 1)
        return x_degree_left, x_degree_right
    
    def yolo_thigh_x_axis(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        x_degree_right = tools.calculate_angle_with_x_axis(
            yolo_landmarks[14], yolo_landmarks[12])
        x_mid_line = int(
            (int(yolo_landmarks[14][0])+int(yolo_landmarks[12][0]))/2)
        y_mid_line = int(
            (int(yolo_landmarks[14][1])+int(yolo_landmarks[12][1]))/2)
        cv2.putText(frame, f'{x_degree_right:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), (int(
            yolo_landmarks[12][0]), int(yolo_landmarks[12][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[14][0])-20, int(yolo_landmarks[14][1])), (int(
            yolo_landmarks[14][0])+20, int(yolo_landmarks[14][1])), color, 1)

        x_degree_left = tools.calculate_angle_with_x_axis(
            yolo_landmarks[13], yolo_landmarks[11])
        x_mid_line = int(
            (int(yolo_landmarks[13][0])+int(yolo_landmarks[11][0]))/2)
        y_mid_line = int(
            (int(yolo_landmarks[13][1])+int(yolo_landmarks[11][1]))/2)
        cv2.putText(frame, f'{x_degree_left:.2f}', (x_mid_line,
                    y_mid_line), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.line(frame, (int(yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), (int(
            yolo_landmarks[11][0]), int(yolo_landmarks[11][1])), color, 2)
        cv2.line(frame, (int(yolo_landmarks[13][0])-20, int(yolo_landmarks[13][1])), (int(
            yolo_landmarks[13][0])+20, int(yolo_landmarks[13][1])), color, 1)
        return x_degree_left, x_degree_right
    
    def mediapipe_ear_hip_x_axis(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        mid_hip_mediapipe = [(mediapipe_landmarks[23][0]+mediapipe_landmarks[24][0])/2,
                             (mediapipe_landmarks[23][1] +
                              mediapipe_landmarks[24][1])/2,
                             (mediapipe_landmarks[23][2]+mediapipe_landmarks[24][2])/2]
        mid_ear_mediapipe = [(mediapipe_landmarks[7][0]+mediapipe_landmarks[8][0])/2,
                             (mediapipe_landmarks[7][1] +
                              mediapipe_landmarks[8][1])/2,
                             (mediapipe_landmarks[7][2]+mediapipe_landmarks[8][2])/2]
        x_degree_left = tools.calculate_angle_with_x_axis(
            mid_hip_mediapipe, mid_ear_mediapipe)
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mid_hip_mediapipe[0]*w), int(
            mid_hip_mediapipe[1]*h)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mid_ear_mediapipe[0]*w), int(mid_ear_mediapipe[1]*h)), (int(
            mid_hip_mediapipe[0]*w), int(mid_hip_mediapipe[1]*h)), color, 2)
        cv2.line(frame, (int(mid_hip_mediapipe[0]*w)-10, int(mid_hip_mediapipe[1]*h)), (int(
            mid_hip_mediapipe[0]*w)+10, int(mid_hip_mediapipe[1]*h)), color, 1)
        return x_degree_left

    def yolo_ear_hip_x_axis(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        mid_ear_yolo = []
        if (yolo_landmarks[4][2] > .7 and yolo_landmarks[3][2] < .7):
            mid_ear_yolo = yolo_landmarks[4]
        elif (yolo_landmarks[4][2] < .7 and yolo_landmarks[3][2] > .7):
            mid_ear_yolo = yolo_landmarks[3]
        else:
            mid_ear_yolo = [(yolo_landmarks[4][0]+yolo_landmarks[3][0])/2,
                            (yolo_landmarks[4][1]+yolo_landmarks[3][1])/2,
                            (yolo_landmarks[4][2]+yolo_landmarks[3][2])/2]

        mid_hip_yolo = []
        if (yolo_landmarks[12][2] > .7 and yolo_landmarks[11][2] < .7):
            mid_hip_yolo = yolo_landmarks[12]
        elif (yolo_landmarks[12][2] < .7 and yolo_landmarks[11][2] > .7):
            mid_hip_yolo = yolo_landmarks[11]
        else:
            mid_hip_yolo = [(yolo_landmarks[12][0]+yolo_landmarks[11][0])/2,
                            (yolo_landmarks[12][1]+yolo_landmarks[11][1])/2,
                            (yolo_landmarks[12][2]+yolo_landmarks[11][2])/2]
        
        x_degree_left = tools.calculate_angle_with_x_axis(
                mid_hip_yolo, mid_ear_yolo)
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mid_hip_yolo[0]), int(
            mid_hip_yolo[1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mid_ear_yolo[0]), int(mid_ear_yolo[1])), (int(
            mid_hip_yolo[0]), int(mid_hip_yolo[1])), color, 2)
        cv2.line(frame, (int(mid_hip_yolo[0])-10, int(mid_hip_yolo[1])),
                 (int(mid_hip_yolo[0])+10, int(mid_hip_yolo[1])), color, 1)
        return x_degree_left

    def mediapipe_distance_knee(self, frame, mediapipe_landmarks, color_tkinter, scale_factor):
        h, w, _ = frame.shape
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_distance_mediapipe(
            mediapipe_landmarks[25], mediapipe_landmarks[26], w, h) * scale_factor
        cv2.putText(frame, f'Distance between Knees: {x_degree_left:.2f} m',  (
            10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_left:.2f} m',  (int(mediapipe_landmarks[26][0]*w)+10, int(
            mediapipe_landmarks[26][1]*h)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mediapipe_landmarks[25][0]*w), int(mediapipe_landmarks[25][1]*h)), (int(
            mediapipe_landmarks[26][0]*w), int(mediapipe_landmarks[26][1]*h)), color, 2)
        return x_degree_left

    def yolo_distance_knee(self, frame, yolo_landmarks, color_tkinter, scale_factor):
        color = color_tkinter[::-1]
        x_degree_left = tools.calculate_distance_yolo(
            yolo_landmarks[14], yolo_landmarks[13]) * scale_factor
        cv2.putText(frame, f'Distance between Knees: {x_degree_left:.2f} m',  (
            10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_left:.2f} m',  (int(
            yolo_landmarks[14][0])+10, int(yolo_landmarks[14][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(yolo_landmarks[14][0]), int(yolo_landmarks[14][1])), (int(
            yolo_landmarks[13][0]), int(yolo_landmarks[13][1])), color, 2)
        return x_degree_left

    def mediapipe_distance_heel_hip(self, frame, mediapipe_landmarks, color_tkinter, scale_factor):
        h, w, _ = frame.shape
        color = color_tkinter[::-1]
        mid_hip_mediapipe = [(mediapipe_landmarks[23][0]+mediapipe_landmarks[24][0])/2,
                             (mediapipe_landmarks[23][1] +
                              mediapipe_landmarks[24][1])/2,
                             (mediapipe_landmarks[23][2]+mediapipe_landmarks[24][2])/2]
        cv2.line(frame, (int(mid_hip_mediapipe[0]*w)-25, int(mid_hip_mediapipe[1]*h)), (int(
            mid_hip_mediapipe[0]*w)+25, int(mid_hip_mediapipe[1]*h)), color, 2)
        x_degree_left = tools.calculate_distance_mediapipe(
            mediapipe_landmarks[29], mid_hip_mediapipe, w, h) * scale_factor
        cv2.putText(frame, f'Distance Mid_Hip and Left_Heel: {x_degree_left:.2f} m', (
            10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_left:.2f} m', (int(mediapipe_landmarks[29][0]*w)+10, int(
            mediapipe_landmarks[29][1]*h)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        x_degree_right = tools.calculate_distance_mediapipe(
            mediapipe_landmarks[30], mid_hip_mediapipe, w, h) * scale_factor
        cv2.putText(frame, f'Distance Mid_Hip and Right_Heel: {x_degree_right:.2f} m',  (
            10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_right:.2f} m',  (int(mediapipe_landmarks[30][0]*w)+10, int(
            mediapipe_landmarks[30][1]*h)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return x_degree_left, x_degree_right

    def mediapipe_distance_wrist_hip(self, frame, mediapipe_landmarks, color_tkinter, scale_factor):
        h, w, _ = frame.shape
        color = color_tkinter[::-1]
        mid_hip_mediapipe = [(mediapipe_landmarks[23][0]+mediapipe_landmarks[24][0])/2,
                             (mediapipe_landmarks[23][1] +
                              mediapipe_landmarks[24][1])/2,
                             (mediapipe_landmarks[23][2]+mediapipe_landmarks[24][2])/2]
        x_degree_left = tools.calculate_distance_mediapipe(
            mediapipe_landmarks[15], mid_hip_mediapipe, w, h)*scale_factor
        cv2.putText(frame, f'Distance Left_Wrist and Mid_Hip: {x_degree_left:.2f} m',  (
            10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_left:.2f} m',  (int(mediapipe_landmarks[15][0]*w)+10, int(
            mediapipe_landmarks[15][1]*h)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        x_degree_right = tools.calculate_distance_mediapipe(
            mediapipe_landmarks[16], mid_hip_mediapipe, w, h)*scale_factor
        cv2.putText(frame, f'Distance Right_Wrist and Mid_Hip: {x_degree_right:.2f} m',  (
            10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_right:.2f} m',  (int(mediapipe_landmarks[16][0]*w)+10, int(
            mediapipe_landmarks[16][1]*h)+35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mediapipe_landmarks[15][0]*w), int(mediapipe_landmarks[15][1]*h)), (int(
            mid_hip_mediapipe[0]*w), int(mid_hip_mediapipe[1]*h)), color, 1)
        cv2.line(frame, (int(mediapipe_landmarks[16][0]*w), int(mediapipe_landmarks[16][1]*h)), (int(
            mid_hip_mediapipe[0]*w), int(mid_hip_mediapipe[1]*h)), color, 1)
        return x_degree_left, x_degree_right

    def yolo_distance_wrist_hip(self, frame, yolo_landmarks, color_tkinter, scale_factor):
        color = color_tkinter[::-1]
        mid_hip_yolo = []
        if (yolo_landmarks[12][2] > .7 and yolo_landmarks[11][2] < .7):
            mid_hip_yolo = yolo_landmarks[12]
        elif (yolo_landmarks[12][2] < .7 and yolo_landmarks[11][2] > .7):
            mid_hip_yolo = yolo_landmarks[11]
        else:
            mid_hip_yolo = [(yolo_landmarks[12][0]+yolo_landmarks[11][0])/2,
                            (yolo_landmarks[12][1]+yolo_landmarks[11][1])/2,
                            (yolo_landmarks[12][2]+yolo_landmarks[11][2])/2]

        x_degree_left = tools.calculate_distance_yolo(
            yolo_landmarks[9], mid_hip_yolo)*scale_factor
        cv2.putText(frame, f'Distance Left_Wrist and Mid_Hip: {x_degree_left:.2f} m',  (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_left:.2f} m',  (int(yolo_landmarks[9][0])+10, int(yolo_landmarks[9][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        x_degree_right = tools.calculate_distance_yolo(yolo_landmarks[10], mid_hip_yolo)*scale_factor
        cv2.putText(frame, f'Distance Right_Wrist and Mid_Hip: {x_degree_right:.2f} m',  (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f'{x_degree_right:.2f} m',  (int(
            yolo_landmarks[10][0])+10, int(yolo_landmarks[10][1])+35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(yolo_landmarks[9][0]), int(yolo_landmarks[9][1])), (int(
            mid_hip_yolo[0]), int(mid_hip_yolo[1])), color, 1)
        cv2.line(frame, (int(yolo_landmarks[10][0]), int(yolo_landmarks[10][1])), (int(
            mid_hip_yolo[0]), int(mid_hip_yolo[1])), color, 1)
        return x_degree_left, x_degree_right

    def yolo_ear_nose_x_axis(self, frame, yolo_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        mid_ear_yolo = []
        if (yolo_landmarks[4][2] > .7 and yolo_landmarks[3][2] < .7):
            mid_ear_yolo = yolo_landmarks[4]
        elif (yolo_landmarks[4][2] < .7 and yolo_landmarks[3][2] > .7):
            mid_ear_yolo = yolo_landmarks[3]
        else:
            mid_ear_yolo = [(yolo_landmarks[4][0]+yolo_landmarks[3][0])/2,
                            (yolo_landmarks[4][1]+yolo_landmarks[3][1])/2,
                            (yolo_landmarks[4][2]+yolo_landmarks[3][2])/2]
        
        x_degree_left = tools.calculate_angle_with_x_axis(
                yolo_landmarks[0], mid_ear_yolo)
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(yolo_landmarks[0][0]), int(
            yolo_landmarks[0][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mid_ear_yolo[0]), int(mid_ear_yolo[1])), (int(
            yolo_landmarks[0][0]), int(yolo_landmarks[0][1])), color, 2)
        return x_degree_left

    def mediapipe_ear_nose_x_axis(self, frame, mediapipe_landmarks, color_tkinter):
        color = color_tkinter[::-1]
        h, w, _ = frame.shape
        mid_ear_mediapipe = [(mediapipe_landmarks[7][0]+mediapipe_landmarks[8][0])/2,
                             (mediapipe_landmarks[7][1] +
                              mediapipe_landmarks[8][1])/2,
                             (mediapipe_landmarks[7][2]+mediapipe_landmarks[8][2])/2]
        x_degree_left = tools.calculate_angle_with_x_axis(
            mediapipe_landmarks[0], mid_ear_mediapipe)
        cv2.putText(frame, f'{x_degree_left:.2f}',  (int(mediapipe_landmarks[0][0]*w), int(
            mediapipe_landmarks[0][1]*h)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(frame, (int(mid_ear_mediapipe[0]*w), int(mid_ear_mediapipe[1]*h)), (int(
            mediapipe_landmarks[0][0]*w), int(mediapipe_landmarks[0][1]*h)), color, 2)

        return x_degree_left