import numpy as np
import math
import cv2
import fpdf
import PIL.Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

class tools:
    
    
    def __init__(self):
        pass
    
    # input : 2 lits [x,y] and wight and hight of frame 
    # output : distance between two point
    def calculate_distance_mediapipe(a,b,w,h):
        a = np.array(a) # First
        b = np.array(b) # Mid
        dist=np.sqrt(((b[0]*w)-(a[0]*w))**2 + ((b[1]*h)-(a[1]*h))**2)
        return dist
    # input : 2 lits [x,y] and wight and hight of frame 
    # output : distance between two point
    def calculate_distance_yolo(a,b):
        a = np.array(a) # First
        b = np.array(b) # Mid
        dist=np.sqrt(((b[0])-(a[0]))**2 + ((b[1])-(a[1]))**2)
        return dist    
    # input : 3 pint for angel [x,y]
    # output : Calculate angle (degree)
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle 
    
    def calculate_angle_3D(A, B, C):
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        AB = B - A
        BC = C - B

        dot_product = np.dot(AB, BC)
        magnitude_AB = np.linalg.norm(AB)
        magnitude_BC = np.linalg.norm(BC)

        angle_rad = np.arccos(dot_product / (magnitude_AB * magnitude_BC))
        angle_deg = np.degrees(angle_rad)

        return angle_deg
    def calculate_angle_with_z_axis(point1, point2):
        # Calculate the vector between the two points
        vector = [point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2]]
        
        # Calculate the length of the vector
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        
        # Normalize the vector
        normalized_vector = [coord / vector_length for coord in vector]
        
        # Define the z-axis unit vector
        z_axis_vector = [0, 0, 1]
        
        # Calculate the dot product between the normalized vector and the z-axis vector
        dot_product = sum(a * b for a, b in zip(normalized_vector, z_axis_vector))
        
        # Calculate the angle between the two vectors in radians
        angle_radians = math.acos(dot_product)
        
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees
    
    def calculate_angle_with_x_axis(point1, point2):
        # Calculate the vector between the two points
        vector = [point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2]]
        
        # Calculate the length of the vector
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        
        # Normalize the vector
        normalized_vector = [coord / vector_length for coord in vector]
        
        # Define the x-axis unit vector
        x_axis_vector = [1, 0, 0]
        
        # Calculate the dot product between the normalized vector and the x-axis vector
        dot_product = sum(a * b for a, b in zip(normalized_vector, x_axis_vector))
        
        # Calculate the angle between the two vectors in radians
        angle_radians = math.acos(dot_product)
        
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        
        # Adjust the angle based on the direction (y-component of the vector)
        if vector[1] > 0:
            angle_degrees = 360 - angle_degrees
        return angle_degrees
    
    def calculate_angle_with_y_axis(point1, point2):
        # Calculate the vector between the two points
        vector = [point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2]]
        
        # Calculate the length of the vector
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        
        # Normalize the vector
        normalized_vector = [coord / vector_length for coord in vector]
        
        # Define the y-axis unit vector
        y_axis_vector = [0, 1, 0]
        
        # Calculate the dot product between the normalized vector and the y-axis vector
        dot_product = sum(a * b for a, b in zip(normalized_vector, y_axis_vector))
        
        # Calculate the angle between the two vectors in radians
        angle_radians = math.acos(dot_product)
        
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees
    
    ### Draw cconnection line in yolo
    def draw_connections_yolo(frame, keypoints, confidence_threshold):
        EDGES = {
            (0, 1): 'm',
            (0, 2): 'c',
            (1, 3): 'm',
            (2, 4): 'c',
            (0, 5): 'm',
            (0, 6): 'c',
            (5, 7): 'm',
            (7, 9): 'm',
            (6, 8): 'c',
            (8, 10): 'c',
            (5, 6): 'y',
            (5, 11): 'm',
            (6, 12): 'c',
            (11, 12): 'y',
            (11, 13): 'm',
            (13, 15): 'm',
            (12, 14): 'c',
            (14, 16): 'c'
        }
        # print(keypoints)
        for keypoint in keypoints:
            if keypoint.size >0:
                for edge, color in EDGES.items():
                    p1, p2 = edge
                    x1, y1, c1 = keypoint[p1]
                    x2, y2, c2 = keypoint[p2]
                    if (float(c1) > confidence_threshold) and (float(c2) > confidence_threshold):
                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)
        return frame


    #Draw Landmark and boxes in yolo
    def draw_landmark(frame,bboxs,keypoints):   
        for bbox in bboxs:
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)      
        for keypoint_person in keypoints:
            i=0
            for keypoint in keypoint_person:
                cv2.circle(frame, (int(keypoint[0]), int(keypoint[1])), 5, (0, 0, 255), -1)
                # cv2.putText(frame, str(i),  (int(keypoint[0])+5, int(keypoint[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                i=i+1
            # if keypoint_person.size >0:
            #     draw_connections_yolo(frame,keypoint_person,0.5)
        
        return frame
    ################################## Concate Image functions ###########################
    def vconcat_resize(img_list, interpolation  
                    = cv2.INTER_CUBIC): 
        # take minimum width 
        w_min = min(img.shape[1]  
                    for img in img_list) 
        
        # resizing images 
        im_list_resize = [cv2.resize(img, 
                        (w_min, int(img.shape[0] * w_min / img.shape[1])), 
                                    interpolation = interpolation) 
                        for img in img_list] 
        # return final image 
        return cv2.vconcat(im_list_resize) 

    def hconcat_resize(img_list,  
                    interpolation  
                    = cv2.INTER_CUBIC): 
        # take minimum hights 
        h_min = min(img.shape[0]  
                    for img in img_list) 
        
        # image resizing  
        im_list_resize = [cv2.resize(img, 
                        (int(img.shape[1] * h_min / img.shape[0]), 
                            h_min), interpolation 
                                    = interpolation)  
                        for img in img_list] 
        
        # return final image 
        return cv2.hconcat(im_list_resize) 

    ############## PDF Report ################
    def create_report(file_path, data):
        # Iterate through the data and add text and three images to the PDF for each row
        i=0
        
        for row in data:
            pdf=fpdf.FPDF()
            pdf.add_page()
            pdf.set_font("Arial",size=10)
            
            text = row.get('text', '')
            images = row.get('images', [])
            # Add text to the PDF
            pdf.cell(w=150,h=10,txt=text,ln=True,align='C')
            
            # Add images to the PDF
            new_img=np.vstack(images)
            img_pil = PIL.Image.fromarray(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))
            img_pil.save("temp_image.jpg")  # Save the temporary image
            pdf.image("temp_image.jpg", x=pdf.w/2-50, y=pdf.get_y(), w=100)
            t=f'{i}_{file_path}'
            i=i+1
            pdf.output(t)
        # pdf.output(file_path)
    ########################## Save image with lable ###########    
    def add_text_to_image(image, text, text_color=(255, 255, 255), background_color=(0, 0, 0), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=2, thickness=2):
        # Get the size of the image
        image_size = (image.shape[1], image.shape[0])

        # Calculate the size of each line of text
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

        # Calculate the starting position for the text
        x = (image_size[0] - text_size[0]) // 2
        y = text_size[1] + 10  # Starting from a bit below the top

        # Split the text into lines if it's too long for the image width
        words = text.split()
        lines = []
        line = ''
        for word in words:
            test_line = line + word + ' '
            test_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
            if test_size[0] <= image_size[0] - 20:  # Leave a margin
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        
        # Calculate the height of the rectangle based on the number of lines
        rectangle_height = len(lines) * (text_size[1] + 5)

        # Draw a filled black rectangle as the background for the text
        cv2.rectangle(image, (0, y - text_size[1] - 5), (image_size[0] + 5, y + rectangle_height), background_color, thickness=cv2.FILLED)

        # Write each line of text on the image
        for line in lines:
            cv2.putText(image, line, (10, y), font, font_scale, text_color, thickness, cv2.LINE_AA)
            y += text_size[1] + 5  # Add some space between lines

        return image
    
    def save_images(data,save_path):
        i=0        
        for row in data: 
            text = row.get('text', '')
            images = row.get('images', [])            
            # Add images to the PDF
            for image in images:
                tools.add_text_to_image(image,text)
            cv2.imwrite(f'{save_path}mediapipe\{i}.jpg',images[0])
            cv2.imwrite(f'{save_path}yolo\{i}.jpg',images[1])
            i=i+1

    def send_email(receiver_email, video_link, csv_link):
        # Email configuration
        sender_email = "mo.habibideh990@gmail.com"  # Your Gmail address
        app_password = "zdha iqsm wkrc ivcw"  # Replace with your App Password

        # Email content
        subject = "Processed Video and CSV Links"
        body = f"Hello \n\n Here are your links:\n\nVideo: {video_link}\nCSV: {csv_link}"

        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)  # Use Gmail's SMTP server and port
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, app_password)  # Log in with App Password
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            server.close()  # Close the connection to the server
    
    def send_forget_password_email(receiver_email, new_password):
        # Email configuration
        sender_email = "mo.habibideh990@gmail.com"  # Your Gmail address
        app_password = "zdha iqsm wkrc ivcw"  # Replace with your App Password

        # Email content
        subject = "Requested Password Reset"
        body = f"Hello \n\n Here are is your new password:\n\nNew Password: {new_password} \n\nPlease change it after logging in."

        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)  # Use Gmail's SMTP server and port
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, app_password)  # Log in with App Password
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            server.close()  # Close the connection to the server

    def generate_strong_password(length=12):
        # Ensure we include letters, digits, and punctuation
        characters = string.ascii_letters + string.digits + string.punctuation
        # Use secrets.choice for cryptographic randomness
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password