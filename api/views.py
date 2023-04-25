import cv2
import face_recognition
import os
import jwt
import datetime
import bcrypt
import smtplib
import shutil
import math

from rest_framework.decorators import api_view
from rest_framework.response import Response

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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
                                        <a href="https://connect-lms.netlify.app/" style="text-decoration: none;display: inline-block;min-width: 100px;text-align: center;padding: 10px 30px;margin: 30px auto;background-color: #1f74ca; color: white; border-radius: 10px; transition: all 0.3s ease;">Login</a>    
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
    
    print("Hello")
    app_password = os.environ.get('APP_PASSWORD')
    s.login("connect.lms.developers@gmail.com", app_password)

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
        return Response({"status":False,"msg": "Incorrect Username or Password"})

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
                        "msg": "Successfully Logged in",
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
                        "msg": "Successfully Logged in",
                        "user_data":serializer.data,
                        "token": token
                    })
            except:
                return Response({"status":False,"msg":"Error"})
        except:
            return Response({"status":False,"msg":"Some Error occured"})

def saveImage(name,email):
    directory = "media"
    arr1 = email.split("@")
    arr = name.split()
    name = "".join(arr)
    name = name.lower()
    email = arr1[0].lower()

    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
    
    for index, file in enumerate(file_list):

        if(file['title'].split(".")[0] == email):
            file.Delete()
        elif(file['title'].split(".")[0] == email+"profile"):
            file.Delete()
        else:
            continue

    for f in os.listdir(directory):
        if(f.split(".")[0]==email):
            filename = os.path.join(directory,f)
            gfile = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : f})
            gfile.SetContentFile(filename)
            gfile.Upload()
            print("Saveimage")
        elif(f.split(".")[0]==email+'profile'):
            filename = os.path.join(directory,f)
            gfile = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : f})
            gfile.SetContentFile(filename)
            gfile.Upload()
            print("saveprofile_image")

    shutil.rmtree('media', ignore_errors=False)
    return


def rename_image(user_type,email,name):
    arr1 = email.split("@")
    arr = name.split()
    name = "".join(arr)
    name = name.lower()
    eml = arr1[0].lower()
    print(eml)

    if(user_type == "student"):
        data = student_models.objects.get(email=email)
    else:
        data = teacher_models.objects.get(email=email)

    fid = ""
    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()

    for index, file in enumerate(file_list):

        if(file['title'].split(".")[0] == eml):
            print("Renamed image")
            fid = file['id']
            data.image = f"https://drive.google.com/uc?export=view&id={fid}" # type: ignore
            data.save()

        elif(file['title'].split(".")[0] == eml+"profile"):
            print("Renamed Profile image")
            fid = file['id']
            data.profile_image = f"https://drive.google.com/uc?export=view&id={fid}" # type: ignore
            data.save()
        else:
            continue
    return


def update_year(email,sem):
    data = student_models.objects.get(email=email)
    print("Hello")
    data.year = str(math.ceil(int(sem)/2))
    data.save()
    return

# Create your views here.
@api_view(['POST'])
# # For Comparing the image taken and the image stored in the database.
def facelogin(request):

    if request.method == 'POST':

        try:
            image = request.data['image']
            user_type = request.data['user_type']

            if(user_type=="student"):
                roll_no = request.data['roll_no']
            else:
                email = request.data['email']
                arr1 = email.split("@")
                eml = arr1[0]
            
        except:
            return Response({"status":False,"msg": "Please provide all the details"})


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
                user = student_models.objects.filter(roll_no=roll_no).first()

                arr1 = user.email.split("@")
                eml = arr1[0]
                
                if user is None:
                    return Response({"status":False, 'msg': "User not found"})
                
                file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
                for index, file in enumerate(file_list):
                    if(file['id'] == str(user.image).split("=")[-1]): # type: ignore
                        print(index+1,'file downloaded : ', file['title'])
                        file.GetContentFile(file['title'])
                known_image = face_recognition.load_image_file(f"{eml}.jpg")
                unknown_image = face_recognition.load_image_file(image)
                image1_encoding = face_recognition.face_encodings(known_image)[0]
                image2_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.api.compare_faces([image1_encoding], image2_encoding, tolerance=0.4)

                print(results)

                if(os.path.exists(f"{eml}.jpg")):
                    os.remove(f"{eml}.jpg")
                
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
                        "msg": "Successfully Logged in",
                        "user_data":serializer.data,
                        "token": token
                    })
                else:
                    return Response({"status":False, "msg":"Face does not match"})
            except:
                return Response({"status":False, "msg": "Details does not match"})
            
        elif (user_type == 'teacher'):

            try:
                user = teacher_models.objects.filter(email=email).first()

                if user is None:
                    return Response({"status":False, 'msg': "User not found"})
                
                file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
                for index, file in enumerate(file_list):
                    if(file['id'] == str(user.image).split("=")[-1]): # type: ignore
                        print(index+1,'file downloaded : ', file['title'])
                        file.GetContentFile(file['title'])
                print("Hello")
                known_image = face_recognition.load_image_file(f"{eml}.jpg")
                unknown_image = face_recognition.load_image_file(image)
                image1_encoding = face_recognition.face_encodings(known_image)[0]
                image2_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.api.compare_faces([image1_encoding], image2_encoding, tolerance=0.4)

                if(os.path.exists(f"{eml}.jpg")):
                    os.remove(f"{eml}.jpg")
                
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
                            "msg": "Successfully Logged in",
                            "user_data":serializer.data,
                            "token": token
                        })
                else:
                    return Response({"status":False, "msg":"Face does not match"})
            except:
                return Response({"status":False, "msg": "Details does not match"})
            
        else:
            return Response({"status":False, "msg": "Please provide a valid user type"})



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

        if (request.data['user_type'] == "teacher" or request.data['user_type'] == "admin"):
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
                            sendMail(user_type, name, roll_no, password, email)
                            return Response({"status": True, "data": serializer.data})
                        return Response({"status":False,"error":serializer.errors})

                    if (request.data['user_type'] == "teacher" or request.data['user_type'] == "admin"):
                        serializer = teacherserializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            name = serializer.data['name']
                            email = serializer.data['email']
                            password = serializer.data['password']
                            user_type = serializer.data['user_type']
                            print("Hello")
                            try:
                                sendMail(user_type, name, email, password)
                            except:
                                email = serializer.data['email']
                                print(email)
                                data = teacher_models.objects.get(email=email)
                                data.delete()
                                return Response({"status":False,"msg":"Please enter valid email"})
                            
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
                    data.status = True
                if (request.data['user_type'] == "teacher" or request.data['user_type'] == "admin"):
                    payload = jwt.decode(
                        token, 'secret', algorithms=['HS256'])
                    data = teacher_models.objects.get(
                        email=payload['email'])
                    data.status = True
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
                    sem = serializer.data['semester']
                    update_year(email,sem)
                    try:
                        if(request.data['image']):
                            saveImage(name,email)
                            rename_image(user_type,email,name)
                    except:
                        return Response({"status":True,"user_data":serializer.data})

                    return Response({"status":True,"user_data":serializer.data})
                    
                return Response({"status":False,"error":serializer.errors})
            
            if(request.data['user_type'] == "teacher" or request.data['user_type'] == "admin"):
                serializer = teacherserializer(
                data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    try:
                        if(request.data['image']):
                            name = serializer.data['name']
                            email = serializer.data['email']
                            user_type = serializer.data['user_type']
                            saveImage(name,email)
                            rename_image(user_type,email,name)
                    except:
                        return Response({"status":True,"user_data":serializer.data})

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
