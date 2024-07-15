#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import smtplib #has functions to interact with an simple mail transfer protocol (SMTP) server to send emails
from email.mime.text import MIMEText #MIMEText class is used to create email message objects that contain plain text content.
#MIME (Multipurpose Internet Mail Extensions), its a standard to format non-ASCII messages so that they can be sent over the internet
#MIMEText provides methods to set text content, character encoding and other attributes of the email.
from email.mime.multipart import MIMEMultipart #MIMEMultipart class creates email message objects that contains parts such as plain text, html attachments.
import mysql.connector
import secrets #generates strong random hexadecimal strings here which is suitable for tokens 

print("Content-type: text/html\n")
#forms connection to the server
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
    )
cursor = conn.cursor()

def generate_token(length=32):  #function to generate random tokens 
    return secrets.token_hex(length // 2) #generates random string of hexadecimal digits. Each hexadecimal character represents half a byte so 2 characters represent a byte
    #so to convert the length into bytes it is divided by 2 which is the number of characters that make up a byte.
    #The length in bytes is then sent to secrets.token_hex() which generates a random hexadecimal string of the specified length in bytes 
    #converts length of token from number of characters to number of bytes
    #if you enter no length in the paramter and just enter 16 in the parameter> secrets.token_hex(16) it will generate 16bytes but 32 hexadecimal character.
token=generate_token()


def send_email(sender_email, receiver_email, subject, smtp_server, smtp_port, smtp_username, smtp_password): #function to send an email

# Creates the MIME object
    message = MIMEMultipart() #creates a MIME object and assigns it to message. MIME is a standard format for email messages that contain different contents such as html, text and attachments.
    message["From"] = sender_email #specifies the sender's email address.
    message["To"] = receiver_email #specifies the recipient's email address.
    message["Subject"] = subject #specifies the subject of the email.

    # Attaches the email body to the message.
    message.attach(MIMEText(emailhtml, "html")) #creates a text part with HTML content , emailhtml contains the HTML content of the email

    # This establishes a connection to the SMTP server specifies by smtp_server and smtp_port
    with smtplib.SMTP(smtp_server, smtp_port) as server: #tls (Transport layer security)
        # Starts tls for secure communication between python script and smtp server
        server.starttls() #starts a TLS connection for secure communication between python scirpt and smtp server, as TLS encrypts data exchanged between python script and server.
        # Logs in to the email account associated with the smtp server
        server.login(smtp_username, smtp_password)       
        # Sends the email
        server.sendmail(sender_email, receiver_email, message.as_string()) #specifies the sender's email and receiver's email address, as well converts the message into a string
    

aftersubmit="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Recovery</title>
    </head>
    <body>
        <h1>Email Sent!</h1>
        <h2>Please Check Your email and follow the guidance on the email</h2>
        <p>Please click <a href="login.py">here</a> to return back to the login page to login with your new password.</p>
    </body>
    </html>
    """
def display_wrong_email(error_msg=""): #function to display to user a page that they have entered a wrong email
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Forgot Password</title>
    <style>
        body{{
            margin: 0;
            height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            display: flex;
            align-items: center; /* Aligns vertically */
            justify-content: center; /* Aligns horizontally */
            background-color: #f7f7f7; /* Just an example background color */
        }}
        h2{{
            font-size: 22px;
            margin-bottom: 10px; /* Adds some space below the header */
        }}


        .box{{
        border: 1px solid #ccc;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Optional: adds a subtle shadow to your box */
        }}
        .inputbox{{
            width: 90%;
            padding:10px;
            margin-bottom: 20px; /* Adds some space below the input field */
            border: 1px solid #ddd; /* Sets border color */
            border-radius: 4px; 
        }}
        .cancel{{
            display: inline-block;
            font-size: 16px;
            text-align: center;
            padding: 10px 20px;
            text-decoration: none;
            border: 2px solid;
            margin-right: 10px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .submit{{
            display: inline-block;
            font-size: 16px;
            text-align: center;
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }}
        .cancel:hover{{
            background-color: #d3d3d3;
        }}
        .cancel:visited{{
            color: black;
        }}
        .submit:hover{{
            opacity: 0.9;
        }}
        
    </style>
    </head>
    <body>
        <div class="box">
            {f'<div style="color: red;">{error_msg}</div>' if error_msg else ''}
            <form action="passwordforget.py" method="post">
                <h2>Forgot Your Password?</h2>
                <p>Please enter your email address to reset your password</p>
                <input type="text" name="email" class="inputbox" required pattern="[^@\s]+@[^@\s]+\.[^@\s]+" placeholder="Email address" title="Enter a valid email address">
                <a href="login.py" class="cancel">Cancel</a>
                <button type="submit" class="submit">Submit</button>
            </form>
            
        </div>
    </body>
    </html>
    """)

emailhtml=f"""  
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Password Reset</title>
    <style>
    body {{
        text-align: center;      /*centeres the body text*/
    }}
    h1, h2 {{
        font-weight: bold;       /*Makes the heading bold and colored*/
    }}
    .Reset-button {{
        display: inline-block;   /*Makes the button an inline block allowing it to have dimensions and padding*/
        padding: 10px 20px;      /*sets space between content of button and its borders*/
        font-size: 16px;         /* Controls font size of contents*/
        text-align: center;      /*Makes the Content text centered*/
        text-decoration: none;   /*Makes it so that the button isnt underlined or anything*/
        border: 2px solid #663399; /*Makes the border thicker with a color*/
        color: black;            /*Makes the color of the contents black*/
        border-radius: 5px;      /*makes the borders corners rounded*/
        transition: background-color 0.3s ease; /*Changes color of background in the duration of 0.3 seconds when
                                hovered on the button*/
    }}
    .Reset-button:hover {{
        cursor: pointer;        /*Makes the mouse cursor change to a pointer when hovered on the button*/
        background-color: #663399; /*Makes the background color change when hovered on*/
        color: #fff;            /*Makes content color change when hovered on*/
    }}
    </style>
    </head>
    <body>
    <h1>Reset your password</h1>
    <h2>Why have I received this email?</h2>
    <p>You have received this email because someone has used the Forgotten password on the Gym website and entered your email address. If you did not request a password reset, please ignore this email.</p>
    <p><strong>If you have used the Forgotten password then please click on the button below to reset your password.</strong></p>
    <a class="Reset-button" href='http://localhost/webprog/Gym/passwordreset.py?token={token}'>Reset Password</a>
    <p>If you have any questions, contact our support team at Support@gym.com</p>
    </body>
    </html>
    """ #the token in {} is used to take them to the website but with a token at the end of it so that we can retrieve it and use it for verification





form = cgi.FieldStorage()
email=form.getvalue('email') #retrieves email user inputted
if email: #checks if user inputted an email
    emailindatabase="SELECT * FROM user where Email=%s" #checks if email is linked with an account
    cursor.execute(emailindatabase,(email,)) 
    user_data=cursor.fetchone() #retrieves result to check if email is linked
    if user_data: #email is in database:
        send_email("mickelgerges1@gmail.com",email,"Forgot Password","sandbox.smtp.mailtrap.io",2525,"52dddb5b4f6b2c","251e868964e025") #sends an email to reset the password
        updateQuery="UPDATE user SET PasswordToken =%s WHERE Email=%s" # updates passwordtoken with a token to use for verification
        cursor.execute(updateQuery,(token, email))
        conn.commit() # makes change permanent
        print(aftersubmit) #prints html page
    else: #if email is not linked
        display_wrong_email("It seems like the email you have submitted does not link to any created accounts") #calls function with error















