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
C = cookies.SimpleCookie()
C.load(os.environ.get("HTTP_COOKIE", ''))
token = C.get("token").value if "token" in C else None 
question6="""
      <label for="acc6">
        <h2>06</h2>
        <h3>How can I become a member of UGYM or Power Zone at GSO Lago?</h3>
      </label>
      <div class="content">
        <p>
          You can sign up for membership online through our website. Simply visit our <a href="index.html"> page</a> and follow the instructions to select your preferred gym brand and membership plan. Membership options include various packages tailored to your needs.
        </p>
      </div>
      """
if token:
    query="SELECT * FROM user WHERE Token=%s"
    cursor.execute(query,(token,))
    user_logged_in=cursor.fetchone()
    if user_logged_in:
      question6=""

print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FAQ</title>
    <link rel="stylesheet" href="style FAQ.css">
</head>
<body>
  <div class="container">
    <h1>FAQ - Gym Membership and Facilities</h1>
    <div class="tab">
      <input type="radio" name="acc" id="acc1">
      <label for="acc1">
        <h2>01</h2>
        <h3> What is GSO Lago?</h3>
      </label>
      <div class="content">
        <p>GSO Lago is a fitness company offering two distinct gym brands: UGYM and Power Zone. Each brand provides unique fitness experiences tailored to different preferences and goals.</p>
      </div>
    </div>
    <div class="tab">
      <input type="radio" name="acc" id="acc2">
      <label for="acc2">
        <h2>02</h2>
        <h3>What amenities does each gym offer?</h3>
      </label>
      <div class="content">
        <p>
          Both gyms are equipped with state-of-the-art facilities to meet your fitness needs.
        </p>
      </div>
    </div>
    <div class="tab">
      <input type="radio" name="acc" id="acc3">
      <label for="acc3">
        <h2>03</h2>
        <h3>What are the membership fees for UGYM and Power Zone at GSO Lago?</h3>
      </label>
      <div class="content">
        <p>
          Membership fees vary depending on the gym brand and type of membership plan. You can view detailed pricing information and sign up for membership on our website.
        </p>
      </div>
    </div>
    <div class="tab">
      <input type="radio" name="acc" id="acc4">
      <label for="acc4">
        <h2>04</h2>
        <h3>What types of fitness classes are available at UGYM and Power Zone?</h3>
      </label>
      <div class="content">
        <p>
          UGYM offers a variety of classes including access to the swimming pool, massage therapy, and more. Whereas Power Zone specializes in physiotherapy, classes, and other specialized services. You can find the class schedules for both UGYM and Power Zone on our website.
        </p>
      </div>
    </div>
    <div class="tab">
      <input type="radio" name="acc" id="acc5">
      <label for="acc5">
        <h2>05</h2>
        <h3>Can I try UGYM or Power Zone before becoming a member at GSO Lago?</h3>
      </label>
      <div class="content">
        <p>
          No, trial passes or guest passes are not currently offered. However, you can explore all the details about our facilities, classes, and amenities on our website. Additionally, you can view images of our gyms to get a better understanding of what we offer.
        </p>
      </div>
    </div>
    <div class="tab">
      <input type="radio" name="acc" id="acc6">
      {question6}
    </div>
    <center>
    <div class="back-to-home">
      <a href="mainpage.py"> Back to Home page</a>
    </div>
  </center>
  </div>
</body>
</html>
""")