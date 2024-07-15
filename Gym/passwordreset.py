#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import mysql.connector
#forms connection to server 
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
    )
cursor = conn.cursor()

print("Content-type: text/html\n")

form = cgi.FieldStorage()
token=form.getvalue('token') #retrieves token from url




Invalidlink="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invalid Reset Link</title>
</head>
<body>
    <h1>Invalid Link</h1>
    <p>The password reset link is invalid. Please try the reset process again if you need to reset your password.</p>
</body>
</html>
""" #html page to print if link is invalid (token may have expired)





if token:#if token exists/is valid
    Query="SELECT * FROM user where PasswordToken=%s" #verifies token
    cursor.execute(Query,(token,))
    userfound=cursor.fetchone()

    if userfound:#token is verified
        passwordreset=f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password</title>
            <style>
            body{{
                text-align:center;
            }}
            .title{{
                color: #333;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
                margin-top: 40px;
            }}
            .inputbox{{
                    width: 400px;
                    border: 1px solid #ccc;
                    padding:10px;
                    margin-top:30px;
                    margin-bottom:10px;
                    border-radius: 5px;
                }}
            .inputcontainer{{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }}
            

            </style>
        </head>
        <body>
            <h1 class="title">Reset Your Password</h1>
            <form action="passwordupdate.py" method="post">
            <div class="inputcontainer">
                <input type="hidden" name="token" value="{token}"> <!--This is hidden as user does not need to see it and is needed to pass it to other page-->
                <input type="password" name="new_password" id="new_password" class="inputbox" placeholder="Password" title="Password" required>
                <input type="password" id="confirm_password" name="confirm_password" class="inputbox" placeholder="Confirm Password" title="Confirm Password" required>
                <button type="submit" value="resetpassword">Reset Password</button>
            </div>
            </form>
        </body>
        </html>
        """

        print(passwordreset) #prints html page
    else: #token does not match:
        print(Invalidlink)
else: #token is not valid/ does not exist
    print(Invalidlink)
    