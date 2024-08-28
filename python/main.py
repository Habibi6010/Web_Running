from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from drawing import drawing
import cv2
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def index():
    return jsonify({"message": "Saeed"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # Need to Connect to Database to check the email and password
    if email == 'test@gmail.com' and password == '123':
        return jsonify({"accsess": True})
    else:
        return jsonify({"accsess": False})


@app.route('/contact_us', methods=['POST'])
def contact_us():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    print(name, email, subject, message)
    # Need to Connect to Database to save the data
    return jsonify({"accsess": True})


# Define a directory to save the video files
VIDEO_SAVE_PATH = './received_videos/'


@app.route('/run_analysis', methods=['POST'])
def run_analysis():

    video_file = request.files.get('videoUpload')
    # get the uploaded video file
    if video_file:
        video_file.save(VIDEO_SAVE_PATH + video_file.filename)
        print('Video file saved successfully')
    else:
        print('No video file uploaded')
        return jsonify({"response": False, "message": "No video file uploaded","link":None})

    height_runner = request.form.get('height_runner')
    selectedModel = request.form.get('selectedModel')
    settings_colors = request.form.get('settings_colors')
    settings_colors = json.loads(settings_colors) if settings_colors else {}
    print(height_runner, selectedModel, settings_colors)
    # Need to Connect to Database to save the data
    text=""
    # text=running_model(height_runner, selectedModel,
    #              settings_colors,video_file.filename)
    threading.Thread(target=background_analysis, args=(height_runner, selectedModel, settings_colors, video_file.filename)).start()

    return jsonify({"response": True, "message": text,"link":ANALYZED_VIDEO_SAVE_PATH+video_file.filename})


def background_analysis(height_runner, selected_model, settings_colors, video_name):
    # Running model analysis in the background
    result_text = running_model(height_runner, selected_model, settings_colors, video_name)
    print(result_text)
    # Here you can add any additional logic such as notifying users via a webhook or other mechanisms.



# Define a directory to save the video files after analysis
ANALYZED_VIDEO_SAVE_PATH = './analyzed_videos/'
def running_model(height_runner, selectModel, settings_colors, video_name):
    drawing_object = drawing()
    cap = cv2.VideoCapture(VIDEO_SAVE_PATH+video_name)
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    
    # Define the codec and create VideoWriter object
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
    out = cv2.VideoWriter(f'{ANALYZED_VIDEO_SAVE_PATH+video_name}.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # Output file
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Run yolo model
        yolo_landmarkss,bounding_boxs = drawing_object.yolo_landmark_detection(frame)
        if len(bounding_boxs)!=0:
            w,y,x,h=bounding_boxs[0][:4]
            scale_factor = float(height_runner)/float(h-y)
        else:
            scale_factor = 0.0
        if selectModel == 'yolo':
            if len(yolo_landmarkss)>0:
                for yolo_landmarks in yolo_landmarkss:
                    if settings_colors['knee_joint_angle'][0]:
                        left_value,right_value = drawing_object.yolo_knee_joint_angle(frame, yolo_landmarks, settings_colors['knee_joint_angle'][1])
                    if settings_colors['between_thigh_angle'][0]:
                        value = drawing_object.yolo_between_thigh_angle(frame, yolo_landmarks, settings_colors['between_thigh_angle'][1])
                    if settings_colors['elbow_joint_angle'][0]:
                        left_value,right_value = drawing_object.yolo_elbow_joint_angle(frame, yolo_landmarks, settings_colors['elbow_joint_angle'][1])
                    if settings_colors['forearm_x_axis'][0]:
                        left_value,right_value = drawing_object.yolo_forearm_x_axis(frame, yolo_landmarks, settings_colors['forearm_x_axis'][1])
                    if settings_colors['shin_x_axis'][0]:
                        left_value,right_value = drawing_object.yolo_shin_x_axis(frame, yolo_landmarks, settings_colors['shin_x_axis'][1])
                    if settings_colors['thigh_x_axis'][0]:
                        left_value,right_value = drawing_object.yolo_thigh_x_axis(frame, yolo_landmarks, settings_colors['thigh_x_axis'][1])
                    if settings_colors['ear_hip_x_axis'][0]:
                        value = drawing_object.yolo_ear_hip_x_axis(frame, yolo_landmarks, settings_colors['ear_hip_x_axis'][1])
                    if settings_colors['distance_knee'][0]:
                        value = drawing_object.yolo_distance_knee(frame, yolo_landmarks, settings_colors['ear_nose_x_axis'][1],scale_factor)
                    if settings_colors['distance_wrist_hip'][0]:
                        left_value,right_value = drawing_object.yolo_distance_wrist_hip(frame, yolo_landmarks, settings_colors['distance_wrist_hip'][1],scale_factor)
                    if settings_colors['ear_nose_x_axis'][0]:
                        value = drawing_object.yolo_ear_nose_x_axis(frame, yolo_landmarks, settings_colors['ear_nose_x_axis'][1])
        
        elif selectModel == 'mediapipe':
            mediapipe_landmarks = drawing_object.mediapipe_landmark_detection(frame)
            if (len(mediapipe_landmarks)>0):
                    if(settings_colors["foot_ground_angle"][0]):
                        left_value,right_value=drawing_object.foot_ground_angle_mediapipe(frame,mediapipe_landmarks,settings_colors["foot_ground_angle"][1])

                    if(settings_colors["knee_joint_angle"][0]):
                        left_value,right_value=drawing_object.mediapipe_knee_joint_angle(frame,mediapipe_landmarks,settings_colors["knee_joint_angle"][1])

                    if(settings_colors["between_thigh_angle"][0]):
                        value=drawing_object.mediapipe_between_thigh_angle(frame,mediapipe_landmarks,settings_colors["between_thigh_angle"][1])

                    if(settings_colors["knee_toe_angle"][0]):
                        left_value,right_value=drawing_object.mediapipe_knee_toe_angle(frame,mediapipe_landmarks,settings_colors["knee_toe_angle"][1])
                        
                    if(settings_colors["elbow_joint_angle"][0]):
                        left_value,right_value=drawing_object.mediapipe_elbow_joint_angle(frame,mediapipe_landmarks,settings_colors["elbow_joint_angle"][1])
                        
                    if(settings_colors["flexion_foot"][0]):
                        left_value,right_value=drawing_object.mediapipe_flexion_foot(frame,mediapipe_landmarks,settings_colors["flexion_foot"][1])

                    if(settings_colors["forearm_x_axis"][0]):
                        left_value,right_value=drawing_object.mediapipe_forearm_x_axis(frame,mediapipe_landmarks,settings_colors["forearm_x_axis"][1])
                    
                    if(settings_colors["shin_x_axis"][0]):
                        left_value,right_value=drawing_object.mediapipe_shin_x_axis(frame,mediapipe_landmarks,settings_colors["shin_x_axis"][1])

                    if(settings_colors["thigh_x_axis"][0]):
                        left_value,right_value=drawing_object.mediapipe_thigh_x_axis(frame,mediapipe_landmarks,settings_colors["thigh_x_axis"][1])

                    if(settings_colors["ear_hip_x_axis"][0]):
                        value=drawing_object.mediapipe_ear_hip_x_axis(frame,mediapipe_landmarks,settings_colors["ear_hip_x_axis"][1])

                    if(settings_colors["distance_knee"][0]):
                        value=drawing_object.mediapipe_distance_knee(frame,mediapipe_landmarks,settings_colors["distance_knee"][1],scale_factor)

                    if(settings_colors["distance_heel_hip"][0]):
                        left_value,right_value=drawing_object.mediapipe_distance_heel_hip(frame,mediapipe_landmarks,settings_colors["distance_heel_hip"][1],scale_factor)

                    if(settings_colors["distance_wrist_hip"][0]):
                        left_value,right_value=drawing_object.mediapipe_distance_wrist_hip(frame,mediapipe_landmarks,settings_colors["distance_wrist_hip"][1],scale_factor)

                    if(settings_colors['ear_nose_x_axis'][0]):
                        value=drawing_object.mediapipe_ear_nose_x_axis(frame,mediapipe_landmarks,settings_colors['ear_nose_x_axis'][1])
                        
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    return("Analysis Done")


if __name__ == '__main__':
    app.run(debug=False)
