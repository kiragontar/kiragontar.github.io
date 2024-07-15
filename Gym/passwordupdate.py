#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import mysql.connector
import bcrypt #provides hashing, used here to hash the password enhancing security
#forms connection with server
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
    )
cursor = conn.cursor()
print("Content-type: text/html\n")

form = cgi.FieldStorage()
token=form.getvalue('token') #retrieves token from passwordreset.py so that we can know which password to update
new_password=form.getvalue('new_password') #retrieves new password added by user
confirm_password=form.getvalue('confirm_password') #retrieves the confirm password added by user

if new_password!=confirm_password: #password and confirm password do not match 
    print("""
        <html>
        <body>
            <p>Error: Passwords do not match.</p>
            <p><a href="javascript:history.back()">Go Back</a></p> <!--Allows user to go back to previous page without resetting the page-->
        </body>
        </html> 
    """)
elif len(new_password)<4: #password is less than 4 characters long
    print("""
        <html>
        <body>
            <p>Error: Passwords must be at least 4 characters long..</p>
            <p><a href="javascript:history.back()">Go Back</a></p> <!--Allows user to go back to previous page without resetting the page-->
        </body>
        </html>
    """)
elif not new_password or ' ' in new_password: #password left empty or has spaces in it
    print("""
    <html>
        <body>
            <p>Error: Passwords Cannot contain any spaces..</p>
            <p><a href="javascript:history.back()">Go Back</a></p> <!--Allows user to go back to previous page without resetting the page-->
        </body>
        </html>
    """)

else: #no errors with password inputs:
    Query="SELECT * FROM user where PasswordToken=%s" #checks which password to update by looking at the passwordtoken passed from passwordreset.py
    cursor.execute(Query,(token,))
    userfound=cursor.fetchone()

    if userfound: #passwordtoken found in database:
        password=bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())#this hashes the password using random piece of data called salt.
        #before hasing the password is encoded into bytes as hashpw requires a byte like object. It does this by using utf-8 encoding.
        #bcrypt.gensalt() generates a random salt value which is used in the hashing process. Salts are added to each password before hashing. Salts are unique to every password.
        #the salted hashed password is then stored in the database.
        #This makes it so that it is a one way hashing, as it is incredibly difficult to convert it back.
        UpdateQuery="UPDATE user SET Password=%s, PasswordToken='' WHERE PasswordToken=%s" #updates password with hashed password and empties passwordtoken as password has been reset
        cursor.execute(UpdateQuery,(password,token))
        conn.commit() #commits changes making it permanent
        print("Your Password has been Reset!")
    else: #if token is not found in database then:
        print("Error: Invalid token")

