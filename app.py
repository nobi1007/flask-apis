from flask import Flask, render_template, request, jsonify, abort
from firebase import Firebase
from random import randint
from datetime import datetime

#added some more libs
import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import  ImageDataGenerator,img_to_array

# import base64
literals = "ABCDDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*=':;,.+-"
def get_token():
    mixed_literals = ""
    lower_limit = 0
    upper_limit = len(literals)
    happend = set()
    while len(happend) < upper_limit:
        arbi_pos = randint(lower_limit,upper_limit-1)
        if arbi_pos not in happend:
            happend.add(arbi_pos)
            mixed_literals += literals[arbi_pos]
    
    token_literal_pos = []
    while len(token_literal_pos) < 23:
        temp_pos = randint(lower_limit,upper_limit-1)
        if temp_pos not in token_literal_pos:
            token_literal_pos.append(temp_pos)
    token = ""
    for i in token_literal_pos:
        token += mixed_literals[i]
    return token

def checkTime(d1,d2):
    t = d2-d1
    t_val = int(t.total_seconds())
    if t_val > 10800: # three hours = 10800 sec
        return False
    return True
"""
def ml_predict(image):
    pass"""
#################################################################################################################
# def get_model():
#     global model
#     print("Loading MobileNet Model...")
#     model=load_model('model_good_testing_Acc_84.h5')
#     print(model)
#     print("Model Loaded!")
# def preprocess_image(image,target_size):
#     if image.mode!="RGB":
#         image=imae.convert("RGB")
#     image=image.resize(target_size)
#     image=img_to_array(image)
#     image=np.expand_dims(image,axis=0)
#     image = np.vstack([image])
#     print(image)
#     return image
# get_model()
# @app.route("/")
# def startWeb():
#     return render_template('predict.html')
# @app.route("/predict",methods=["POST"])
# def predict():
#     message=request.get_json(force=True)
#     encoded=message['image']
#     decoded=base64.b64decode(encoded)
#     image=Image.open(io.BytesIO(decoded))
#     processed_image=preprocess_image(image,target_size=(224,224))
#     print(model)
#     graph = tf.get_default_graph()
#     print(model)
#     with graph.as_default():
#         prediction=model.predict(processed_image)
#         print(prediction)
#     response={
#         'prediction':{
#             'akiec':str(prediction[0][0]),
#             'bcc':str(prediction[0][1]),
#             'bkl':str(prediction[0][2]),
#             'df':str(prediction[0][3]),
#             'mel':str(prediction[0][4]),
#             'nv':str(prediction[0][5]),
#             'vasc':str(prediction[0][6]),
#     }}
#     return jsonify(response)
################################################################################################################
config = {
  "apiKey": "AIzaSyArL9WuBVYY04Nmt519xi08wnF6muZDIao",
  "authDomain": "skin-cancer-detection-e1c4c.firebaseapp.com",
  "databaseURL": "https://skin-cancer-detection-e1c4c.firebaseio.com",
  "projectId": "skin-cancer-detection-e1c4c",
  "storageBucket": "skin-cancer-detection-e1c4c.appspot.com",
  "serviceAccount": "skin-cancer-detection-e1c4c-firebase-adminsdk-ssryp-79ea70418c.json"
}

firebase = Firebase(config)
db = firebase.database()
storage = firebase.storage()

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def landing():
    return render_template("landing.html")
 
@app.route("/predict",methods=["GET"])
def prediction():
    return render_template("prediction_main.html")


@app.route("/api/register",methods=["POST"])
def registration():
    predict_reqest = request.get_json()
    if predict_reqest:
        new_user = predict_reqest["user"]
        new_user_id = new_user["user-id"]
        print(new_user["email-id"])
        # print()
        all_users = dict(db.child("users").get().val())
        
        check = True
        if new_user_id not in all_users:
            for user in list(all_users.keys()):
                if "email-id" in list(all_users[user].keys()):
                    if all_users[user]["email-id"] == new_user["email-id"]:
                        check = False
                        break
            if check:
                db.child("users").child(new_user_id).update(new_user)
                response = {"status":"Success","message":f"User with username {new_user_id} registered, now you may login."}
                return jsonify(response)
            else:
                response = {"status":"Failed","message":"Invalid Request - email already registered"}
                return jsonify(response)
        else:
            response = {"status":"Failed","message":"Invalid Request - User Id is already registered"}
            return jsonify(response)
    else:
        print(predict_reqest)
        return render_template("404.html")


@app.route("/api/getusers/<username>",methods=["GET"])
def user_details(username):
    all_users = dict(db.child("users").get().val())
    response = {}
    print(all_users.keys())
    if username in all_users.keys():
        op_user = all_users[username]
        response["Status"] = "Success"
        response["first-name"] = op_user["first-name"]
        response["last-name"] = op_user["last-name"]
        response["user-id"] = op_user["user-id"]
        response["email-id"] = op_user["email-id"]
        response["age"] = op_user["age"]
        response["mobile-number"] = op_user["mobile-number"]
        response["gender"] = op_user["gender"]
        return jsonify(response)
    else:
        response["Status"] = "Failed"
        response["Message"] = "Requested user not found"
        return jsonify(response)


@app.route("/api/login",methods=["POST"])
def logging_in():
    all_users = dict(db.child("users").get().val())
    datetime_format = "%y-%m-%d %H:%M:%S"

    input_creds = request.get_json()

    if input_creds:
        if input_creds['user-id'] in all_users.keys():
            temp = all_users[input_creds['user-id']]
            if input_creds["user-id"]==temp["user-id"] and input_creds["password"] == temp["password"]:
                if "time-stamp" in temp.keys():
                    current_time = datetime.today()
                    
                    saved_time_string = temp["time-stamp"]
                    saved_time = datetime.strptime(saved_time_string,datetime_format)

                    is_logged_in = checkTime(saved_time,current_time)
                    if is_logged_in:
                        response = {"status":"Success","message":"User is already logged in"}
                        return jsonify(response)
                    else:
                        current_time_string = current_time.strftime(datetime_format)
                        tokenId = get_token()
                        response = {"status":"Success","tokenId":tokenId,"message":"tokenId will be refreshed in every three hours"}
                        db.child("users").child(input_creds["user-id"]).update({"tokenId":tokenId,"time-stamp":current_time_string})
                        return jsonify(response)    # the auth token recieved here has to be saved in shared preference.
                else:
                    current_time = datetime.today()
                    current_time_string = current_time.strftime(datetime_format)
                    tokenId = get_token()
                    response = {"status":"Success","tokenId":tokenId,"message":"tokenId will be refreshed in every three hours"}
                    db.child("users").child(input_creds["user-id"]).update({"tokenId":tokenId,"time-stamp":current_time_string})
                    return jsonify(response)    # the auth token recieved here has to be saved in shared preference.
            else:
                response = {"status":"Failed","message":"Either user-id or password is incorrect"}
                return jsonify(response)    
        else:
            response = {"status":"Failed","message":"User is not registered"}
            return jsonify(response)
    else:
        # print(predict_reqest)
        response = {"status":"Failed","message":"Invalid Request"}
        return jsonify(response)

@app.route("/api/logout",methods=["POST"])
def logging_out():
    all_users = dict(db.child("users").get().val())
    datetime_format = "%y-%m-%d %H:%M:%S"
    input_creds = request.get_json()
    if "user-id" in input_creds and "tokenId" in input_creds:
        if input_creds['user-id'] in all_users.keys():
            temp = all_users[input_creds['user-id']]
            if input_creds["user-id"]==temp["user-id"]:
                if "tokenId" in temp.keys() and temp["tokenId"] == input_creds["tokenId"]:                  
                    current_time = datetime.today()
                    saved_time_string = temp["time-stamp"]
                    saved_time = datetime.strptime(saved_time_string,datetime_format)
                    is_logged_in = checkTime(saved_time,current_time)

                    if is_logged_in:
                        response = {"status":"Success","message":"User has been logged out."}
                        current_user = all_users[input_creds["user-id"]]
                        db.child("users").child(current_user["user-id"]).remove()
                        del current_user["tokenId"]
                        del current_user["time-stamp"]                        
                        db.child("users").child(current_user["user-id"]).update(current_user)
                        return jsonify(response)
                    else:
                        response = {"status":"Failed","message":"User is not currently logged in"}
                        return jsonify(response)  
                else:
                    response = {"status":"Failed","message":"User is not currently logged in"}
                    return jsonify(response) 
            else:
                response = {"status":"Failed","message":"Invalid User-Id"}
                return jsonify(response)    
        else:
            response = {"status":"Failed","message":"User is not registered"}
            return jsonify(response)
    else:
        response = {"status":"Failed","message":"Invalid Request"}
        return jsonify(response)


@app.route("/api/predict",methods=["POST"])
def prediction_api():
    all_users = dict(db.child("users").get().val())
    datetime_format = "%y-%m-%d %H:%M:%S"
    current_time = datetime.today()
    current_time_string = current_time.strftime(datetime_format)

    predict_reqest = request.get_json()
    if predict_reqest and "user-id" in predict_reqest and "tokenId" in predict_reqest and "image-data" in predict_reqest and "user-name" in predict_reqest:
        user_id = predict_reqest["user-id"]
        image_data = predict_reqest["image-data"]
        time_stamp = current_time_string
        user_name = predict_reqest["user-name"]
        tokenId = predict_reqest["tokenId"]
        # output = ml_predict(image_data)
        if user_id in all_users:
            current_user = all_users[user_id]
            if "tokenId" in current_user and current_user["tokenId"]==tokenId:
                # output = ml_predict(image_data)
                json_response = {
                    "results" : {
                        "val1":1,
                        "val2":2,
                        "val3":3,
                        "val4":4,
                        "val5":5,
                    },
                    "status":"Success",
                    "message":"For the given image following are the results"
                }

                firebase_data = {
                    "user_name":user_name,
                    "image_data":image_data
                }
                db.child("Predictions").child(user_id).child(time_stamp).update(firebase_data)

                return jsonify(json_response)
            else:
                response = {"status":"Failed","message":"User not logged in or invalid token. Try logging in again"}
                return jsonify(response)
        else:
            response = {"status":"Failed","message":"User not found"}
            return jsonify(response)
    else:
        response = {"status":"Failed","message":"Invalid Request"}
        return jsonify(response)        

if __name__ == "__main__":
    app.run(port = 4568,debug=True)
