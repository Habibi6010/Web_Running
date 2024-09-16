from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import json
from drawing import drawing
import cv2
import threading
import os
import pandas as pd
from Analysis_Landmarks_Pusture import Analysis_Landmarks
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/video_list', methods=['POST'])
def video_list():
    username = request.json.get('username')
    print(username)
    video_list = []
    for file in os.listdir(VIDEO_SAVE_PATH):
        if file.startswith(username):
            video_list.append(file)
    return jsonify({"video_list": video_list})


@app.route('/')
def index():
    return jsonify({"message": "Mostafa's API"})


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
    username = request.form.get('username')
    height_runner = request.form.get('height_runner')
    selectedModel = request.form.get('selectedModel')
    settings_colors = request.form.get('settings_colors')
    settings_colors = json.loads(settings_colors) if settings_colors else {}
    print(height_runner, selectedModel, settings_colors)
    # get the uploaded video file
    if video_file:
        video_file.save(f'{VIDEO_SAVE_PATH}{username}_{video_file.filename}')
        print('Video file saved successfully')
    else:
        print('No video file uploaded')
        return jsonify({"response": False, "message": "No video file uploaded","link":None})
    # Need to Connect to Database to save the data
    text=""
    text,response,write_file_name=running_model(height_runner, selectedModel,
                 settings_colors,video_file.filename,username)
    print(text)
    print(response)
    print("file: "+os.path.abspath(write_file_name)+".mp4")
 
    csvaddress = write_file_name.rsplit('/',1)[0]+"/all_data.csv"
    print(f'csv file: {csvaddress}')
    # threading.Thread(target=background_analysis, args=(height_runner, selectedModel, settings_colors, video_file.filename,username)).start()
    return jsonify({"response": response, "message": text,"link":os.path.abspath(write_file_name)+".mp4","csvaddress":csvaddress})


def background_analysis(height_runner, selected_model, settings_colors, video_name,username):
    # Running model analysis in the background
    result_text,response = running_model(height_runner, selected_model, settings_colors, video_name,username)
    print(result_text)
    print(response)
    # Here you can add any additional logic such as notifying users via a webhook or other mechanisms.



# Define a directory to save the video files after analysis
ANALYZED_VIDEO_SAVE_PATH = 'video/'
def running_model(height_runner, selectModel, settings_colors, video_name,username):
    drawing_object = drawing()
    cap = cv2.VideoCapture(f'{VIDEO_SAVE_PATH}{username}_{video_name}')
    print(VIDEO_SAVE_PATH+video_name)
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return("Error: Could not open video.",False,"")
    try:
        
        # Define the codec and create VideoWriter object
        counter=0
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
        write_folder_name = f'{ANALYZED_VIDEO_SAVE_PATH}{username}_{selectModel}_{video_name.split(".")[0]}_{counter}'
        while os.path.exists(f'{write_folder_name}'):
            counter+=1
            write_folder_name = f'{ANALYZED_VIDEO_SAVE_PATH}{username}_{selectModel}_{video_name.split(".")[0]}_{counter}'
        
        # create new folder for save analyzed video
        os.makedirs(write_folder_name)
        write_file_name = write_folder_name.split("/")[1]
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(f'{write_folder_name}/{write_file_name}.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),
                            (width,height))  # Output file
        df_toe_off = pd.DataFrame()
        df_full_flight = pd.DataFrame()
        df_touch_down = pd.DataFrame()
        df_full_support = pd.DataFrame()
        df_all_data = pd.DataFrame()
        frame_number=0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_number+=1
            dic_all_data = {}
            # Run yolo model
            yolo_landmarkss,bounding_boxs = drawing_object.yolo_landmark_detection(frame)
            if len(bounding_boxs)!=0:
                w,y,x,h=bounding_boxs[0][:4]
                scale_factor = float(height_runner)/float(h-y)
            else:
                scale_factor = 0.0
            if selectModel == 'yolo':
                    for yolo_landmarks in yolo_landmarkss:
                        if len(yolo_landmarks)>0:
                            if settings_colors['knee_joint_angle'][0]:
                                left_value,right_value = drawing_object.yolo_knee_joint_angle(frame, yolo_landmarks, settings_colors['knee_joint_angle'][1])
                                dic_all_data['Angle of knee (shin-thigh) joint.'] = [int(left_value),int(right_value)]
                            if settings_colors['between_thigh_angle'][0]:
                                value = drawing_object.yolo_between_thigh_angle(frame, yolo_landmarks, settings_colors['between_thigh_angle'][1])
                                dic_all_data['Angle between thighs.'] = int(value)
                            if settings_colors['elbow_joint_angle'][0]:
                                left_value,right_value = drawing_object.yolo_elbow_joint_angle(frame, yolo_landmarks, settings_colors['elbow_joint_angle'][1])
                                dic_all_data['Angle of elbow joint.']= [int(left_value),int(right_value)]
                            if settings_colors['forearm_x_axis'][0]:
                                left_value,right_value = drawing_object.yolo_forearm_x_axis(frame, yolo_landmarks, settings_colors['forearm_x_axis'][1])
                                dic_all_data['Angle of forearm with x-axis.'] = [int(left_value),int(right_value)]
                            if settings_colors['shin_x_axis'][0]:
                                left_value,right_value = drawing_object.yolo_shin_x_axis(frame, yolo_landmarks, settings_colors['shin_x_axis'][1])
                                dic_all_data['Angle of shin with x-axis.'] = [int(left_value),int(right_value)]
                            if settings_colors['thigh_x_axis'][0]:
                                left_value,right_value = drawing_object.yolo_thigh_x_axis(frame, yolo_landmarks, settings_colors['thigh_x_axis'][1])
                                dic_all_data['Angle of thigh with x-axis.'] = [int(left_value),int(right_value)]
                            if settings_colors['ear_hip_x_axis'][0]:
                                value = drawing_object.yolo_ear_hip_x_axis(frame, yolo_landmarks, settings_colors['ear_hip_x_axis'][1])
                                dic_all_data['Angle of ear-hip line with the x-axis.']=int(value)
                            if settings_colors['distance_knee'][0]:
                                value = drawing_object.yolo_distance_knee(frame, yolo_landmarks, settings_colors['ear_nose_x_axis'][1],scale_factor)
                                dic_all_data['Distance between knees.'] = round(value,3)
                            if settings_colors['distance_wrist_hip'][0]:
                                left_value,right_value = drawing_object.yolo_distance_wrist_hip(frame, yolo_landmarks, settings_colors['distance_wrist_hip'][1],scale_factor)
                                dic_all_data['Distance of hip to wrist.']=[round(left_value,3),round(right_value,3)]
                            if settings_colors['ear_nose_x_axis'][0]:
                                value = drawing_object.yolo_ear_nose_x_axis(frame, yolo_landmarks, settings_colors['ear_nose_x_axis'][1])
                                dic_all_data['Angle of ear-nose line with the x-axis.'] = int(value)
                            # Extract Features for posture analysis
                            dic_all_data['frame'] = frame_number
                            df_temp=pd.DataFrame([dic_all_data])
                            df_all_data = pd.concat([df_all_data,df_temp],ignore_index=True)
                            
                            dic={}
                            dic = Analysis_Landmarks.yolo_toe_off(yolo_landmarks,scale_factor)
                            dic['frame'] = frame_number
                            df_temp = pd.DataFrame([dic])
                            df_toe_off = pd.concat([df_toe_off,df_temp],ignore_index=True)
                            dic={}
                            dic = Analysis_Landmarks.yolo_full_flight(yolo_landmarks,scale_factor)
                            dic['frame'] = frame_number
                            df_temp = pd.DataFrame([dic])
                            df_full_flight = pd.concat([df_full_flight,df_temp],ignore_index=True)
                            dic={}
                            dic=Analysis_Landmarks.yolo_touch_down(yolo_landmarks)
                            dic['frame']=frame_number
                            df_temp = pd.DataFrame([dic])
                            df_touch_down = pd.concat([df_touch_down,df_temp],ignore_index=True)
                            dic={}
                            dic=Analysis_Landmarks.yolo_full_support(yolo_landmarks,scale_factor)
                            dic['frame']=frame_number
                            df_temp = pd.DataFrame([dic])
                            df_full_support = pd.concat([df_full_support,df_temp],ignore_index=True)
            elif selectModel == 'mediapipe':
                mediapipe_landmarks = drawing_object.mediapipe_landmark_detection(frame)
                if (len(mediapipe_landmarks)>0):
                        if(settings_colors["foot_ground_angle"][0]):
                            left_value,right_value=drawing_object.foot_ground_angle_mediapipe(frame,mediapipe_landmarks,settings_colors["foot_ground_angle"][1])
                            dic_all_data['Angle of foot with ground.'] = [int(left_value),int(right_value)]
                        if(settings_colors["knee_joint_angle"][0]):
                            left_value,right_value=drawing_object.mediapipe_knee_joint_angle(frame,mediapipe_landmarks,settings_colors["knee_joint_angle"][1])
                            dic_all_data['Angle of knee (shin-thigh) joint.'] = [int(left_value),int(right_value)]
                        if(settings_colors["between_thigh_angle"][0]):
                            value=drawing_object.mediapipe_between_thigh_angle(frame,mediapipe_landmarks,settings_colors["between_thigh_angle"][1])
                            dic_all_data['Angle between thighs.'] = int(value)
                        if(settings_colors["knee_toe_angle"][0]):
                            left_value,right_value=drawing_object.mediapipe_knee_toe_angle(frame,mediapipe_landmarks,settings_colors["knee_toe_angle"][1])
                            dic_all_data['Angle of foot line with x-axis.']=[int(left_value),int(right_value)]
                        if(settings_colors["elbow_joint_angle"][0]):
                            left_value,right_value=drawing_object.mediapipe_elbow_joint_angle(frame,mediapipe_landmarks,settings_colors["elbow_joint_angle"][1])
                            dic_all_data['Angle of elbow joint.']=[int(left_value),int(right_value)]
                        if(settings_colors["flexion_foot"][0]):
                            left_value,right_value=drawing_object.mediapipe_flexion_foot(frame,mediapipe_landmarks,settings_colors["flexion_foot"][1])
                            dic_all_data['Angle of ankle (toe-heel-shin) joint.']=[int(left_value),int(right_value)]
                        if(settings_colors["forearm_x_axis"][0]):
                            left_value,right_value=drawing_object.mediapipe_forearm_x_axis(frame,mediapipe_landmarks,settings_colors["forearm_x_axis"][1])
                            dic_all_data['Angle of forearm with x-axis.']=[int(left_value),int(right_value)]
                        if(settings_colors["shin_x_axis"][0]):
                            left_value,right_value=drawing_object.mediapipe_shin_x_axis(frame,mediapipe_landmarks,settings_colors["shin_x_axis"][1])
                            dic_all_data['Angle of shin with x-axis.']=[int(left_value),int(right_value)]
                        if(settings_colors["thigh_x_axis"][0]):
                            left_value,right_value=drawing_object.mediapipe_thigh_x_axis(frame,mediapipe_landmarks,settings_colors["thigh_x_axis"][1])
                            dic_all_data['Angle of thigh with x-axis.']=[int(left_value),int(right_value)]
                        if(settings_colors["ear_hip_x_axis"][0]):
                            value=drawing_object.mediapipe_ear_hip_x_axis(frame,mediapipe_landmarks,settings_colors["ear_hip_x_axis"][1])
                            dic_all_data['Angle of ear-hip line with the x-axis.'] = int(value)
                        if(settings_colors["distance_knee"][0]):
                            value=drawing_object.mediapipe_distance_knee(frame,mediapipe_landmarks,settings_colors["distance_knee"][1],scale_factor)
                            dic_all_data['Distance between knees.'] = round(value,3)
                        if(settings_colors["distance_heel_hip"][0]):
                            left_value,right_value=drawing_object.mediapipe_distance_heel_hip(frame,mediapipe_landmarks,settings_colors["distance_heel_hip"][1],scale_factor)
                            dic_all_data['Distance of hip to heel.']=[round(left_value,3),round(right_value,3)]
                        if(settings_colors["distance_wrist_hip"][0]):
                            left_value,right_value=drawing_object.mediapipe_distance_wrist_hip(frame,mediapipe_landmarks,settings_colors["distance_wrist_hip"][1],scale_factor)
                            dic_all_data['Distance of hip to wrist.']=[round(left_value,3),round(right_value,3)]
                        if(settings_colors['ear_nose_x_axis'][0]):
                            value=drawing_object.mediapipe_ear_nose_x_axis(frame,mediapipe_landmarks,settings_colors['ear_nose_x_axis'][1])
                            dic_all_data['Angle of ear-nose line with the x-axis.'] = int(value)
                        # Extract Features for posture analysis
                        dic_all_data['frame'] = frame_number
                        df_temp=pd.DataFrame([dic_all_data])
                        df_all_data = pd.concat([df_all_data,df_temp],ignore_index=True)
                        
                        dic={}
                        dic=Analysis_Landmarks.mediapipe_toe_off(mediapipe_landmarks,width,height,scale_factor)
                        dic['frame']=frame_number
                        df = pd.DataFrame([dic])
                        df_toe_off = pd.concat([df_toe_off,df],ignore_index=True)
                        dic={}
                        dic = Analysis_Landmarks.mediapipe_full_flight(mediapipe_landmarks,width,height,scale_factor)
                        dic['frame']=frame_number
                        df = pd.DataFrame([dic])
                        df_full_flight = pd.concat([df_full_flight,df],ignore_index=True)
                        dic={}
                        dic = Analysis_Landmarks.mediapipe_touch_down(mediapipe_landmarks,width,height)
                        dic['frame']=frame_number
                        df = pd.DataFrame([dic])
                        df_touch_down = pd.concat([df_touch_down,df],ignore_index=True)
                        dic={}
                        dic = Analysis_Landmarks.mediapipe_full_support(mediapipe_landmarks,width,height,scale_factor)
                        dic['frame']=frame_number
                        df = pd.DataFrame([dic])
                        df_full_support = pd.concat([df_full_support,df],ignore_index=True)
            out.write(frame)
            df_toe_off.to_csv(f'{write_folder_name}/toe_off.csv',index=False)
            df_full_support.to_csv(f'{write_folder_name}/full_support.csv',index=False)
            df_full_flight.to_csv(f'{write_folder_name}/full_flight.csv',index=False)
            df_touch_down.to_csv(f'{write_folder_name}/touch_down.csv',index=False)
            df_all_data.to_csv(f'{write_folder_name}/all_data.csv',index=False)
            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cap.release()
        out.release()
        return("Analysis Done",True,f'{write_folder_name}/{write_file_name}')
    except Exception as e:
        print(f"Error: {e}")
        return(f"Error: {e}",False,"")

if __name__ == '__main__':
    app.run(debug=False)
