#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import os
import mysql.connector
from http import cookies

conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
)
cursor = conn.cursor()
print("Content-type: text/html\n")
C = cookies.SimpleCookie()
C.load(os.environ.get("HTTP_COOKIE", ''))

navigation="""
    <nav>
      <label class="logo"> U GYM </label>
      <ul>
          <li><a href="mainpage.py"> Home </a></li>
          <li><a href="login.py"> Log In </a></li>
          <li><a href="Chatbot.html">Chatbot</a></li>
      </ul>
    </nav>
    """
token = C.get("token").value if "token" in C else None


if token:
  query="SELECT * FROM user WHERE Token=%s"
  cursor.execute(query,(token,))
  user_logged_in=cursor.fetchone()
  if user_logged_in:
    navigation="""
    <nav>
        <label class="logo">GSO LAGO</label>
        <ul>
            <li><a href="mainpage.py">Home</a></li>
            <li><a href="membershiptype.html">Prices</a></li>
            <li><a href="accountpage.py">Account</a></li>
        </ul>
    </nav>
    """



print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uclasses</title>
    <style>

*{{
    padding: 0;
    margin:0;
    text-decoration: none;
    list-style: none;
  }}
  
  body {{
    font-family: Facón;
    background: #ffffff
  }}
  
  nav{{
    background: #000000;
    height: 80%;
    width:auto;
    margin-bottom: 50px;
  }}
  
  label.logo{{
    color: white;
    font-size: 35px;
    line-height: 80px;
    padding: 0 100px;
    /* font-height: bold; */
  
  }}
  
  nav ul {{
    float: right;
    margin-right: 20px;
  }}
  
  nav ul li{{
    display: inline-block;
    line-height: 80px;
    margin: 0 5px;
  }}
  
  nav ul li a{{
    color: white;
    font-size: 17px;
    border-radius:3px;
    padding: 7px 13px;
    text-transform: uppercase;
  }}
  
  a.active, a:hover{{
    background: #a1a1a1;
    transition: .5s;
  }}
            
  .container {{
    max-width: 12000px;
    margin: 0 auto;
    padding: 20px;
    margin-bottom: 70px;
    
                
  }}
  .classes-page {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    margin-top: 20px;
  }}
  .class-box {{
    width: 30%;
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    transition: all 0.3s ease;
    text-align: center;
  }}
  .class-box:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }}
  .class-box img {{
    width: 100%;
    border-radius: 5px;
    display:block;
    border: 2px black;
  }}
  .class-name {{
    margin-top: 10px;
    font-weight: bold;
  }}
  .class-description {{
    display: none;
    margin-top: 10px;
  }}
  .class-box:hover .class-description {{
    display: block;
  }}
  footer {{
    background-color: #333; 
    padding: 50px; /* Adjust padding as needed */
  }}
  .navigation {{
    list-style-type: none;
    padding: 0;
    text-align: right;
    margin-right: 30px;
  }}
  
  .navigation li {{
    display: inline-block;
    margin-left: 30px;
    font-family: Arial, Helvetica, sans-serif;
  }}
  
  .navigation li a {{
    text-decoration: none;
    color: #ffffff;
  
  }}
  
  .navigation li a:hover {{
    background-color: #dddddd57;
  }}
  
  
    </style>
</head>
<body>

  {navigation}

    <div class="container">
        <div class="classes-page">
            <div class="class-box">
                <img src="pictures/ugymmassage.jpg" alt="Massage">
                <p class="class-name">Umassage</p>
                <p class="class-description"> Recieve an unforgetable massage experience with our professionals.</p>
            </div>
            <div class="class-box">
                <img src="pictures/ugymswimming.jpg" alt="Swimming">
                <p class="class-name">USwimming</p>
                <p class="class-description">Learn swimming techniques in our state-of-the-art pool.</p>
            </div>

            <div class="class-box">
                <img src="pictures/physicugym.jpg" alt="physiotherapy">
                <p class="class-name">Uphysio</p>
                <p class="class-description">Learn physiotherapy techniques with our personal coach.</p>
            </div>
            <!-- Add more class boxes as needed -->
        </div>
    </div>
    <footer>

  <ul class="navigation">
    <li><a href="aboutus.html">About Us</a></li>
    <li><a href="contactus.html">Contact Us</a></li>
    <li><a href="privacy.html">Privacy Policy</a></li>
    <li><a href="FAQ.py">FAQ</a></li>
  </ul>

</footer>
</body>

</html>""")