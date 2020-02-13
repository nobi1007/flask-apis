A- Register

Request - 
{
    "user": {
        "user-id": "nobi1007",
        "first-name": "Shyam",
        "last-name": "Mittal",
        "email-id": "mittalshyam1007@yahoo.com",
        "password": "abc123456",
        "age": "21",
        "gender": "male",
        "mobile-number": "8707600139"
    }
}

Response -

Type 1 -
{
  "message": "Invalid Request - User Id is already registered",
  "status": "Failed"
}

Type 2 -
{
  "message": "Invalid Request - email already registered",
  "status": "Failed"
}

Type 3 -
{
  "message": "User with username nobi1008 registered, now you may login.",
  "status": "Success"
}



B- Login

Request -
{
	"user-id":"nobi1007",
	"password":"abc123456"
}

Response -

Type 1 -
{
  "message": "tokenId will be refreshed in every two hours.",
  "status": "Success",
  "tokenId": "qUr9p3aN^i1xVhM8vDFlILH"
}

Type 2 -
{
  "message": "User is not registered",
  "status": "Failed"
}

Type 3 -
{
  "message": "Either user-id or password is incorrect",
  "status": "Failed"
}



C- Get User Details

Request -

GET http://127.0.0.1:4568/api/getusers/nobi1007


Response - 

Type 1 -
{
  "Status": "Failed"
  "Message": "Requested user not found"
}


Type 2 -
{
  "Status": "Success",
  "age": "21",
  "email-id": "mittalshyam1007@yahoo.com",
  "first-name": "Shyam",
  "gender": "male",
  "last-name": "Mittal",
  "mobile-number": "8707600139",
  "user-id": "nobi1007"
}