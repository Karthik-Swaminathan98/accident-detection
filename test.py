import os
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

print("hello")
np.set_printoptions(suppress=True)
a=0
model = tensorflow.keras.models.load_model('Accident.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
print("Camera")

SENDER_ADDRESS = os.environ['SENDER_ADDRESS']
SENDER_PASS = os.environ['SENDER_PASS']
RECEIVER_ADDRESSES = os.environ['RECEIVER_ADDRESSES'].split(',')
ALERT_LOCATION = os.environ.get('ALERT_LOCATION', 'Unknown')

while(True):
    ret,frame = cap.read()
    size = (224, 224)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    prediction*=100
    class1 = int(prediction[0][0])
    class2 = int(prediction[0][1])
    if(class1>50):
        print("Accident Occured")
        cv2.putText(frame,'Accident Occured',(10,50),font,1,(0,0,255),2)
        a=a+1
        print(a)
        if(a==20):
            cv2.imwrite("NewPicture.jpg",frame)
            mail_content = 'Location: ' + ALERT_LOCATION
            message = MIMEMultipart()
            message['From'] = SENDER_ADDRESS
            message['To'] = ", ".join(RECEIVER_ADDRESSES)
            message['Subject'] = 'Accident Detection'
            message.attach(MIMEText(mail_content, 'plain'))
            attach_file_name = 'NewPicture.jpg'
            attach_file = open(attach_file_name, 'rb')
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)
            payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(SENDER_ADDRESS, SENDER_PASS)
            text = message.as_string()
            session.sendmail(SENDER_ADDRESS, RECEIVER_ADDRESSES, text)
            session.quit()
            print('Mail Sent')
                
    else:
        print("Accident not Occured")
        cv2.putText(frame,'Accident not Occured',(10,50),font,1,(0,0,255),2)
        a=0
        print(a)
    #print(class1,class2)
    cv2.imshow("display",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


