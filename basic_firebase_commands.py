from firebase import Firebase

config = {
  "apiKey": "AIzaSyArL9WuBVYY04Nmt519xi08wnF6muZDIao",
  "authDomain": "skin-cancer-detection-e1c4c.firebaseapp.com",
  "databaseURL": "https://skin-cancer-detection-e1c4c.firebaseio.com",
  "projectId": "skin-cancer-detection-e1c4c",
  "storageBucket": "skin-cancer-detection-e1c4c.appspot.com",
  "serviceAccount": "skin-cancer-detection-e1c4c-firebase-adminsdk-ssryp-79ea70418c.json"
}

firebase = Firebase(config)
# firebase = pyrebase.initialize_app(config)

db = firebase.database()
# data = {"name": "Joe Tilsed"}
# # db.child("users").child("Joe").set(data)
# db.child("users").child("Joe").update({"name": "Joe W Tilsed"})
# db.child("users").child("Shyam").update({"name": "Shyam Mittal"})
# data2 = {
#     "users/Shyamm":{
#         "name" : "Shyam Mittal Ji"
#     }
# }
# dic = {}
# dic = dict(db.child("users").get().val())
# print(len(dic))
# print("Shyam" in dic)
# print(dic.keys())
users = dict(db.child("users").get().val())
user1 = users["nobi1008"]
db.child("users").child("nobi1008").remove()
print(user1)
del user1["tokenId"]
del user1["time-stamp"]
print(user1)
db.child("users").child("nobi1008").update(user1)
# storage = firebase.storage()
# as admin
# storage.child("something2.png").put("pic.jpeg")
# storage.child("something.png").download("downloaded1.png")