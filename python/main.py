from flask import Flask, jsonify, request, render_template,send_from_directory,send_file
import json
from flask_cors import CORS
from drawing import drawing
import cv2
import threading
import os
import pandas as pd
import urllib.parse
from Analysis_Landmarks_Pusture import Analysis_Landmarks
from supabase import create_client, Client
import datetime
import requests
from tools import tools
import math
# import shutil
import subprocess
from RankClustering import RankClustering
from RankClustering import ART2
import re
import time

##### Main Variable for  Address of server and video save path
# Define a directory to save the video files when user uploads
VIDEO_SAVE_PATH = 'received_videos/'
# Define a directory to save the analyzed video files
ANALYZED_VIDEO_SAVE_PATH = 'analyzed_video_file/'
# Define a directory for temporary save videos
TEMP_VIDEO_SAVE_PATH = 'temp_video_file/'
# Define ffmpeg path 
# windows example
# ffmpeg_path = r"C:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
# linux example
ffmpeg_path = "ffmpeg"
# Server fetch address
# fetch_address = "3.150.57.26"
# fetch_address = "127.0.0.1"
fetch_address = "aims-technologies.com"

# supabase api infroamtion
SUPABASE_URL = "https://rokmmhmgoothqrqbppqo.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJva21taG1nb290aHFycWJwcHFvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE5ODgxNzksImV4cCI6MjA2NzU2NDE3OX0.UlXUhvfSih-cw-QtN6F0looCsvCAnRum352B0xdCLH0"




# Create a supabase api connection and clinet

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__,static_folder='static',template_folder='templates')
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

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/videolog')
def porfile():
    return render_template('VideoLog.html')

@app.route('/rankinglog')
def rankinglog():
    return render_template('RankingLog.html')

@app.route('/profile')
def profile():
    return render_template('Profile.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    response = supabase.table("user").select("*").eq("email", email).execute()
    if len(response.data) > 0:
        if response.data[0]['password'] == password and response.data[0]['is_active']:
            response = supabase.table("user").update({"last_login": str(datetime.datetime.now())}).eq("email", email).execute()
            if len(response.data) > 0:
                print("Last login time updated successfully.")
                return jsonify({"accsess": True,'username':response.data[0]['full_name'],'useremail':response.data[0]['email']})
            else:
                print("Failed to update last login time.")
                return jsonify({"accsess": False})
        else:
            print("Incorrect password.")
            return jsonify({"accsess": False})
    else:
        print("Email not found.")
        return jsonify({"accsess": False})


@app.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.json
    email = data.get('email')
    response = supabase.table("user").select("*").eq("email", email).execute()
    if len(response.data) > 0:
        new_password = tools.generate_strong_password(length=12)
        if tools.send_forget_password_email(email, new_password):
            response = supabase.table("user").update({"password": new_password}).eq("email", email).execute()
            if len(response.data) > 0:
                return jsonify({"accsess": True,'message':'Email sent successfully. Please check your inbox.'})
            else:
                return jsonify({"accsess": False,'message':'Failed to update password. Please try again later.'})
        else:
            return jsonify({"accsess": False,'message':'Failed to send email. Please try again later.'})
    else:
        return jsonify({"accsess": False,'message':'Email not found. Please check your email address.'})

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

page_data_dic={}
@app.route('/run_analysis', methods=['POST'])
def run_analysis():
    # get data from the request
    video_file = request.files.get('videoUpload')
    userEmail = request.form.get('userEmail')
    runnerID = request.form.get('runnerID')
    selectedModel = request.form.get('selectedModel')

    # Create Recived Video Folder
    if not os.path.exists(VIDEO_SAVE_PATH):
        os.makedirs(VIDEO_SAVE_PATH)
        print(f"Folder created: {VIDEO_SAVE_PATH}")
    else:
        print(f"Folder already exists: {VIDEO_SAVE_PATH}")
    
    # Create User Analyzed Video Folder
    user_folder = f"{VIDEO_SAVE_PATH}{userEmail}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        print(f"Folder created: {user_folder}")
    else:
        print(f"Folder already exists: {user_folder}")

    # get the uploaded video file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # YYYYMMDDHHMMSS
    # video_address = f'{VIDEO_SAVE_PATH}{username}/{timestamp}_{runnerName}_{runnerGender}'
    video_address = f'{VIDEO_SAVE_PATH}{userEmail}/{timestamp}_{video_file.filename}'
    if video_file:
        video_file.save(video_address)
        # print('Video file saved successfully')
        print(f"video file address: {video_address}")
    else:
        print('No video file uploaded')
        return jsonify({"response": False, "message": "No video file uploaded"})
    
    # threading.Thread(target=background_analysis, args=(selectedModel,video_address)).start()
    df=run_model_get_landmarks(selectedModel, video_address)
    name_without_ext = os.path.splitext(video_address)[0]  # 'test@gmail.com_test_video'
    output_csv = name_without_ext + '_landmarks.pkl'
    # df.to_csv(output_csv, index=False)
    df.to_pickle(output_csv)
    print(f"Saved landmarks for each frame to {output_csv}")
    # Get user information from database
    response_user = supabase.table("user").select("*").eq("email", userEmail).execute()
    if len(response_user.data) > 0:
        response_upload_video = supabase.table("upload_video").insert({
            "user_id": response_user.data[0]['user_id'],
            "video_name": video_file.filename,
            "video_path": video_address,
            "model_used": selectedModel,
            "runner_id": runnerID,
            "landmark_path": output_csv,
            "upload_time": str(datetime.datetime.now())
        }).execute()
    else:
        return jsonify({"response": False, "message": "User email not found in database"})
    if len(response_upload_video.data) == 0:
        return jsonify({"response": False, "message": "Failed to log video upload in database"})
    else:
        upload_time = response_upload_video.data[0]['upload_time']
        upload_time = datetime.datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = upload_time.strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({"response": True,"message":" Video is being analyzed in the background",
                        "video_name":video_file.filename,
                        "video_id":response_upload_video.data[0]['video_id'],
                        "upload_date":formatted_time})

def run_model_get_landmarks(selected_model, video_address):   
    cap = cv2.VideoCapture(video_address)
    drawing_object = drawing()
    frame_landmarks = []
    frame_number = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        landmarks = None
        if selected_model == 'yolo':
            yolo_landmarks, _ = drawing_object.yolo_landmark_detection(frame)
            if len(yolo_landmarks) > 0:
                # If multiple people, take the first
                landmarks = yolo_landmarks[0]
        elif selected_model == 'mediapipe':
            mediapipe_landmarks = drawing_object.mediapipe_landmark_detection(frame)
            if mediapipe_landmarks and len(mediapipe_landmarks) > 0:
                landmarks = mediapipe_landmarks
        # Store landmarks or None
        frame_landmarks.append({
            'frame': frame_number,
            'landmarks': landmarks if landmarks is not None else None
        })
    cap.release()
    # Save to DataFrame 
    df = pd.DataFrame(frame_landmarks)
    return df

@app.route('/download_csv/<path:filepath>', methods=['GET'])
def download_csv_file(filepath):
    video_path=os.path.dirname(filepath)
    video_filename = os.path.basename(filepath)
    print(f"Serving CSV from {video_path} / {video_filename}")
    return send_from_directory(video_path, video_filename, as_attachment=True)
    # Decode the filename as Flask encodes URLs.
    # decoded_filename = urllib.parse.unquote(filename)
    # print(f"Download file: {os.path.abspath(ANALYZED_VIDEO_SAVE_PATH)}/{decoded_filename}")
    # return send_from_directory(os.path.abspath(ANALYZED_VIDEO_SAVE_PATH)+"/"+decoded_filename, "all_data.csv")

@app.route('/download_video/<path:filepath>', methods=['GET'])
def download_video_file(filepath):
    video_path=os.path.dirname(filepath)
    video_filename = os.path.basename(filepath)
    print(f"Serving video from {video_path} / {video_filename}")
    return send_from_directory(video_path, video_filename, as_attachment=True)
    # decoded_foldername = urllib.parse.unquote(foldername)  # KEEP @ character
    # abs_dir = os.path.abspath(os.path.join(ANALYZED_VIDEO_SAVE_PATH, decoded_foldername))

    # video_filename = "video_output.mp4"
    # video_file_path = os.path.join(abs_dir, video_filename)

    # if not os.path.exists(video_file_path):
    #     return f"File not found: {video_file_path}", 404

    # print(f"Serving video from {video_file_path}")
    # return send_from_directory(abs_dir, video_filename, as_attachment=True)


@app.route('/video/<path:filename>')
def video(filename):
    # video_dir = os.path.join(app.root_path, 'static', 'videos')
    print(f"Serving video:{filename}")
    return send_file(filename, mimetype='video/mp4')
    # return send_from_directory(filename)


@app.route('/draw_analysis', methods=['POST'])
def draw_analysis():
    data = request.json
    video_id = data.get('video_id')
    userEmail = data.get('userEmail')
    setting_colors = data.get('settings_colors')
    runner_height = height_to_cm(data.get('runner_height'))

    # Get video information from database
    response_video = supabase.table("upload_video").select("*").eq("video_id", video_id).execute()
    if len(response_video.data) == 0:
        return jsonify({"response": False, "message": "Video ID not found in database"})
    video_info = response_video.data[0]
    # Create Analyzed Video Folder
    if not os.path.exists(ANALYZED_VIDEO_SAVE_PATH):
        os.makedirs(ANALYZED_VIDEO_SAVE_PATH)
        print(f"Folder created: {ANALYZED_VIDEO_SAVE_PATH}")
    else:
        print(f"Folder already exists: {ANALYZED_VIDEO_SAVE_PATH}")
    # Create User Analyzed Video Folder
    user_folder = f"{ANALYZED_VIDEO_SAVE_PATH}{userEmail}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        print(f"Folder created: {user_folder}")
    else:
        print(f"Folder already exists: {user_folder}")

    message,response,write_folder_name,input_video_name= drawing_on_video(setting_colors,userEmail,video_info,runner_height)
    # Save the analyzed video path to database
    if response:
        response_update = supabase.table("analysis_video").insert({
            "video_id": video_id,
            "analysis_video_path": write_folder_name + f'/{input_video_name}_annotated_video.mp4',
            "analysis_csv_path": write_folder_name + f'/{input_video_name}_all_data.csv',
            "analysis_setting": json.dumps(setting_colors),
            "analysis_time": str(datetime.datetime.now())
        }).execute()
        if len(response_update.data) == 0:
            print("Failed to update analyzed video path in database")
            return jsonify({"response": False, "message": "Failed to update analyzed video path in database"})

    output_video_address = write_folder_name + f'/{input_video_name}_annotated_video.mp4'
    print(f"Output video address URL: {output_video_address}")
    output_video_csv = write_folder_name + f'/{input_video_name}_all_data.csv'
    print(f"Output video csv address URL: {output_video_csv}")

    return jsonify({"response": response, "message": message, "videoaddress": output_video_address, "csvaddress": output_video_csv})

def drawing_on_video(settings_colors,userEmail,video_info,runner_height):
    drawing_object = drawing()
    username = userEmail
    timestamp = datetime.datetime.strptime(video_info['upload_time'], "%Y-%m-%dT%H:%M:%S.%f")
    timestamp = timestamp.strftime("%Y%m%d%H%M%S") # YYYYMMDDHHMMSS
    input_video_name = video_info['video_name']
    input_video_name = input_video_name.split('.')[0]
    selectModel = video_info['model_used']
    settings_colors = settings_colors
    height_runner = runner_height

    video_file_address = video_info['video_path']
    csv_file_address = video_info['landmark_path']

    print(f"Video file address in drawing: {video_file_address}")
    print(f"CSV File address in drawing: {csv_file_address}")
    df_landmarks = pd.read_pickle(csv_file_address)
    cap = cv2.VideoCapture(video_file_address)
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return("Error: Could not open video.",False,"")
    try:
        
        # Define the codec and create VideoWriter object
        counter=0
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for mp4
        write_folder_name = f'{ANALYZED_VIDEO_SAVE_PATH}{username}/{timestamp}_{input_video_name}_{counter}'
        while os.path.exists(f'{write_folder_name}'):
            counter+=1
            write_folder_name = f'{ANALYZED_VIDEO_SAVE_PATH}{username}/{timestamp}_{input_video_name}_{counter}'
        
        # create new folder for save analyzed video
        os.makedirs(write_folder_name)
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(f'{write_folder_name}/{input_video_name}_video_output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),
                            (width,height))  # Output file
        
        df_posture_features = pd.DataFrame()
        df_all_data = pd.DataFrame()
        frame_number=0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_number+=1
            dic_all_data = {}
            scale_factor = 0.0
            if selectModel == 'yolo':
                    yolo_landmarkss,bounding_boxs = drawing_object.yolo_landmark_detection(frame)
                    if len(bounding_boxs)!=0:
                        w,y,x,h = bounding_boxs[0][:4]
                        scale_factor = float(height_runner)/float(h-y)
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
                            dic = Analysis_Landmarks.yolo_feature_selection(yolo_landmarks,scale_factor)
                            dic['frame'] = frame_number
                            df_temp = pd.DataFrame([dic])
                            df_posture_features = pd.concat([df_posture_features,df_temp],ignore_index=True)
            elif selectModel == 'mediapipe':
                # mediapipe_landmarks = drawing_object.mediapipe_landmark_detection(frame)
                mediapipe_landmarks = df_landmarks.iloc[frame_number-1]['landmarks']

                if (mediapipe_landmarks and (len(mediapipe_landmarks)>0)):
                    scale_factor = get_scale_factor_mediapipe(mediapipe_landmarks, float(height_runner), height, width)     
                    print(f"scale_factor: {scale_factor}")  
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
                    dic = {}
                    dic = Analysis_Landmarks.mediapipe_feature_selection(mediapipe_landmarks,width,height,scale_factor)
                    dic['frame'] = frame_number
                    df_temp = pd.DataFrame([dic])
                    df_posture_features = pd.concat([df_posture_features,df_temp],ignore_index=True)
            out.write(frame)
            df_all_data.to_csv(f'{write_folder_name}/{input_video_name}_all_data.csv',index=False)
            df_posture_features.to_csv(f'{write_folder_name}/{input_video_name}_posture_features.csv',index=False)

            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cap.release()
        out.release()
        # shutil.copy(f'{write_folder_name}/video_output.mp4', 'static/videos/test.mp4')
        input_path = f"{write_folder_name}/{input_video_name}_video_output.mp4"
        output_path = f"{write_folder_name}/{input_video_name}_annotated_video.mp4"

        subprocess.run([
            ffmpeg_path, '-y','-i', input_path,
            '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
            output_path
        ])
        return("Analysis Done",True,write_folder_name,input_video_name)
    except Exception as e:
        print(f"Error: {e}")
        return(f"Error: {e}",False,"")

def get_scale_factor_mediapipe(landmarks, height_runner,image_height,image_width):
    top = {'x':landmarks[0][0],'y':landmarks[0][1]}  # Nose
    ankle_left = {'x':landmarks[27][0],'y':landmarks[27][1]}  # Left ankle
    ankle_right = {'x':landmarks[28][0],'y':landmarks[28][1]}  # Right ankle

    # Convert to pixel coordinates
    x_top, y_top = int(top['x'] * image_width), int(top['y'] * image_height)
    x_ankle_l, y_ankle_l = int(ankle_left['x'] * image_width), int(ankle_left['y'] * image_height)
    x_ankle_r, y_ankle_r = int(ankle_right['x'] * image_width), int(ankle_right['y'] * image_height)

    # Average ankle position
    x_ankle = (x_ankle_l + x_ankle_r) / 2
    y_ankle = (y_ankle_l + y_ankle_r) / 2

    # Pixel height between head and ankles
    pixel_height = math.sqrt((x_ankle - x_top) ** 2 + (y_ankle - y_top) ** 2)

    if pixel_height == 0:
        return 0  # Avoid division by zero

    # Calculate scale factor (cm per pixel)
    scale_factor = height_runner / pixel_height
    return scale_factor
def height_to_cm(height_str):
    # Remove any spaces and handle formats like 5'6", 5' 6", etc.
    height_str = height_str.replace(" ", "")
    
    # Split at the apostrophe
    try:
        feet, inches = height_str.split("'")
        inches = inches.replace('"', '')  # Remove the inch symbol if present
        feet = int(feet)
        inches = int(inches)
    except:
        raise ValueError("Invalid height format. Use format like 5'6\"")

    # Convert to cm (1 foot = 30.48 cm, 1 inch = 2.54 cm)
    cm = int(round(feet * 30.48 + inches * 2.54))
    return cm
# ChaBot using chatGPT API and RAG system
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    system_answer = {"answer": "Hello, I am ChaBot. How can I help you?"}
    url = f'http://localhost:5678/webhook-test/chatbot?chatInput={message}&sessionId={1234}'
    response = requests.get(url)
    data = response.json()
    print(data.get('output'))
    system_answer["answer"] = data.get('output')
    # n8n_response = response.get('output')
    # print(n8n_response)

    username = message[0]["username"]
    datetime_chat = message[0]["dateTime"]
    text = [
        {"role": "user", "message": message[0]["content"]},
        {"role": "system", "message": system_answer["answer"]}]
    # supabase.table("chat_history").insert([{"username": username, "datetime": datetime_chat, "message": text}]).execute()
    print("Chat history saved successfully.")
    return jsonify(system_answer)


# User runner history
@app.route('/get_user_history', methods=['POST'])
def get_user_history():
    data = request.json
    userEmail = data.get('userEmail')
    
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found.", "history": []})
    user_id = response_email.data[0]['user_id']
    print(f"Useremail:{userEmail} UserID:{user_id}")
    # Find runner under this user
    response_runner = supabase.table("runner").select("*").eq("user_id", int(user_id)).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "No runner found under this user.", "history": []})
    # Find uploaded videos and analysis video from DB
    response = supabase.table("upload_video").select("*, analysis_video(*)").eq("user_id", user_id).execute()
    if len(response.data) == 0:
        return jsonify({"response": False, "message": "No video history found.", "history": []})
    # Construct the response data with video and analysis links 
    uploaded_videos = []
    for video in response.data:
        # Find runner name
        for runner in response_runner.data:
            if video['runner_id'] == runner['runner_id']:
                runner_name = runner['name']
                runner_height = f"{runner['feet']}'{runner['inche']}\""
                runner_gender = runner['gender']
                break
            else:
                runner_name = "Unknown"
                runner_height = "Unknown"
                runner_gender = "Unknown"
        # Find video upload time
        upload_time = video['upload_time']
        upload_time = datetime.datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = upload_time.strftime("%Y-%m-%d %H:%M:%S")
        # Finde video link
        video_link ="download_video/"+ video['video_path']
        # Find analysis video link
        result_link = []
        for result in video['analysis_video']:
            result_link.append("download_video/"+result['analysis_video_path'])

        uploaded_videos.append({
            'runner_name': runner_name,
            'runner_id': video['runner_id'],
            'runner_height': runner_height,
            'runner_gender': runner_gender,
            'timestamp': formatted_time,
            'video_link': video_link,
            'result_link': result_link,
            'video_id': video['video_id'],
            'video_name': video['video_name'],
        })
            
    # print(f"Uploaded videos data: {uploaded_videos}")
    return jsonify({"response": True, "message": "Video history found.", "history": uploaded_videos})

#Get user information and scores
@app.route('/save_runner_score', methods=['POST'])
def save_runner_score():
    data = request.json
    userEmail = data.get("userEmail")
    runnerID = data.get("runnerID")
    season = data.get("season")
    category = data.get("category")
    selectedEvent = data.get("selectedEvent")
    scores = data.get("scores")
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']

    # Find runner info from DB
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runnerID)).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    gender = response_runner.data[0]['gender']
    # Save scores to DB
    # print(f"Scores: {scores}")
    scores_list = [convert_scores_to_float(score) for score in scores if score.strip() != ''] 
    response_save = supabase.table("score").insert({"runner_id": int(runnerID),
                                                    "user_id": int(user_id),
                                                    "season": season,
                                                    "category": category,
                                                    "event": selectedEvent,
                                                    "score_list": json.dumps(scores_list),
                                                    "created_at": str(datetime.datetime.now()),
                                                    }).execute()
    if len(response_save.data) == 0:
        return jsonify({"response": False, "message": "Failed to save scores."})
    
    score_id = response_save.data[0]['score_id']
    scores = [float(val) for val in scores_list]
    # print(scores)
    # Predict ranking based on scores
    plot,df_class_summary,predict_info = ranking_prediction(score_id,category, selectedEvent,season,gender, scores,runner_name=response_runner.data[0]['name'])
    response_save = supabase.table("score").update({"analysis_img_path":plot,"predict_info":predict_info}).eq("score_id",score_id).execute()
    if len(response_save.data) == 0:
        return jsonify({"response": False, "message": "Failed to analysis scores."})
    # Edit the summary DataFrame and heders
    class_columns = ['Cluster', 'Max Best Score', 'Min Best Score', 'Max Avg','Min Avg', 'Mean Avg']
    df_class_summary = df_class_summary[class_columns]
    return jsonify({"response": True, "message": "Scores saved successfully.","plot_path":plot,'class_summary':df_class_summary.to_dict(orient='records'),'class_columns':['Cluster', 'Max Best Score', 'Min Best Score', 'Max Avg','Min Avg', 'Mean Avg']}) 

def convert_scores_to_float(time_str):
    pattern = re.compile(r'^(\d{1,2}):(\d{1,2})\.(\d{1,2})$|^(\d{1,3}\.\d+)$|^(\d{1,3})$')
    match = pattern.match(time_str)

    if not match:
        raise ValueError("Invalid time format")

    if match.group(1) is not None:
        # Format: mm:ss.xx
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        hundredths = int(match.group(3))
        total_seconds = minutes * 60 + seconds + hundredths / 100
    elif match.group(4) is not None:
        # Format: ss.xx — safely parse as float
        total_seconds = float(match.group(4))
    elif match.group(5) is not None:
        # Format: s or ss
        total_seconds = int(match.group(5))
    else:
        raise ValueError("Unrecognized format")

    return round(total_seconds, 2)

def ranking_prediction(score_id,category, selectedEvent,season,gender, scores,runner_name="Unknown"):
    data_dic={'gender':gender,'season':season,'category':category,'event':selectedEvent}
    print(f"Data dic: {data_dic}")
    rc = RankClustering(data_dic)
    pred_cluster = rc.predict_cluster(scores)
    print(f"Predicted cluster: {pred_cluster}")
    plot_title = f"{category} {selectedEvent} {season} Analysis"
    plot_path = rc.draw_boxpolt(pred_cluster,plot_name=f"{score_id}_{category}_{selectedEvent}_{season}.png",is_comparison=False,plot_title=plot_title,runner_name=runner_name)
    df = rc.get_cluster_summary()
    return plot_path,df,pred_cluster

@app.route('/compare_scores_same_season_category_event_gender', methods=['POST'])
def compare_scores_same_season_category_event_gender():
    recived_data = request.json
    userEmail = recived_data.get("userEmail")
    gender = recived_data.get("gender")
    event = recived_data.get("event")
    season = recived_data.get("season")
    category = recived_data.get("category")
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find scores info from DB
    response_score = supabase.table("score").select("*").eq("user_id", int(user_id)).execute()
    if len(response_score.data) == 0:
        return jsonify({"response": False, "message": "No scores found for this user."})
    # Filter scores based on user input selection
    filtered_scores = []
    image_name = f"{gender}_{season}_{category}_{event}"
    plot_title = f"{gender}_{season}_{category}_{event}"
    for data in recived_data['score_data']:
        score_id = data.get("score_id")
        runner_name = data.get("runner_name")
        # Find score info from DB
        for score in response_score.data:
            if (score['score_id'] == int(score_id)):
                image_name=image_name + f"_{int(score_id)}"
                filtered_scores.append({
                    "score_id": score['score_id'],
                    "name": runner_name,
                    "predict_info": score['predict_info']})
                break
    if len(filtered_scores) == 0:
        return jsonify({"response": False, "message": "No matched scores found for this selection."})
    # Predict ranking based on scores
    # image_name = image_name + ".png"
    # print(f"Filtered scores: {filtered_scores}   {image_name}")
    rc = RankClustering({"gender":gender, "season": season, "category": category, "event": event})
    result_path = rc.draw_boxplot_comparison_same_season_evet_category_gender(filtered_scores,plot_name=image_name+".png",plot_title=plot_title)
    # print(f"Result path: {result_path}")
    return jsonify({"response": True, "message": "Scores found successfully.", "result_path": result_path})
       
@app.route('/compare_individual',methods=['POST'])
def compare_individual():
    recived_data = request.json
    name = recived_data.get("name")
    gender = recived_data.get("gender")
    event = recived_data.get("event")
    season = recived_data.get("season")
    category = recived_data.get("category")
    scores = recived_data.get("scores")
    score_id = recived_data.get("score_id")
    # Predict ranking based on scores
    try:
        scores_list = [convert_scores_to_float(score) for score in scores if score.strip() != '']
        # print(f"Scores list: {scores_list}")
        rc = RankClustering({'gender':gender,'season':season,'category':category,'event':event})
        pred_cluster = rc.predict_cluster(scores_list)
        print(f"Predicted cluster: {pred_cluster}")
        # get score data from score id to DB
        print(f"Score ID: {score_id}")
        response_score = supabase.table("score").select("*").eq("score_id", int(score_id)).execute()
        if len(response_score.data) == 0:
            return jsonify({"response": False, "message": "Score ID not found."})
        score_data = response_score.data[0]
        # Save score info to DB
        response_save = supabase.table("score").insert({
            "runner_id": int(score_data['runner_id']),
            "user_id": int(score_data['user_id']),
            "season": season,
            "category": category,
            "event": event,
            "score_list": json.dumps(scores_list),
            "created_at": str(datetime.datetime.now()),
            "isActive": True,
            "predict_info": pred_cluster}).execute()
        if len(response_save.data) == 0:
            return jsonify({"response": False, "message": "Failed to save scores."})
        new_score_id = int(response_save.data[0]['score_id'])

        # Save analysis image path to DB
        response_update = supabase.table("score").update({"score_id": score_id}).eq("score_id", int(score_id)).execute()
        if len(response_update.data) == 0:
            return jsonify({"response": False, "message": "Failed to update scores."})
        # Make plot name
        plot_name = f"{new_score_id}_{category}_{event}_{season}.png"
        plot_title = f"{category} {event} {season} Analysis"
        # # Clean old coeresponding images
        # for old in os.listdir(rc.plot_output_folder):
        #     if old.startswith('last_comparison_') and old.endswith('.png'):
        #         p = os.path.join(rc.plot_output_folder, old)
        #         if os.path.getmtime(p) < time.time() - 12 * 3600:
        #             try: os.remove(p)
        #             except: pass

        # Make new name for image
        # plot_name = f"last_comparison_{int(time.time()*1000)}.png"

        plot_path = rc.draw_boxpolt(pred_cluster, plot_name=f"{plot_name}",is_comparison=False,plot_title=plot_title, runner_name=name)

        # Save the plot path to DB
        response_update = supabase.table("score").update({"analysis_img_path": plot_path}).eq("score_id", int(new_score_id)).execute()
        if len(response_update.data) == 0:
            return jsonify({"response": False, "message": "Failed to update analysis image path."})
        return jsonify({"response": True, "message": "Scores found successfully.", "result_path": plot_path})
    except Exception as e:
        print(f"Error in compare_individual: {e}")
        return jsonify({"response": False, "message": f"Failed to compare individual scores.\n{e}"})


@app.route('/update_scores', methods=['POST'])
def update_scores():
    data = request.json
    userEmail = data.get("userEmail")
    score_id = data.get("score_id")
    season = data.get("season")
    category = data.get("category")
    selectedEvent = data.get("event")
    scores = data.get("scores")
    scores_list = [convert_scores_to_float(score) for score in scores if score.strip() != '']
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # updata score info from DB
    response_update = supabase.table("score").update({"season": season,
                                                     "category": category,
                                                     "event": selectedEvent,
                                                     "score_list": json.dumps(scores_list),
                                                     "updated_at": str(datetime.datetime.now())
                                                    }).eq("score_id", int(score_id)).eq("user_id",int(user_id)).execute()
    print(f"Response update: {response_update.data}")
    if len(response_update.data) == 0:
        return jsonify({"response": False, "message": "Failed to update scores."})
    # Find runner info from DB
    runner_id = response_update.data[0]['runner_id']
    # print(f"Runner ID: {runner_id}")
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runner_id)).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    gender = response_runner.data[0]['gender']
    scores = [float(val) for val in scores_list]
    plot,df_class_summary,predict_info = ranking_prediction(score_id,category, selectedEvent,season,gender, scores,runner_name=response_runner.data[0]['name'])
    response_update = supabase.table("score").update({"analysis_img_path": plot,"predict_info":predict_info}).eq("score_id", int(score_id)).execute()
    if len(response_update.data) == 0:
        return jsonify({"response": False, "message": "Failed to analysis scores."})
    return jsonify({"response": True, "message": "Scores updated successfully.","plot_path": plot})
    # Predict ranking based on scores

@app.route("/delete_scores", methods=['POST'])
def delete_scores():
    data = request.json
    score_id = data.get("score_id")
    # Detete score info from DB
    response_delete = supabase.table("score").update({"isActive": False}).eq("score_id", int(score_id)).execute()
    if len(response_delete.data) == 0:
        return jsonify({"response": False, "message": "Failed to delete scores."})
    return jsonify({"response": True, "message": "Scores deleted successfully."})

@app.route('/find_runner_info',methods=['POST'])
def find_runner_info():
    # Get runner info from json
    useremail=request.json.get('userEmail')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", useremail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner info from DB
    response_runner = supabase.table("runner").select("*").eq("user_id",int(user_id)).eq("isActive",True).execute()
    # print(f"response_runner: {response_runner.data}")
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    return jsonify({"response": True, "message": "Runner info found successfully.", "runners": response_runner.data})


@app.route('/save_runner_info',methods=['POST'])
def save_runner_info():
    data = request.form
    runnerName = data.get('runnerName')
    # Save all name in lowercase
    runnerName = str(runnerName)
    runnerName = runnerName.lower()
    runnerGender = data.get('runnerGender')
    runnerHeightFeet= data.get('ruunerHeightFeet')
    runnerHeightInche= data.get('ruunerHeightInche')
    userEmail = data.get('userEmail')
    runnerID = data.get('runnerID')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner info in DB
    if runnerID == '':
        runnerID = -1
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runnerID)).eq("user_id",int(user_id)).eq("isActive",True).execute()
    if len(response_runner.data) == 0:
        response_runner = supabase.table("runner").select("*").eq("name", runnerName).eq("user_id",int(user_id)).eq("feet",runnerHeightFeet).eq("inche",runnerHeightInche).eq("gender",runnerGender).eq("isActive",True).execute()
        if len(response_runner.data) == 0:
            # If runner not found, insert new runner
            response = supabase.table("runner").insert({"user_id": int(user_id), "name": runnerName,"feet":runnerHeightFeet,"inche":runnerHeightInche,"gender":runnerGender,"created_at":str(datetime.datetime.now()),"isActive":True}).execute()  
            # print(f"Insert response: {response.data}")
            return jsonify({"response": True, "message": "Runner info is added to database.","runnerID":response.data[0]['runner_id']})
        else:
            return jsonify({"response": True, "message": "Runner with same info was in database.","runnerID":response_runner.data[0]['runner_id']})
    else:
        return jsonify({"response": True, "message": "Runner info was in database.","runnerID":response_runner.data[0]['runner_id']})

@app.route('/update_runner_info',methods=['POST'])
def update_runner_info():
    data = request.json
    runnerID = data.get('runnerID')
    userEmail = data.get('userEmail')
    updatedName = data.get('name')
    updatedGender = data.get('gender')
    updatedHeight = data.get('height')

    feet = updatedHeight.split("'")[0]
    inche = updatedHeight.split("'")[1].replace('"', '').strip()

    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner info from DB
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runnerID)).eq("user_id",int(user_id)).eq("isActive",True).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    # Update runner info in DB

    response_update = supabase.table("runner").update({"name": updatedName, "gender":updatedGender,"feet": feet, "inche": inche}).eq("runner_id", int(runnerID)).eq("user_id",int(user_id)).execute()
    if len(response_update.data) == 0:
        return jsonify({"response": False, "message": "Failed to update runner info."})
    return jsonify({"response": True, "message": "Runner info updated successfully."})

@app.route('/get_user_runners', methods=['POST'])
def get_user_runners():
    data = request.json
    userEmail = data.get('userEmail')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner under this user
    response_runner = supabase.table("runner").select("*").eq("user_id", int(user_id)).eq("isActive",True).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": True, "message": "No runner found under this user.","runners":[]})
    runners = []
    for runner in response_runner.data:
        upload_time = runner['created_at']
        upload_time = datetime.datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = upload_time.strftime("%Y-%m-%d %H:%M:%S")
        runners.append({
            "runner_id": runner['runner_id'],
            "name": runner['name'],
            "height": f"{runner['feet']}'{runner['inche']}\"",
            "gender": runner['gender'],
            "created_at": formatted_time,
            "userEmail": userEmail
        })
    return jsonify({"response": True, "message": "Runners found successfully.","runners":runners})


@app.route('/delete_runner', methods=['POST'])
def delete_runner():
    data = request.json
    runnerID = data.get('runnerID')
    userEmail = data.get('userEmail')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner info from DB
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runnerID)).eq("user_id",int(user_id)).execute()
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    # Delete runner from DB
    response_delete = supabase.table("runner").update({"isActive":False}).eq("runner_id", int(runnerID)).execute()
    if len(response_delete.data) == 0:
        return jsonify({"response": False, "message": "Failed to delete runner."})
    return jsonify({"response": True, "message": "Runner deleted successfully."})


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.json
    userEmail = data.get('userEmail')
    # Find user info from DB
    response_email = supabase.table("user").select("*").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_info = response_email.data[0]
    time = user_info['created_at']
    time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"response": True, "message": "User info found successfully.",
                    "full_name": user_info['full_name'],
                    "role": user_info['role'],
                    "created_at": formatted_time
                    })

@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    data = request.json
    userEmail = data.get('useremali')
    full_name = data.get('full_name')
    role = data.get('role')
    print(f"Update user info: email={userEmail}, full_name={full_name}, role={role}")
    # Update user info from DB
    response_update = supabase.table("user").update({"full_name": full_name,'role':role}).eq("email", userEmail).execute()
    if len(response_update.data) == 0:
        return jsonify({"response": False, "message": "Failed to update user info."})
    return jsonify({"response": True, "message": "User info updated successfully."})

@app.route('/change_user_password', methods=['POST'])
def change_user_password():
    data = request.json
    userEmail = data.get('useremali')
    new_password = data.get('newPassword')
    current_password = data.get('currentPassword')
    print(f"Change password for email: {userEmail}")
    # Check current password
    response = supabase.table("user").select("password").eq("email", userEmail).execute()
    if len(response.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    if response.data[0]['password'] == new_password:
        return jsonify({"response": False, "message": "New password cannot be the same as the current password."})
    if response.data[0]['password'] != current_password:
        return jsonify({"response": False, "message": "Current password is incorrect."})
    # Update user password from DB
    auth_response = supabase.table("user").update({"password": new_password}).eq("email", userEmail).execute()
    if len(auth_response.data)==0:
        return jsonify({"response": False, "message": "Failed to change password. User not found."})
    return jsonify({"response": True, "message": "Password changed successfully."})
    
@app.route('/get_user_scores', methods=['POST'])
def get_user_scores():
    data = request.json
    userEmail = data.get('userEmail')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", userEmail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find scores under this user
    response_scores = supabase.table("score").select("*").eq("user_id", int(user_id)).eq("isActive",True).execute()
    if len(response_scores.data) == 0:
        return jsonify({"response": True, "message": "No scores found under this user.","scores":[]})
    scores = []
    # Find runner name
    # response_runner = supabase.table("runner").select("name").eq("runner_id", score['runner_id']).execute()
    response_runner = supabase.table("runner").select("name,runner_id,gender").eq("user_id",int(user_id)).execute()

    for score in response_scores.data:
        # Find runner name
        runner_name = "Unknown"
        gender = "Unknown"
        for runner in response_runner.data:
            if score['runner_id'] == runner['runner_id']:
                runner_name = runner['name']
                gender = runner['gender']
                break
            else:
                runner_name = "Unknown"
                gender = "Unknown"
       # Find season, category, event
        season = score['season']
        category = score['category']
        event = score['event']
        # Find created_at time
        created_at = score['created_at']
        created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")
        # Find scores
        scores_list = json.loads(score['score_list'])
        scores.append({
            "score_id": score['score_id'],
            "runner_name": runner_name,
            "gender":gender,
            "season": season,
            "category": category,
            "event": event,
            "scores": scores_list,
            "created_at": formatted_time,
            "analysis_img_path":score['analysis_img_path']
        })
    return jsonify({"response": True, "message": "Scores found successfully.","scores":scores})


@app.route('/convert_upload_video_preview', methods=['POST'])
def convert_upload_video_preview():
    video_file = request.files.get("video") or request.files.get("videoUpload")
    print(f"video file: {video_file}")
    # Check if video file is provided
    if not video_file:
        return jsonify({"response": False, "message": "No video file provided."})
    # Check if temp folder is existing
    if not os.path.exists(TEMP_VIDEO_SAVE_PATH):
        os.makedirs(TEMP_VIDEO_SAVE_PATH)
    # Delete all files in the temporary video save directory
    for filename in os.listdir(TEMP_VIDEO_SAVE_PATH):
        file_path = os.path.join(TEMP_VIDEO_SAVE_PATH, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            continue
    # Save video on the temporary path
    video_path = os.path.join(TEMP_VIDEO_SAVE_PATH, video_file.filename)
    with open(video_path, "wb") as f:
        video_file.save(f)
    # Call the video conversion function (to be implemented)
    preview_path = convert_video_to_preview(video_path)
    if not preview_path:
        return jsonify({"response": False, "message": "Failed to create video preview."})
    return jsonify({"response": True, "message": "Video preview created successfully.", "preview_path": preview_path})

def convert_video_to_preview(video_path):
    # convert video file to mp4
    input_path = video_path
    output_path = f"{TEMP_VIDEO_SAVE_PATH}/{os.path.basename(video_path)}.mp4"

    subprocess.run([
        ffmpeg_path, '-y','-i', input_path,
        '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
        output_path
    ])
    output_path = "video/" + output_path
    print(f"Converted video saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
