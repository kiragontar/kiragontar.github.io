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
token = C.get("token").value if "token" in C else None
navigation="""
    <nav>
      <label class="logo"> POWERZONE </label>
      <ul>
          <li><a href="mainpage.py"> Home </a></li>
          <li><a href="login.py"> Log In </a></li>
          <li><a href="Chatbot.html">Chatbot</a></li>
      </ul>
    </nav>
    """

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
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title> Power Zone</title>
  <link href="style_p_z.css" rel="stylesheet" type="text/css" />
</head>
  <style>
    .img {{
      width: 100%;
      height: 25%;
    }}
  </style>

<body>

{navigation}


   
  <div class="container">
    <div class="box">
      <span>  </span>
      <div class="content">
        <h2>Swimming Pool</h2>
        <p>Immerse yourself in luxury at our gym's pristine swimming pool. Encircled by lush greenery, the pool offers a serene escape from your workout routine. Dive into refreshing azure waters, surrounded by elegant mosaic tiles.</p>
      </div>
    </div>
    <div class="box">
      <span></span>
      <div class="content">
        <h2>Physiotherapy</h2>
        <p>Discover tranquillity in the peaceful setting of our physiotherapy clinic. Enjoy recuperating among beautiful vegetation and stylish design. Sink into relaxation on sun-drenched loungers as you begin your therapeutic journey with us.</p>
      </div>
    </div>
    <div class="box">
      <span></span>
      <div class="content">
        <h2>Massage</h2>
        <p>Step into our massage sanctuary, where relaxation awaits amidst serene surroundings. Let skilled hands melt away tension, while soothing aromas envelop you in tranquility. Experience blissful rejuvenation with each tailored session, nurturing your body and soul.</p>
      </div>
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

</html>


""")