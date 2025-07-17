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


##### Main Variable for  Address of server and video save path
# Define a directory to save the video files when user uploads
VIDEO_SAVE_PATH = 'received_videos/'
# Define a directory to save the analyzed video files
ANALYZED_VIDEO_SAVE_PATH = 'analyzed_video_file/'
# Definfe ffmpeg path
ffmpeg_path = r"C:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
# Server fetch address
# fetch_address = "13.59.211.224"
fetch_address = "127.0.0.1"


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
            "landmark_path": output_csv
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

    message,response,write_folder_name= drawing_on_video(setting_colors,userEmail,video_info,runner_height)

    # Save the analyzed video path to database
    if response:
        response_update = supabase.table("analysis_video").insert({
            "video_id": video_id,
            "analysis_video_path": write_folder_name + '/fixed_output.mp4',
            "analysis_csv_path": write_folder_name + '/all_data.csv',
            "analysis_setting": json.dumps(setting_colors)
        }).execute()
        if len(response_update.data) == 0:
            print("Failed to update analyzed video path in database")
            return jsonify({"response": False, "message": "Failed to update analyzed video path in database"})

    output_video_address = write_folder_name + '/fixed_output.mp4'
    print(f"Output video address URL: {output_video_address}")
    output_video_csv = write_folder_name + '/all_data.csv'
    print(f"Output video csv address URL: {output_video_csv}") 

    return jsonify({"response": response, "message": message, "videoaddress": output_video_address, "csvaddress": output_video_csv})

def drawing_on_video(settings_colors,userEmail,video_info,runner_height):
    drawing_object = drawing()
    username = userEmail
    timestamp = datetime.datetime.strptime(video_info['upload_time'], "%Y-%m-%dT%H:%M:%S.%f")
    timestamp = timestamp.strftime("%Y%m%d%H%M%S") # YYYYMMDDHHMMSS
    input_video_name = video_info['video_name']
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
        out = cv2.VideoWriter(f'{write_folder_name}/video_output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),
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
            df_all_data.to_csv(f'{write_folder_name}/all_data.csv',index=False)
            df_posture_features.to_csv(f'{write_folder_name}/posture_features.csv',index=False)
            
            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cap.release()
        out.release()
        # shutil.copy(f'{write_folder_name}/video_output.mp4', 'static/videos/test.mp4')
        input_path = f"{write_folder_name}/video_output.mp4"
        output_path = f"{write_folder_name}/fixed_output.mp4"

        subprocess.run([
            ffmpeg_path, '-y','-i', input_path,
            '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
            output_path
        ])
        return("Analysis Done",True,write_folder_name)
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


# User history
@app.route('/get_user_history', methods=['POST'])
def get_user_history():
    data = request.json
    username = data.get('username')
    print(f"Username:{username}")
    user_video_path = f"{VIDEO_SAVE_PATH}{username}"
    analyzed_user_video_path = f"{ANALYZED_VIDEO_SAVE_PATH}{username}"
    if not os.path.exists(user_video_path):
        print(f"User video folder does not exist: {user_video_path}")
        return jsonify({"response": False, "message": "No video history found.", "history": []})
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    video_files = [f for f in os.listdir(user_video_path) if f.lower().endswith(video_extensions)]
    # print(f"Found {len(video_files)} video files for user {username}.")
    # print(f"Video files: {video_files}")
    uploaded_videos = []
    for video_file in video_files:
            parts = video_file.split('_',1)
            video_name = parts[1] if len(parts) > 1 else video_file
            timestamp_str = parts[0]
            try:
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_time = "Unknown"
            
            # print(f"Processing video file: {video_file} with timestamp: {formatted_time} and name: {video_name}")
            video_link = f"download_video/{user_video_path}/{video_file}"
            # print(f"User video path: {video_link}")

            result_folders = os.listdir(analyzed_user_video_path)
            result_link = []
            for folder in result_folders:
                if video_file in folder:
                    result_path = analyzed_user_video_path + "/" + folder
                    result_link.append(f"download_video/{result_path}/fixed_output.mp4")

            uploaded_videos.append({
                'video_name': video_name,
                'timestamp': formatted_time,
                'video_link': video_link,
                'result_link': result_link
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
    # Save scores to DB
    scores_dic = {str(i+1): int(val) for i, val in enumerate(scores)}
    response_save = supabase.table("score").insert({"runner_id": int(runnerID),
                                                    "user_id": int(user_id),
                                                    "season": season,
                                                    "category": category,
                                                    "event": selectedEvent,
                                                    "score_list": json.dumps(scores_dic)
                                                    }).execute()
    if len(response_save.data) == 0:
        return jsonify({"response": False, "message": "Failed to save scores."})
    return jsonify({"response": True, "message": "Scores saved successfully.","score_id": response_save.data[0]['score_id'] })

@app.route('/find_runner_info',methods=['POST'])
def find_runner_info():
    # Get runner info from json
    runner_id=request.json.get('runnerID')
    useremail=request.json.get('userEmail')
    # Find user id from DB
    response_email = supabase.table("user").select("user_id").eq("email", useremail).execute()
    if len(response_email.data) == 0:
        return jsonify({"response": False, "message": "User email not found."})
    user_id = response_email.data[0]['user_id']
    # Find runner info from DB
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runner_id)).eq("user_id",int(user_id)).execute()
    # print(f"response_runner: {response_runner.data}")
    if len(response_runner.data) == 0:
        return jsonify({"response": False, "message": "Runner ID not found."})
    return jsonify({"response": True, "message": "Runner info found successfully.",
                    "name": response_runner.data[0]['name'],
                    "heightFeet": response_runner.data[0]['feet'],
                    "heightInches": response_runner.data[0]['inche'],
                    "gender": response_runner.data[0]['gender']
                    })


@app.route('/save_runner_info',methods=['POST'])
def save_runner_info():
    data = request.form
    runnerName = data.get('runnerName')
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
    response_runner = supabase.table("runner").select("*").eq("runner_id", int(runnerID)).eq("user_id",int(user_id)).execute()
    if len(response_runner.data) == 0:
        response_runner = supabase.table("runner").select("*").eq("name", runnerName).eq("user_id",int(user_id)).eq("feet",runnerHeightFeet).eq("inche",runnerHeightInche).eq("gender",runnerGender).execute()
        if len(response_runner.data) == 0:
            # If runner not found, insert new runner
            response = supabase.table("runner").insert({"user_id": int(user_id), "name": runnerName,"feet":runnerHeightFeet,"inche":runnerHeightInche,"gender":runnerGender}).execute()  
            # print(f"Insert response: {response.data}")
            return jsonify({"response": True, "message": f"Runner info added to DB. Runner ID is {response.data[0]['runner_id']}","runnerID":response.data[0]['runner_id']})
        else:
            return jsonify({"response": True, "message": f"Runner with same info was in DB. Runner ID is {response_runner.data[0]['runner_id']}","runnerID":response_runner.data[0]['runner_id']})
    else:
        return jsonify({"response": True, "message": "Runner info was in DB.","runnerID":response_runner.data[0]['runner_id']})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
