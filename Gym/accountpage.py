#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import os
import mysql.connector
from http import cookies

#forms connection with server
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
)
cursor = conn.cursor()
C = cookies.SimpleCookie() #creates a simplecookie object and assigns it to C
C.load(os.environ.get("HTTP_COOKIE", ''))#loads cookies from HTTP request headers into the simpleCookies which is in "C".
#os.environ["HTTP_COOKIE"] retrieves value from the "HTTP_COOKIE" environment variable which is in the server side. 
#which contains the cookie data sent by the client in the HTTP request headers.
token = C.get("token").value if "token" in C else None #gets the value of the cookie token and assigns it to token, if cookie token is empty then token=None
form = cgi.FieldStorage()

if "action" in form and form.getvalue("action") == "logout": #checks if user clicks logout
    if token: #cookie token exists
        # Invalidate the token in the database
        update_query = "UPDATE user SET Token = NULL WHERE Token = %s"
        cursor.execute(update_query, (token,))
        conn.commit() #commits change making it permanent


        # If the logout action is triggered, clear the token
        C["token"] = "" #sets token to empty string effectively clearing it
        C["token"]["path"] = "/" #removes path of token
        C["token"]["max-age"] = 0 #expires token
    
        # Output the header to clear the cookie
        print(C.output())
        # Now, output the redirection header
        print("Location: login.py\n\n")
        print()
    else: #cookie token doesnt exist
        print("Content-type: text/html\n")
        print("<p>You have Already logged out.</p>")

else: #if user doesnt click logout
    print("Content-type: text/html\n")
    if token: #cookie token exists
        query="SELECT mID, FirstName, LastName, Email, PhoneNumber, DOB, Student FROM user WHERE token=%s " #selects user information from token
        cursor.execute(query,(token,))
        user_info=cursor.fetchone() #collects user info
        if user_info: # token exist in database and collected user info.
            mID, first_name, last_name, email, phone_number, dob, student_status=user_info #assigns each variable the variable from the database.
            if student_status=="1": #checks the student status and sets them to yes or no so user understands it better.
                student_status="Yes"
            else:
                student_status="No"
        
            print(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Account Page</title>
                <style>
                body{{
                    font-family: Facón;
                    margin:0;
                    padding:0;
                    color:#333;
                    background-color: #fff;
                }}
                .title{{
                    text-align: center;
                }}
                .container{{
                    display: flex;
                    flex-direction: column;
                    align-items:center;
                    justify-content: center;
                    width:100%;
                
                }}
                .userinfo{{
                    background-color: #f9f9f9;
                    padding:15px;
                    width:600px;
                    margin:20px auto;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                    list-style-type: none;
                
                }}
                .userinfo li{{
                    padding: 10px 0;
                    margin-top:20px;
                    margin-bottom:20px;
                    border-bottom: 1px solid #ddd;
                }}
                .userinfo li:last-child{{
                    border-bottom: none;
                }}
                .info-label{{
                    font-weight: bold;
                }}
                a{{
                    text-decoration:none;
                }}
        
                nav{{
                    background: #000000;
                    height: 80%;
                    padding:0 20px;
                }}
                
                label.logo{{
                    color: white;
                    font-size: 35px;
                    line-height: 80px;
                    padding: 0 100px;
                }}
                
                nav ul {{
                    float: right;
                    margin:0;
                }}
                
                nav ul li{{
                    display: inline-block;
                    line-height: 80px;
                    margin: 0 5px;
                    
                }}
                
                nav ul li a, .logout-button{{
                    color: white;
                    font-size: 17px;
                    border-radius:3px;
                    padding: 7px 13px;
                    text-transform: uppercase;
                }}
                .logout-button{{
                    background:gray;
                    border:none;
                    font-family: Facón;
                }}
                
                a.active, a:hover, logout-button:hover{{
                    background: #a1a1a1;
                    transition: .5s;
                }}
                </style>
            </head>
            <body>
                <nav>
                    <!-------------------------- Navigation Bar ------------------------>
                    <label class="logo">GSO LAGO</label>
                    <ul>
                    <li><a href="mainpage.py">Home</a></li>
                    <li><a href="membershiptype.html">Prices</a></li>
                    <li><a href="fortune_wheel.html">Rewards</a></li>
                    <li>
                        <form method="post">
                            <button type="submit" name="action" class="logout-button" value="logout">Log out</button>
                        </form>
                    </li>
                    </ul>
                </nav>
                    <!--------------------------------------------------------------------->
                <div class="container">
                <h1 class="title">Account Details</h1>
                <ul class="userinfo">
                    <li><span class="info-label">Membership ID:</span>{mID}</li> 
                    <li><span class="info-label">First Name:</span>{first_name}</li>
                    <li><span class="info-label">Last Name:</span>{last_name}</li>
                    <li><span class="info-label">Email:</span>{email}</li>
                    <li><span class="info-label">Phone Number:</span>{phone_number}</li>
                    <li><span class="info-label">Date of Birth:</span>{dob}</li>
                    <li><span class="info-label">Student:</span>{student_status}</li>
                </ul>
                </div>
            </body>
            </html>
            """)
    
        else: #if results werent collected:
            print("Invalid Session. Please Log in again.")
    else:#if cookie token doesnt exist.
        print("Invalid Session. Please Log in again.")

