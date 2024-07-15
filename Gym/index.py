#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb #used to check for errors
import smtplib #has functions to interact with an simple mail transfer protocol (SMTP) server to send emails
from email.mime.text import MIMEText #MIMEText class is used to create email message objects that contain plain text content.
#MIME (Multipurpose Internet Mail Extensions), its a standard to format non-ASCII messages so that they can be sent over the internet
#MIMEText provides methods to set text content, character encoding and other attributes of the email.
from email.mime.multipart import MIMEMultipart #MIMEMultipart class creates email message objects that contains parts such as plain text, html attachments.
import mysql.connector #used to connect to the database
import os #used to interact with operating system, used here with files.
import secrets #generates strong random hexadecimal strings here which is suitable for tokens 
import datetime #provides functions to manipulate date and time, used here to calculate age from the format "dd-mm-yyyy"
import bcrypt #provides hashing, used here to hash the password enhancing security
import random #generates random numbers, used here for membershipID


def generate_token(length=32):  #function to generate random tokens 
    return secrets.token_hex(length // 2) #generates random string of hexadecimal digits. Each hexadecimal character represents half a byte so 2 characters represent a byte
    #so to convert the length into bytes it is divided by 2 which is the number of characters that make up a byte.
    #The length in bytes is then sent to secrets.token_hex() which generates a random hexadecimal string of the specified length in bytes 
    #converts length of token from number of characters to number of bytes
    #if you enter no length in the paramter and just enter 16 in the parameter> secrets.token_hex(16) it will generate 16bytes but 32 hexadecimal character.

token=generate_token()   #assigns the generate_token() function into token
ImageFile=generate_token() #assigns the generate_token() function into ImageFile. this is to help us understand which image corresponds to which user.

print("Content-type: text/html\n") #specifies content type is html
# Forms a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="MickelUWE",
    password="Jram1212", 
    database="Gym"
    )
cursor = conn.cursor()


def generate_mID():#function to generate a membership ID
    while True:#makes an infinite loop until a unique membership id is found.
        mID = 'm' + ''.join(random.choices('0123456789', k=4)) #concatenates m to random choices of numbers from 0 to 9, up to 4 times, effectively creating m(four numbers).
        cursor.execute("SELECT * FROM user WHERE mID = %s", (mID,)) #executes a query to check if MembershipID is in the database
        if not cursor.fetchone():  #this meands if it does not find mID in the database then:
            return mID #returns the generated mID.


def send_email(sender_email, receiver_email, subject, smtp_server, smtp_port, smtp_username, smtp_password): #function to send email
    





    #my html body
    #double curly brackets are used in css to prevent it to think that the contents inside one curly brackets are to be substituted due to the use of fstring
    #so double curly brackets are used instead
    html_body = f"""  
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Gym Verification</title>
    <style>
    body {{
        text-align: center;      /*centeres the body text*/
    }}
    h1, h2 {{
        color: rebeccapurple;
        font-weight: bold;       /*Makes the heading bold and colored*/
    }}
    .verify-button {{
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
    .verify-button:hover {{
        cursor: pointer;        /*Makes the mouse cursor change to a pointer when hovered on the button*/
        background-color: #663399; /*Makes the background color change when hovered on*/
        color: #fff;            /*Makes content color change when hovered on*/
    }}
    </style>
    </head>
    <body>
    <h1>Welcome to the Gym</h1>
    <h2>You have Registered Your email with our Gym!</h2>
    <p>This is an automated email sent to you for registering with our Gym.</p>
    <p><strong>Please Click the Button below to verify your account.</strong></p>
    <a class="verify-button" href='http://localhost/webprog/Gym/verify.py/{token}'>Verify Your Account</a> <!--Token added at end of link so that it can retrieved-->
    <p>If you have any questions, contact our support team at Support@gym.com</p>
    </body>
    </html>
    """ #the token in {} is used to take them to the website but with a token at the end of it so that we can retrieve it to use it to verify user



    # Creates the MIME object
    message = MIMEMultipart() #creates a MIME object and assigns it to message. MIME is a standard format for email messages that contain different contents such as html, text and attachments.
    message["From"] = sender_email #specifies the sender's email address.
    message["To"] = receiver_email #specifies the recipient's email address.
    message["Subject"] = subject #specifies the subject of the email.

    # Attaches the email body to the message.
    message.attach(MIMEText(html_body, "html")) #creates a text part with HTML content , html_body contains the HTML content of the email

    # This establishes a connection to the SMTP server specifies by smtp_server and smtp_port
    with smtplib.SMTP(smtp_server, smtp_port) as server: #tls (Transport layer security)
        # Starts tls for secure communication between python script and smtp server
        server.starttls() #starts a TLS connection for secure communication between python scirpt and smtp server, as TLS encrypts data exchanged between python script and server.
        # Logs in to the email account associated with the smtp server
        server.login(smtp_username, smtp_password)       
        # Sends the email
        server.sendmail(sender_email, receiver_email, message.as_string()) #specifies the sender's email and receiver's email address, as well converts the message into a string
    


    

#usernameinformation is an empty dictionary that is created to take and store the input from the user and store them
usernameinformation={} #empty dictionary
form = cgi.FieldStorage() #parses form data submitted in a HTTP request. returns the submitted form fields and their values
best_price=form.getvalue('best_price') #collects the value of an element with the name of "best_price"
usernameinformation["FirstName"] = form.getvalue('FirstName') #collects the value of element with the name "FirstName" and saves it into the usernameInformation dictionary.
usernameinformation["LastName"] = form.getvalue('LastName') #collects the value of element with the name "LastName" and saves it into the usernameInformation dictionary.
usernameinformation["email"] = form.getvalue('email')#collects the value of element with the name "email" and saves it into the usernameInformation dictionary.
usernameinformation["Password"] = form.getvalue('Password') #collects the value of element with the name "Password" and saves it into the usernameInformation dictionary.
usernameinformation["Confirm Password"] = form.getvalue('Confirm Password') #collects the value of element with the name "Confirm Password" and saves it into the usernameInformation dictionary.
usernameinformation["DOB"] = form.getvalue('DOB') #collects the value of element with the name "DOB" and saves it into the usernameInformation dictionary.
usernameinformation["country_code"] = form.getvalue('country_code') #collects the value of element with the name "country_code" and saves it into the usernameInformation dictionary.
usernameinformation["Phone"] = form.getvalue('Phone') #collects the value of element with the name "Phone" and saves it into the usernameInformation dictionary.
usernameinformation["Student"] = form.getvalue('Student') #collects the value of element with the name "Student" and saves it into the usernameInformation dictionary.
usernameinformation["studentID"]=form.getvalue('studentID') #collects the value of element with the name "studentID" and saves it into the usernameInformation dictionary.


def calculate_age(DOB): #function to calculate age from date of birth.
    try:#converting string to datetime object, first datetime is the module, second datetime is a class in the module and strptime belongs to datetime class
        DOB_date=datetime.datetime.strptime(DOB, '%Y-%m-%d') #(DOB,'%Y-%m-%d) tells strptime how to intepret the format of DOB %Y represents 4 digit year, %m represents 2 digit month, %d represents 2 digit day
        #capital Y is used to tell strptime that the fomat is 4 digits yyyy if only 2 digits are needed such as 22(yy) then lowercase y would be used
        today=datetime.datetime.now() #todays date 

        age=today.year - DOB_date.year -((today.month,today.day)<(DOB_date.month,DOB_date.day)) #checks if todays month is earlier than births month, if yes return 1 otherwise 0, if both months are equal compares day instead.
        #first subtracts birth year from current year, then subtracts by 1 or 0 depending if todays month and day are earlier than DOB month and day
        return age
    except Exception as e: #if error occurs:
        print(f"error calculating age:: {e}") # prints out the error
        return None #returns nothing if an error occurs

age=calculate_age(usernameinformation["DOB"]) #calls function of calculating age with the DOB collected as the argument and assigns it to age

mID = generate_mID() #calls the generate_mID function and assigns it to mID


Password=usernameinformation["Password"]  #assigns Password the value of the input from the dictionary
if not Password or ' ' in Password: #if password is left empty or if it contains spaces then:
    print("Invalid Password, Password cannot be empty or contain spaces") #prints this
    print("Please try again <html><body><a href='index.html'>here</a></body></html>") #prints this allowing them to go back to try again
elif age<16: #checks if user is under 16
    print("Invalid Age requirement, You must be 16 and above to sign up with our gym") #prints this
    print("Please return to the signup page <html><body><a href='index.html'>here</a></body></html> ") #prints this allowing them to go back to try again.
else: #else if its neither of these two conditions:

    Query="select email from user where email='"+usernameinformation["email"]+"'"  #query to check if email exists in the database
    cursor.execute(Query) #executes the query 
    result=cursor.fetchall() #assigns result the value of the rows collected from the database
    if result: #checks if the query was able to select an email, if it was:
        print("Email already Exists, please retry with another email: <a href='index.html'>Go Back</a>")#prints this allowing them to return back and try again
    else: #if email isnt in database, proceed:
        #send_email("mickelgerges1@gmail.com",usernameinformation["email"],"Welcome gym","sandbox.smtp.mailtrap.io",2525,"52dddb5b4f6b2c","251e868964e025")
        #calls send_email function
        #allows email to be sent and specifies who the sender is who the receiver is , and what the receiver should receive
        print("<p>Your Account has been Created Successfully.</p>") #tells user that there account has been created
        print("<h2>Please Remember Your mID as you need it to access the facilities and log in to the website.</h2>")#tells user to remember their mID
        print(f"<h1>Your mID:<u> {mID}</u></h1>") #tells user their mID
        print(f"<p>Please proceed to payment <a href='paymentpage.py?best_price={best_price}'>Here</a></p>") #link to take them to payment with the price in the link so it can be retrieved in the payment page.
        print("<p>Please Check Your email to Verify your account</p>") #tells user to check their email to verify their account
        

   
        if form['Student'].value=='yes': #checks if user picked if they are a student
            Student=1 #updates value to 1 if they are a student 
        else:#otherwise student picked they are not a student
            Student=0 #updates value to 0 if not
        uploaded_file=form["studentID"] #retrieves information about the studentID file uploaded
        splitFilename=(uploaded_file.filename).rsplit(".")[-1] #.filename retrieves the name of the file and .rsplit(".") splits the filename based on the period and retrusn a list of substrings.
        #[-1] retrieves the last substring and so retrieves the file extension for ex: png, jpeg etc...
        
        

        usernameinformation["Password"] = bcrypt.hashpw(usernameinformation["Password"].encode('utf-8'), bcrypt.gensalt()) #this hashes the password using random piece of data called salt.
        #before hasing the password is encoded into bytes as hashpw requires a byte like object. It does this by using utf-8 encoding.
        #bcrypt.gensalt() generates a random salt value which is used in the hashing process. Salts are added to each password before hashing. Salts are unique to every password.
        #the salted hashed password is then stored in the database.
        #This makes it so that it is a one way hashing, as it is incredibly difficult to convert it back.
        if form['Student'].value=='no': #if the user does not upload any files it will give NULL to ImageFile
        
            InsertQuery="Insert into user(mID,Email, DOB, FirstName, LastName,Country_Code, PhoneNumber, Student,Document,EmailToken,IsVerified,Password,Status,PasswordToken) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #query that inserts the input from the form to the database
            #values define what is inputted to each attribute
            values=(
                mID,
                usernameinformation["email"],
                usernameinformation["DOB"], 
                usernameinformation["FirstName"], 
                usernameinformation["LastName"],
                usernameinformation["country_code"],
                usernameinformation["Phone"],
                Student,
                "", #inputs empty string
                token, #input generate token in EmailToken for user verification
                "0", #initially set to 0 until user verifies their account
                usernameinformation["Password"],
                "0", #set to 0, 
                "" #passwordToken is initially set to an empty string until user wants to reset their password
            )
            cursor.execute(InsertQuery,values) #executes the querry
            conn.commit() #makes changes performed permanent
        else: #else if student is a student input details of imagefile
             InsertQuery="Insert into user(mID,Email, DOB, FirstName, LastName,Country_Code, PhoneNumber, Student,Document,EmailToken,IsVerified,Password,Status,ImageFile,PasswordToken) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #query that inserts the input from the form to the database
        #values define what is inputted to each attribute
        #if users is a student it will save the studentidimage to the database
        values=(
            mID,
            usernameinformation["email"],
            usernameinformation["DOB"], 
            usernameinformation["FirstName"], 
            usernameinformation["LastName"],
            usernameinformation["country_code"],
            usernameinformation["Phone"],
            Student,
            "",
            token,
            "0",
            usernameinformation["Password"],
            "0",
            ImageFile+"."+splitFilename, #inputs the filename and extension in the database. This will help us verify which image corressponds to which user
            ""
    
        )
        cursor.execute(InsertQuery,values) #executes the querry
        conn.commit() #makes changes performed permanent




        


        StudentIdUpload = 'C:\\xampp\\htdocs\\webprog\\Gym\\StudentID\\' #specifies directory of the folder where the studentid file is saved
        if not os.path.exists(StudentIdUpload): #checks if folder exists if not its creates a new folder called studentidupload
            os.makedirs(StudentIdUpload) #creates folder specified in the studentIdUpload.
        

        if 'studentID' in form: #checks if the student id file was inputted, if yes it continues on with the following.
            student_id_image = ImageFile+"."+splitFilename #student_id_image is assigned the value of the file from the input 
            if student_id_image!='': #checks if file is not empty
                # Save the file to the "StudentID" folder  
                with open(os.path.join(StudentIdUpload, student_id_image), 'wb') as f: #opens the file in binary write mode ('wb') and safely closes it afterwards. student_id_image represents the filename of the file that is saved there.
                    file_content = form["studentID"].file.read() #reads the file and assigns file_content the value of the read file
                    f.write(file_content) #writes the content of the file in the folder


        
       






