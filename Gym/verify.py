#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import mysql.connector
import os
#forms connection with the server.
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
    )
cursor = conn.cursor()
print("Content-type: text/html\n") 



# Gets the path info from the environment
path_info = os.environ.get("PATH_INFO", "") #PATH_INFO contains the url the user went through. This gets the url.

# Splits the path into components
path_components = path_info.split("/") #splits url based on "/"

# The last component is the token
if len(path_components) > 1: #checks if it was split
    token = path_components[-1] #gets last sublist which is the token as it was put in the last position in the verify link in index.py

Query="select EmailToken from user where EmailToken='"+token+"'" #query selecting emailtoken which matches the generated one
cursor.execute(Query) #executes the query
result=cursor.fetchall() #assigns result the value of the token from the database
if result:
    print("User Verified") #if the token is in the database it will print user verified
    Query="Update user set IsVerified=1 where EmailToken='"+token+"'" #query to update the value of ISverified to 1 if user is verified
    cursor.execute(Query)
    conn.commit()
    

        
else:
    print("Error Invalid user")
