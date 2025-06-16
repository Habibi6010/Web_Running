from flask import Flask, jsonify, request, render_template,send_from_directory
from flask_cors import CORS
import json
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

##### Main Variable for  Address of server and video save path
# Define a directory to save the video files when user uploads
VIDEO_SAVE_PATH = 'received_videos/'
# Define a directory to save the analyzed video files
ANALYZED_VIDEO_SAVE_PATH = 'analyzed_video_file/'

# Server fetch address
# fetch_address = "13.59.211.224"
fetch_address = "127.0.0.1"


# supabase api infroamtion
SUPABASE_URL = "https://cgttxnlppkmiguxcxpvh.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNndHR4bmxwcGttaWd1eGN4cHZoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MTYzOTk5NCwiZXhwIjoyMDU3MjE1OTk0fQ.3DldbLH07uvz_ctAwxXSqJ9fscE5LkgvBZ9SeXLe5fc"

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

@app.route('/profile')
def porfile():
    return render_template('profile.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # Need to Connect to Database to check the email and password
    if (email == 'habibi6010@gmail.com' and password == '123') or (email == 'nourani@utdallas.edu' and password == '1234'):
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



@app.route('/run_analysis', methods=['POST'])
def run_analysis():
    video_file = request.files.get('videoUpload')
    username = request.form.get('username')
    height_runner = request.form.get('height_runner')
    selectedModel = request.form.get('selectedModel')
    print(height_runner, selectedModel)
    # Create Recived Video Folder
    if not os.path.exists(VIDEO_SAVE_PATH):
        os.makedirs(VIDEO_SAVE_PATH)
        print(f"Folder created: {VIDEO_SAVE_PATH}")
    else:
        print(f"Folder already exists: {VIDEO_SAVE_PATH}")
    # get the uploaded video file
    if video_file:
        video_file.save(f'{VIDEO_SAVE_PATH}{username}_{video_file.filename}')
        print('Video file saved successfully')
    else:
        print('No video file uploaded')
        return jsonify({"response": False, "message": "No video file uploaded"})
    video_address = f'{VIDEO_SAVE_PATH}{username}_{video_file.filename}'
    print(f"video file address: {video_address}")
    # threading.Thread(target=background_analysis, args=(selectedModel,video_address)).start()
    background_analysis(selectedModel, video_address)
    return jsonify({"response": True,"message":" Video is being analyzed in the background"})

def background_analysis(selected_model, video_address):   
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
    # Save to DataFrame and CSV
    df = pd.DataFrame(frame_landmarks)
    # filename = os.path.basename(video_address)  # 'test@gmail.com_test_video.MOV'
    name_without_ext = os.path.splitext(video_address)[0]  # 'test@gmail.com_test_video'
    output_csv = name_without_ext + '_landmarks.csv'
    df.to_csv(output_csv, index=False)
    print(f"Saved landmarks for each frame to {output_csv}")
    


def run_analysis_orginal():

    video_file = request.files.get('videoUpload')
    username = request.form.get('username')
    height_runner = request.form.get('height_runner')
    selectedModel = request.form.get('selectedModel')
    settings_colors = request.form.get('settings_colors')
    settings_colors = json.loads(settings_colors) if settings_colors else {}
    print(height_runner, selectedModel, settings_colors)
    if not os.path.exists(VIDEO_SAVE_PATH):
        os.makedirs(VIDEO_SAVE_PATH)
        print(f"Folder created: {VIDEO_SAVE_PATH}")
    else:
        print(f"Folder already exists: {VIDEO_SAVE_PATH}")
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
    print(f'file: {write_file_name}')
    # send email to user with the link of the video and csv file

    file_link = f"http://{fetch_address}:5001/download_video/{write_file_name}"
    csv_link = f"http://{fetch_address}:5001/download_csv/{write_file_name}"
    print(f"file_link: {file_link}")
    print(f"csv_link: {csv_link}")
    i = 0
    while i < 3:
        if (tools.send_email(username,file_link,csv_link)):
            break
        else:
            i += 1
    return jsonify({"response": response, "message": text,"videoaddress":write_file_name,"csvaddress":write_file_name})



@app.route('/download_csv/<filename>', methods=['GET'])
def download_csv_file(filename):
    # Decode the filename as Flask encodes URLs.
    decoded_filename = urllib.parse.unquote(filename)
    print(f"Download file: {os.path.abspath(ANALYZED_VIDEO_SAVE_PATH)}/{decoded_filename}")
    return send_from_directory(os.path.abspath(ANALYZED_VIDEO_SAVE_PATH)+"/"+decoded_filename, "all_data.csv")

@app.route('/download_video/<path:foldername>', methods=['GET'])
def download_video_file(foldername):
    decoded_foldername = urllib.parse.unquote(foldername)  # KEEP @ character
    abs_dir = os.path.abspath(os.path.join(ANALYZED_VIDEO_SAVE_PATH, decoded_foldername))

    video_filename = "video_output.mp4"
    video_file_path = os.path.join(abs_dir, video_filename)

    if not os.path.exists(video_file_path):
        return f"File not found: {video_file_path}", 404

    print(f"Serving video from {video_file_path}")
    return send_from_directory(abs_dir, video_filename, as_attachment=True)


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
                mediapipe_landmarks = drawing_object.mediapipe_landmark_detection(frame)
                if (len(mediapipe_landmarks)>0):
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
        
        return("Analysis Done",True,write_folder_name.split("/")[-1])
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




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=False)
