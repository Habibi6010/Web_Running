import pandas as pd
from tools import tools

class Analysis_Landmarks:
    def __init__(self) -> None:
        pass

    def mediapipe_toe_off(landmarks, width, height, scale_factor):
        # Extract the coordinates of the landmarks
        pose_landmarks = [
            [int((lmk[0])*width), int((lmk[1])*height), round(lmk[2], 3)] for lmk in landmarks]
        dic_toe_off = {}
        dic_toe_off['hip_right'] = pose_landmarks[24]
        dic_toe_off['hip_left'] = pose_landmarks[23]
        dic_toe_off['knee_right'] = pose_landmarks[26]
        dic_toe_off['knee_left'] = pose_landmarks[25]
        dic_toe_off['ankle_right'] = pose_landmarks[28]
        dic_toe_off['ankle_left'] = pose_landmarks[27]
        dic_toe_off['heel_right'] = pose_landmarks[30]
        dic_toe_off['heel_left'] = pose_landmarks[29]
        dic_toe_off['toe_right'] = pose_landmarks[32]
        dic_toe_off['toe_left'] = pose_landmarks[31]
        # Calculate the features
        dic_toe_off['angle_right_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_right'], dic_toe_off['knee_right'], dic_toe_off['ankle_right']))
        dic_toe_off['angle_left_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_left'], dic_toe_off['knee_left'], dic_toe_off['ankle_left']))
        dic_toe_off['distance_right_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_right'], dic_toe_off['ankle_right']), 2)*scale_factor
        dic_toe_off['distance_left_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_left'], dic_toe_off['ankle_left']), 2)*scale_factor
        dic_toe_off['angle_right_toe_heel_x'] = int(tools.calculate_angle_with_x_axis(
            dic_toe_off['toe_right'], dic_toe_off['heel_right']))
        dic_toe_off['angle_left_toe_heel_x'] = int(tools.calculate_angle_with_x_axis(
            dic_toe_off['toe_left'], dic_toe_off['heel_left']))
        return dic_toe_off

    def yolo_toe_off(landmarks, scale_factor):
        dic_toe_off = {}
        dic_toe_off['hip_right'] = [
            int(landmarks[12][0]), int(landmarks[12][1])]
        dic_toe_off['hip_left'] = [
            int(landmarks[11][0]), int(landmarks[11][1])]
        dic_toe_off['knee_right'] = [
            int(landmarks[14][0]), int(landmarks[14][1])]
        dic_toe_off['knee_left'] = [
            int(landmarks[13][0]), int(landmarks[13][1])]
        dic_toe_off['ankle_right'] = [
            int(landmarks[16][0]), int(landmarks[16][1])]
        dic_toe_off['ankle_left'] = [
            int(landmarks[15][0]), int(landmarks[15][1])]
        # Calculate the features
        dic_toe_off['angle_right_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_right'], dic_toe_off['knee_right'], dic_toe_off['ankle_right']))
        dic_toe_off['angle_left_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_left'], dic_toe_off['knee_left'], dic_toe_off['ankle_left']))
        dic_toe_off['distance_right_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_right'], dic_toe_off['ankle_right']), 2)*scale_factor
        dic_toe_off['distance_left_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_left'], dic_toe_off['ankle_left']), 2)*scale_factor
        return dic_toe_off

    def mediapipe_full_flight(landmarks, width, height, scale_factor):
        pose_landmarks = [[int((lmk[0])*width), int((lmk[1])*height),
                           round(lmk[2], 3), lmk[3]] for lmk in landmarks]
        dic_toe_off = {}
        dic_toe_off['hip_right'] = [pose_landmarks[24][0],
                                    pose_landmarks[24][1], pose_landmarks[24][2]]
        dic_toe_off['hip_left'] = [pose_landmarks[23][0],
                                   pose_landmarks[23][1], pose_landmarks[23][2]]
        dic_toe_off['knee_right'] = [pose_landmarks[26][0],
                                     pose_landmarks[26][1], pose_landmarks[26][2]]
        dic_toe_off['knee_left'] = [pose_landmarks[25][0],
                                    pose_landmarks[25][1], pose_landmarks[25][2]]
        dic_toe_off['ear_right'] = [pose_landmarks[8][0],
                                    pose_landmarks[8][1], pose_landmarks[8][2]]
        dic_toe_off['ear_left'] = [pose_landmarks[7][0],
                                   pose_landmarks[7][1], pose_landmarks[7][2]]
        # Calculate the features
        if pose_landmarks[24][3] > 0.5 and pose_landmarks[23][3] > 0.5:
            dic_toe_off['hip_mid'] = [int((pose_landmarks[24][0]+pose_landmarks[23][0])/2), int(
                (pose_landmarks[24][1]+pose_landmarks[23][1])/2)]
        elif pose_landmarks[24][3] > 0.5:
            dic_toe_off['hip_mid'] = [
                pose_landmarks[24][0], pose_landmarks[24][1]]
        elif pose_landmarks[23][3] > 0.5:
            dic_toe_off['hip_mid'] = [
                pose_landmarks[23][0], pose_landmarks[23][1]]
        if pose_landmarks[7][3] > 0.5 and pose_landmarks[8][3] > 0.5:
            dic_toe_off['ear_mid'] = [int((pose_landmarks[7][0]+pose_landmarks[8][0])/2), int(
                (pose_landmarks[7][1]+pose_landmarks[8][1])/2)]
        elif pose_landmarks[7][3] > 0.5:
            dic_toe_off['ear_mid'] = [
                pose_landmarks[7][0], pose_landmarks[7][1]]
        elif pose_landmarks[8][3] > 0.5:
            dic_toe_off['ear_mid'] = [
                pose_landmarks[8][0], pose_landmarks[8][1]]
        dic_toe_off['distance_knee'] = round(tools.calculate_distance_yolo(
            pose_landmarks[26], pose_landmarks[25]), 2)*scale_factor
        return dic_toe_off

    def yolo_full_flight(landmarks, scale_factor):
        dic_toe_off = {}
        dic_toe_off['hip_right'] = [
            int(landmarks[12][0]), int(landmarks[12][1])]
        dic_toe_off['hip_left'] = [
            int(landmarks[11][0]), int(landmarks[11][1])]
        dic_toe_off['knee_right'] = [
            int(landmarks[14][0]), int(landmarks[14][1])]
        dic_toe_off['knee_left'] = [
            int(landmarks[13][0]), int(landmarks[13][1])]
        dic_toe_off['ear_right'] = [int(landmarks[4][0]), int(landmarks[4][1])]
        dic_toe_off['ear_left'] = [int(landmarks[3][0]), int(landmarks[3][1])]
        # Calculate the features
        if landmarks[12][2] > 0.5 and landmarks[11][2] > 0.5:
            dic_toe_off['hip_mid'] = [int(
                (landmarks[12][0]+landmarks[11][0])/2), int((landmarks[12][1]+landmarks[11][1])/2)]
        elif landmarks[12][2] > 0.5:
            dic_toe_off['hip_mid'] = dic_toe_off['hip_right']
        elif landmarks[11][2] > 0.5:
            dic_toe_off['hip_mid'] = dic_toe_off['hip_left']
        if landmarks[3][2] > 0.5 and landmarks[4][2] > 0.5:
            dic_toe_off['ear_mid'] = [int(
                (landmarks[3][0]+landmarks[4][0])/2), int((landmarks[3][1]+landmarks[4][1])/2)]
        elif landmarks[3][2] > 0.5:
            dic_toe_off['ear_mid'] = dic_toe_off['ear_left']
        elif landmarks[4][2] > 0.5:
            dic_toe_off['ear_mid'] = dic_toe_off['ear_right']
        dic_toe_off['distance_knee'] = round(tools.calculate_distance_yolo(
            dic_toe_off['knee_right'], dic_toe_off['knee_left']), 2)*scale_factor
        return dic_toe_off

    def mediapipe_touch_down(landmarks, width, height):
        # Extract the coordinates of the landmarks
        pose_landmarks = [[int((lmk[0])*width), int((lmk[1])*height),
                           round(lmk[2], 3), round(lmk[3], 3)] for lmk in landmarks]
        dic_touch_down = {}
        dic_touch_down['hip_right'] = pose_landmarks[24]
        dic_touch_down['hip_left'] = pose_landmarks[23]
        dic_touch_down['knee_right'] = pose_landmarks[26]
        dic_touch_down['knee_left'] = pose_landmarks[25]
        dic_touch_down['ankle_right'] = pose_landmarks[28]
        dic_touch_down['ankle_left'] = pose_landmarks[27]
        dic_touch_down['heel_right'] = pose_landmarks[30]
        dic_touch_down['heel_left'] = pose_landmarks[29]
        dic_touch_down['toe_right'] = pose_landmarks[32]
        dic_touch_down['toe_left'] = pose_landmarks[31]
        dic_touch_down['shoulder_right'] = pose_landmarks[12]
        dic_touch_down['shoulder_left'] = pose_landmarks[11]
        dic_touch_down['elbow_right'] = pose_landmarks[14]
        dic_touch_down['elbow_left'] = pose_landmarks[13]
        dic_touch_down['wrist_right'] = pose_landmarks[16]
        dic_touch_down['wrist_left'] = pose_landmarks[15]
        # Calculate the features
        dic_touch_down['angle_right_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_touch_down['hip_right'], dic_touch_down['knee_right'], dic_touch_down['ankle_right']))
        dic_touch_down['angle_left_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_touch_down['hip_left'], dic_touch_down['knee_left'], dic_touch_down['ankle_left']))
        dic_touch_down['angle_right_toe_heel_x'] = int(tools.calculate_angle_with_x_axis(
            dic_touch_down['toe_right'], dic_touch_down['heel_right']))
        dic_touch_down['angle_left_toe_heel_x'] = int(tools.calculate_angle_with_x_axis(
            dic_touch_down['toe_left'], dic_touch_down['heel_left']))
        dic_touch_down['angle_right_shoulder_elbow_wrist'] = int(tools.calculate_angle(
            dic_touch_down['shoulder_right'], dic_touch_down['elbow_right'], dic_touch_down['wrist_right']))
        dic_touch_down['angle_left_shoulder_elbow_wrist'] = int(tools.calculate_angle(
            dic_touch_down['shoulder_left'], dic_touch_down['elbow_left'], dic_touch_down['wrist_left']))
        return dic_touch_down

    def yolo_touch_down(landmarks):
        # Extract the coordinates of the landmarks
        dic_toe_off = {}
        dic_toe_off['hip_right'] = [
            int(landmarks[12][0]), int(landmarks[12][1])]
        dic_toe_off['hip_left'] = [
            int(landmarks[11][0]), int(landmarks[11][1])]
        dic_toe_off['knee_right'] = [
            int(landmarks[14][0]), int(landmarks[14][1])]
        dic_toe_off['knee_left'] = [
            int(landmarks[13][0]), int(landmarks[13][1])]
        dic_toe_off['ankle_right'] = [
            int(landmarks[16][0]), int(landmarks[16][1])]
        dic_toe_off['ankle_left'] = [
            int(landmarks[15][0]), int(landmarks[15][1])]
        dic_toe_off['shoulder_right'] = [
            int(landmarks[6][0]), int(landmarks[6][1])]
        dic_toe_off['shoulder_left'] = [
            int(landmarks[5][0]), int(landmarks[5][1])]
        dic_toe_off['elbow_right'] = [
            int(landmarks[8][0]), int(landmarks[8][1])]
        dic_toe_off['elbow_left'] = [
            int(landmarks[7][0]), int(landmarks[7][1])]
        dic_toe_off['wrist_right'] = [
            int(landmarks[10][0]), int(landmarks[10][1])]
        dic_toe_off['wrist_left'] = [
            int(landmarks[9][0]), int(landmarks[9][1])]
        # Calculate the features
        dic_toe_off['angle_right_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_right'], dic_toe_off['knee_right'], dic_toe_off['ankle_right']))
        dic_toe_off['angle_left_hip_knee_ankle'] = int(tools.calculate_angle(
            dic_toe_off['hip_left'], dic_toe_off['knee_left'], dic_toe_off['ankle_left']))
        dic_toe_off['angle_right_shoulder_elbow_wrist'] = int(tools.calculate_angle(
            dic_toe_off['shoulder_right'], dic_toe_off['elbow_right'], dic_toe_off['wrist_right']))
        dic_toe_off['angle_left_shoulder_elbow_wrist'] = int(tools.calculate_angle(
            dic_toe_off['shoulder_left'], dic_toe_off['elbow_left'], dic_toe_off['wrist_left']))
        return dic_toe_off

    def mediapipe_full_support(landmarks, width, height, scale_factor):
        # Extract the coordinates of the landmarks
        pose_landmarks = [
            [int((lmk[0])*width), int((lmk[1])*height), round(lmk[2], 3)] for lmk in landmarks]
        dic_full_support = {}
        dic_full_support['hip_right'] = pose_landmarks[24]
        dic_full_support['hip_left'] = pose_landmarks[23]
        dic_full_support['knee_right'] = pose_landmarks[26]
        dic_full_support['knee_left'] = pose_landmarks[25]
        dic_full_support['ankle_right'] = pose_landmarks[28]
        dic_full_support['ankle_left'] = pose_landmarks[27]

        # Calculate the features
        dic_full_support['distance_right_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_full_support['hip_right'], dic_full_support['ankle_right']), 2)*scale_factor
        dic_full_support['distance_left_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_full_support['hip_left'], dic_full_support['ankle_left']), 2)*scale_factor
        dic_full_support['distance_knee_together'] = int(tools.calculate_distance_yolo(
            dic_full_support['knee_right'], dic_full_support['knee_left']))*scale_factor
        return dic_full_support

    def yolo_full_support(landmarks, scale_factor):
        dic_toe_off = {}
        dic_toe_off['hip_right'] = [
            int(landmarks[12][0]), int(landmarks[12][1])]
        dic_toe_off['hip_left'] = [
            int(landmarks[11][0]), int(landmarks[11][1])]
        dic_toe_off['knee_right'] = [
            int(landmarks[14][0]), int(landmarks[14][1])]
        dic_toe_off['knee_left'] = [
            int(landmarks[13][0]), int(landmarks[13][1])]
        dic_toe_off['ankle_right'] = [
            int(landmarks[16][0]), int(landmarks[16][1])]
        dic_toe_off['ankle_left'] = [
            int(landmarks[15][0]), int(landmarks[15][1])]
        # Calculate the features
        dic_toe_off['distance_right_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_right'], dic_toe_off['ankle_right']), 2)*scale_factor
        dic_toe_off['distance_left_hip_ankle'] = round(tools.calculate_distance_yolo(
            dic_toe_off['hip_left'], dic_toe_off['ankle_left']), 2)*scale_factor
        dic_toe_off['distance_knees_together'] = int(tools.calculate_distance_yolo(
            dic_toe_off['knee_right'], dic_toe_off['knee_left']))*scale_factor
        return dic_toe_off
