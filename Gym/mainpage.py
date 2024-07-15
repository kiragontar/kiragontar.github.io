#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import mysql.connector
import os
from http import cookies

conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
)
cursor = conn.cursor()
print("Content-type: text/html\n")

C = cookies.SimpleCookie() #creates a simplecookie object and assigns it to C
C.load(os.environ.get("HTTP_COOKIE", ''))#loads cookies from HTTP request headers into the simpleCookies which is in "C".
#os.environ["HTTP_COOKIE"] retrieves value from the "HTTP_COOKIE" environment variable which is in the server side. 
#which contains the cookie data sent by the client in the HTTP request headers.
token = C.get("token").value if "token" in C else None #gets the value of the cookie token and assigns it to token, if cookie token is empty then token=None.
navigation="""
        <nav>
        <label class="logo">GSO LAGO</label>
            <ul>
                <li><a href="Chatbot.html">Chatbot</a></li>
                <li><a href="login.py">Log In</a></li>
            </ul>
        </nav>
        """
#defines navigation with just the login page  and define getstartedwithus initially
getstartedwithus="""
        <button class="get-started-button" onclick="location.href='gym_form.html';">Get Started With Us</button>
        """
if token: #cookie token exists:
    query="SELECT * FROM user WHERE Token=%s" #verify token in database
    cursor.execute(query,(token,))
    user_logged_in=cursor.fetchone()
    if user_logged_in: #token verified:
        navigation="""
        <nav>
            <label class="logo">GSO LAGO</label>
            <ul>
                <li><a href="membershiptype.html">Prices</a></li>
                <li><a href="fortune_wheel.html">Rewards</a></li>
                <li><a href="accountpage.py">Account</a></li>
            </ul>
        </nav>
        """
        #define navigation with new pages as user logged in as cookie token exists
        getstartedwithus="" #remove getstartedwithus as user logged in

    
        


print(f"""
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Home</title>
  <link href="style_home_p.css" rel="stylesheet" type="text/css" />
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>

<body>
  {navigation}
  <!-- <div class="ads">
  <p> welcome to our gym use "welcome10" to get 10% off on ur first subscribtion</p>
  </div> -->
  <!--------------------------------------------------------------------->

  <center>
    {getstartedwithus}

    <div class="parent-container">
      <div class="container-1">
        <a href="u_gym.py"><img src="pictures/u-gym.jpg" alt="Image 1"></a>
        <h2>U GYM</h2>
      </div>

      <div class="container-2">
        <a href="power_zone.py"> <img src="pictures/p-z.png" alt="Image 2"></a>
        <h2>Power Zone</h2>
      </div>
    </div>
  </center>


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