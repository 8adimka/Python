curl -X GET "http://localhost:5000/users/"

curl -X POST "http://localhost:5000/users/" -H "Content-Type:application/json" -d '{"username":"Admin", "password":"123", "role":"admin"}'

curl -X POST "http://localhost:5000/auth/" -H "Content-Type:application/json" -d '{"username":"Admin", "password":"123"}'
curl -X PUT "http://localhost:5000/auth/" -H "Content-Type:application/json" -d '{"refresh_token":"<JW_Token>"}'

curl -X DELETE "http://localhost:5000/users/2" -H "Content-Type:application/json" -H "Authorization:Bearer <JW_token>"