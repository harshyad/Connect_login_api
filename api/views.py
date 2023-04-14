import cv2
# import face_recognition
import sys
import dlib
import os
import jwt
import datetime
import bcrypt
import smtplib
import shutil

from rest_framework.decorators import api_view
from rest_framework.response import Response

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# predictor_path = sys.argv[1]
# face_rec_model_path = sys.argv[2]
# faces_folder_path = sys.argv[3]

# detector = dlib.get_frontal_face_detector()
# sp = dlib.shape_predictor(predictor_path)
# facerec = dlib.face_recognition_model_v1(face_rec_model_path)

face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"  # Update with the correct file path
face_recognition = dlib.face_recognition_model_v1(face_rec_model_path)

# Local Imports
from api.serializers import Imageserializer, teacherserializer
from api.models import student_models, teacher_models

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder = '1iwZ2iE3e_7tfegKAI-halhhK9fn9Nv-A'

# Logic of functions


def sendMail(*args):
    pk = ''
    if (args[0] == 'student'):
        pk = "Rollno"
    else:
        pk = "Email"
    message = MIMEMultipart('alternative')
    message['Subject'] = "Credentials"
    html = f'''<html><body><table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td bgcolor="#F9FAFC">
                    <div align="center" style="padding: 45px 0;">
                        <table border="0" cellpadding="0" cellspacing="0" style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.5em;max-width: 500px;">
                            <thead>
                                <tr>
                                    <td style="text-align: center;"><img src="https://user-images.githubusercontent.com/90459197/229793821-61fd3ae8-342b-4ba8-a577-7cf41182d120.png" style="margin-bottom: 1rem; width: 210px; " alt=""></td>
                                </tr>
                                <tr>
                                    <td style="background-color: #1f74ca; color: white; padding: 0 20px; border-radius: 15px 15px 0 0;">
                                        <h2 align="center">Credentials</h2>
                                    </td>
                                </tr>
                            </thead>
                            <tbody style="background-color: white;padding: 40px 20px;border-radius: 0 0 15px 15px;display: block;box-shadow: 0 10px 30px -30px black;">
                                <tr>
                                    <td>
                                        <p align="center" style="margin: 0; color: #475467;">Hi, <strong>{args[1]}</strong></p>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <p align="center" style="color: #7a899f;margin-bottom: 0;font-size: 14px;">We're sending you this email because you have registered on our platform. Your credentials are {pk} - {args[2]} and password - {args[3]} </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <a href="javascript:void(0)" style="text-decoration: none;display: inline-block;min-width: 100px;text-align: center;padding: 10px 30px;margin: 30px auto;background-color: #1f74ca; color: white; border-radius: 10px; transition: all 0.3s ease;">Login</a>    
                                    </td>
                                </tr>
                            </tbody>
                        <tfoot>
                            <tr>
                            <td>
                                <p align="center">
                                <small style="color:#7a899f;">
                                &copy;2023 Copyright <a href="#" target="_blank" style="text-decoration: none; color: #1f74ca;">Connect </a>. All Rights Reserved.
                                </small>
                                </p>
                            </td>
                            </tr>
                        </tfoot>
                        </table>
                    </div>
                </td>
            </tr>
        </table></body></html>'''
    part2 = MIMEText(html, 'html')
    message.attach(part2)
    msg = message.as_string()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    # msg = "Hello"
    s.login("connect.lms.developers@gmail.com", "xfmsbsfletutkkcx")
    
    if (pk == 'Rollno'):
        print("Logged in")
        s.sendmail("connect.lms.developers@gmail.com",
                   args[4], msg)
        print("Sent mail")
    elif (pk == 'Email'):
        print("Logged in")
        s.sendmail("connect.lms.developers@gmail.com",
                   args[2], msg)
        print("Sent mail")
    s.quit()

    return


def loginlogic(password, user):

    if user is None:
        return Response({"status":False,"msg": 'User Not Found'})

    # password = password.encode('utf-8')
    # bcrypt.checkpw(password,user.password)

    if (user.password != password):
        return Response({"status":False,"msg": "Incorrect Password"})

    else:

        try:

            try:
                if(user.user_type == "student"):

                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'roll_no': user.roll_no,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                        'iat': datetime.datetime.utcnow(),
                    }
                    serializer = Imageserializer(user)
                    token = jwt.encode(payload, 'secret', algorithm='HS256')
                    return Response({
                        "status":True,
                        "message": "Successfully Logged in",
                        "user_data":serializer.data,
                        "token":token
                    })
                else:
                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                        'iat': datetime.datetime.utcnow(),
                    }
                    token = jwt.encode(payload, 'secret', algorithm='HS256')
                    serializer = teacherserializer(user)
                    return Response({
                        "status":True,
                        "message": "Successfully Logged in",
                        "user_data":serializer.data,
                        "token": token
                    })
            except:
                return Response({"status":False,"msg":"Error"})
        except:
            return Response({"status":False,"msg":"Some Error occured"})

def saveImage(name):
    directory = "media"
    for f in os.listdir(directory):
        arr = name.split()
        name = "".join(arr)
        name = name.lower()
        if(f.split(".")[0]==name):
            filename = os.path.join(directory,f)
            gfile = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : f})
            gfile.SetContentFile(filename)
            gfile.Upload()
            shutil.rmtree('media', ignore_errors=False)
            return
        else:
            continue
    return
        

def rename_image(user_type,email,name):
    arr = name.split()
    name = "".join(arr)
    name = name.lower()
    if(user_type == "student"):
        data = student_models.objects.get(email=email)
    else:
        data = teacher_models.objects.get(email=email)
    fid = ""
    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
    for index, file in enumerate(file_list):
        if(file['title'].split(".")[0] == name):
            fid = file['id']
            data.image = f"https://drive.google.com/file/d/{fid}" # type: ignore
            data.save()
            return
        else:
            continue
    return


# Create your views here.

@api_view(['POST'])
# For Comparing the image taken and the image stored in the database.
def facelogin(request):

    if request.method == 'POST':

        try:
            name = request.data['name']
            email = request.data['email']
            image = request.data['image']
            user_type = request.data['user_type']
        except:
            return Response({"Error": "Please provide all the details"})

        arr = name.split()
        name = "".join(arr)
        name = name.lower()

        # cam = cv2.VideoCapture(0)
        # cv2.namedWindow('Python WebCam Screenshot App')

        # img_counter = 0

        # while True:
        #     ret, frame = cam.read()

        #     if not ret:
        #         break

        #     cv2.imshow('test', frame)

        #     k = cv2.waitKey(1)

        #     # if k%256 == 27:
        #     #     print("Escape hit , Closing the app")
        #     #     break

        #     if k % 256 == 32:
        #         # img_name = "E:\\Desktop\\College_Work\\College_Final_Project\\Face\\Face\\media\\Matching.jpg".format(img_counter)
        #         img_name = "//home//harshyadav//Desktop//Face-Login-Api//Face_Login_college_Project//media//match.jpg".format(
        #             img_counter)
        #         cv2.imwrite(img_name, frame)
        #         img_counter += 1
        #         break

        # try:
        #     file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
            # for index, file in enumerate(file_list):
            #     if(file['title'].split(".")[0] == name):
            #         print(file['id'])
            #         print('file downloaded : ', file['title'])
            #         file.GetContentFile(file['title'])
            # known_image = face_recognition.load_image_file(f"{name}.jpg")
            # # unknown_image = face_recognition.load_image_file("media/match.jpg")
            # unknown_image = face_recognition.load_image_file(image)

            # image1_encoding = face_recognition.face_encodings(known_image)[0]
            # image2_encoding = face_recognition.face_encodings(unknown_image)[0]

            # results = face_recognition.api.compare_faces(
            #     [image1_encoding], image2_encoding, tolerance=0.4)

            # if(os.path.exists(f"{name}.jpg")):
            #     os.remove(f"{name}.jpg")

            # cam.release()

            # cv2.destroyAllWindows()

        # except:
            # cam.release()
            # cv2.destroyAllWindows()
            # return Response({'results': 'User details does not match'}, 404)

        # Creating Token for the Logged in user.
        if (user_type == 'student'):

            try:
                user = student_models.objects.filter(email=email).first()
                print(str(user.image).split("/")[-1]) # type: ignore
                file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
                print("hello")
                for index, file in enumerate(file_list):
                    if(file['id'] == str(user.image).split("/")[-1]): # type: ignore
                        print(index+1,'file downloaded : ', file['title'])
                        file.GetContentFile(file['title'])
                known_image = face_recognition.load_image_file(f"{name}.jpg")
                unknown_image = face_recognition.load_image_file(image)
                image1_encoding = face_recognition.face_encodings(known_image)[0]
                image2_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.api.compare_faces([image1_encoding], image2_encoding, tolerance=0.4)

                if(os.path.exists(f"{name}.jpg")):  
                    os.remove(f"{name}.jpg")

                if user is None:
                    return Response({'Result': "User not found"})
                
                if results == [True]:
                    
                    payload = {
                        'id': user.pk,
                        'email': user.email,
                        'roll_no': user.roll_no,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        'iat': datetime.datetime.utcnow(),
                    }

                    token = jwt.encode(payload, 'secret', algorithm='HS256')
                    # return Response({'Result': results, 'Token': token})

                    serializer = Imageserializer(user)
                    return Response({
                        "status":True,
                        "message": "Successfully Logged in",
                        "user_data":serializer.data,
                        "token": token
                    })
                else:
                    return Response({"status":False, "Message":"Face does not match"})
            except:
                return Response({"status":False, "Error": "Details does not match"})
            
        elif (user_type == 'teacher'):

            try:
                user = teacher_models.objects.filter(email=email).first()
                file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
                for index, file in enumerate(file_list):
                    if(file['id'] == str(user.image).split("/")[-1]): # type: ignore
                        print(index+1,'file downloaded : ', file['title'])
                        file.GetContentFile(file['title'])
                known_image = face_recognition.load_image_file(f"{name}.jpg")
                unknown_image = face_recognition.load_image_file(image)
                image1_encoding = face_recognition.face_encodings(known_image)[0]
                image2_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.api.compare_faces([image1_encoding], image2_encoding, tolerance=0.4)

                if(os.path.exists(f"{name}.jpg")):
                    os.remove(f"{name}.jpg")

                if user is None:
                    return Response({'Result': "User not found"})
                
                if results == [True]:  
                    

                    payload = {
                            'id': user.pk,
                            'email': user.email,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                            'iat': datetime.datetime.utcnow(),
                        }

                    token = jwt.encode(payload, 'secret', algorithm='HS256')

                    # return Response({'Result': results, 'Token': token})
                    print("Hello")
                    serializer = teacherserializer(user)
                    return Response({
                            "status":True,
                            "message": "Successfully Logged in",
                            "user_data":serializer.data,
                            "token": token
                        })
                else:
                    return Response({"status":False, "Message":"Face does not match"})
            except:
                return Response({"status":False, "Error": "Details does not match"})
            
        else:
            return Response({"status":False, "Error": "Please provide a valid user type"})



@api_view(['POST'])
# Use for login via username and password
def login(request):
    try:
        if (request.data['user_type'] == "student"):
            try:
                roll_no = request.data['roll_no']
                password = request.data['password']
            except:
                return Response({"status":False,"msg":"Please provide all the details"})
            user = student_models.objects.filter(roll_no=roll_no).first()
            response = loginlogic(password, user)
            return response

        if (request.data['user_type'] == "teacher"):
            try:
                email = request.data['email']
                password = request.data['password']
            except:
                return Response({"status":False,"msg":"Please provide all the details"})
            user = teacher_models.objects.filter(email=email).first()
            response = loginlogic(password, user)
            return response
        else:
            return Response({"status":False,"msg":"Please provide a valid user type"})
    except:
        return Response({"status":False,"msg":"Some error occured"})


@api_view(['POST'])
# Use for registering the user image with user details in the database.
def Register(request):

    if request.method == 'POST':
        try:
            user = request.query_params['user']
            if (user == "admin"):
                try:
                    if (request.data['user_type'] == "student"):
                        serializer = Imageserializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            name = serializer.data['name']
                            email = serializer.data['email']
                            roll_no = serializer.data['roll_no']
                            password = serializer.data['password']
                            user_type = serializer.data['user_type']
                            # sendMail(user_type, name, roll_no, password, email)
                            return Response({"status": True, "data": serializer.data})
                        return Response({"status":False,"error":serializer.errors})

                    if (request.data['user_type'] == "teacher"):
                        serializer = teacherserializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            name = serializer.data['name']
                            email = serializer.data['email']
                            password = serializer.data['password']
                            user_type = serializer.data['user_type']
                            print(serializer.data['user_type'])
                            # sendMail(user_type, name, email, password)
                            return Response({"status": True,"data": serializer.data})
                        return Response({"status":False,"error":serializer.errors})
                    else:
                        return Response({"status":False,"msg": "Please select the usertype first"})
                except:
                    return Response({"status":False,"msg": "Some error occured"})
            else:
                return Response({"status":False, "msg": "You are not allowed to register"})
        except:
            return Response({"status":False, "msg": "Please select the usertype first"})


@api_view(['POST', 'PUT', 'PATCH'])
# Use for updating the existing student model
def update(request):
    if request.method == 'PUT':
        try:
            token = request.headers["token"]
            if not token:
                return Response({"error": "User not authenticated"}, 401)

            data = ""
            try:
                if (request.data['user_type'] == "student"):
                    payload = jwt.decode(
                        token, 'secret', algorithms=['HS256'])
                    data = student_models.objects.get(
                        email=payload['email'])
                    data.status = "true"
                if (request.data['user_type'] == "teacher"):
                    payload = jwt.decode(
                        token, 'secret', algorithms=['HS256'])
                    data = teacher_models.objects.get(
                        email=payload['email'])
                    data.status = "true"
            except:
                return Response({
                    "status":False,
                    "Error": "User with this email does not exist"
                })
            if (request.data['user_type'] == "student"):
                serializer = Imageserializer(
                data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    name = serializer.data['name']
                    email = serializer.data['email']
                    user_type = serializer.data['user_type']
                    saveImage(name)
                    rename_image(user_type,email,name)
                    return Response({"status":True,"user_data":serializer.data})
                return Response({"status":False,"error":serializer.errors})
            if(request.data['user_type'] == "teacher"):
                serializer = teacherserializer(
                data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    name = serializer.data['name']
                    email = serializer.data['email']
                    user_type = serializer.data['user_type']
                    saveImage(name)
                    rename_image(user_type,email,name)
                    return Response({"status":True,"user_data":serializer.data})
                return Response({"status":False,"error":serializer.errors})
            return Response()
        
        except:
            return Response({"status":False,"msg": "Some error occured"})


@api_view(['POST','GET'])
# Use for viewing the data of registered user
def view(request):

    if request.method == 'GET':

        try:

            token = request.headers['token']
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            try :
                data = student_models.objects.get(roll_no=payload['roll_no'])
                serializer = Imageserializer(data)
                return Response({"status":True,"user_data":serializer.data})
            
            except:
                data = teacher_models.objects.get(email=payload['email'])
                serializer = teacherserializer(data)
                return Response({"status":True,"user_data":serializer.data})
            
        except:
            
            return Response({"status":False,"msg":"Some error occured"})

    if request.method == 'POST':

        if (request.data):

            try:
                id = request.data['id']
                user_type = request.data['user_type']

            except:
                return Response({"status":False,"Error": "Please provide all the details"})

            if (user_type == 'student'):
                if id != None:
                    try:
                        data = student_models.objects.get(id=id)
                    except:
                        return Response({
                            "status":False,
                            "Error": "User with this id does not exist"
                        }, 404)
                    serializer = Imageserializer(data)
                    return Response({"status":True,"data":serializer.data}, 200)
            elif (user_type == 'teacher'):

                if id != None:
                    try:
                        data = teacher_models.objects.get(id=id)
                    except:
                        return Response({
                            "status":False,
                            "Error": "User with this id does not exist"
                        }, 404)
                    serializer = Imageserializer(data)
                    return Response({"status":True,"data":serializer.data}, 200)
            else:
                return Response({"status":False,"Error": "Please provide valid user_type"})
        else:
            data = student_models.objects.all()
            serializer = Imageserializer(data, many=True)
            Total_Records = len(serializer.data)
            return Response({"status":True,"records": serializer.data, "Total records": Total_Records}, 200)
