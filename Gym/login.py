#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe

import cgi
import cgitb #used to check for errors
import mysql.connector #used to connect to the database
import secrets #generates strong random hexadecimal strings here which is suitable for tokens 
import bcrypt #provides hashing, used here to hash the password enhancing security
import os #used to interact with operating system, used here with files.
from http import cookies #used to set up cookies to remember user.

# Forms a connection to the MySQL database
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

def get_user_data_from_token(token): #function to get user data from the token in the database
    try:
        cursor.execute("SELECT * FROM user WHERE Token = %s", (token,)) #executes query to select all information where token matches
        return cursor.fetchone() #returns that it has found matching results meaning that token exists in database
    except Exception as e: #if an error is encountered it prints this:
        print("Error retrieving user data from database:", e)
        return None #returns nothing.


C = cookies.SimpleCookie() #creates a simplecookie object and assigns it to C


def display_login_page(error_msg=""): #function to display login page with or without an error message
    
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Page</title>
        <style>
        .title{{/*Styles for elements with class="title"*/
    font-family: Arial, Helvetica, sans-serif; /*font family for the text*/
    font-size: 15px; /*font size for the text*/
    color: #403866; /*color for the text*/
    text-align: center; /*centers the text*/
    margin-top: 150px; /*Adds 150px of space on top of the title*/
}}
    .logintitle{{ /*Styles for elements with class="logintitle"*/
        margin-bottom: 40px; /*Adds 40px of space to the bottom of the element.*/
    }}
    .inputboxes{{ /*Styles for element with class="inputboxes"*/
        display: flex; /*Displays container as a flexbox*/
        flex-direction: column; /*Arranges element items in a column so that they are under each other*/
        align-items: center; /*Arranges element items so that they are centered horizontally*/
       
        
    }}
    .inputbox{{ /*Styles for elements with class="inputbox"*/
            width: 400px; /*Makes the width of the box to 400px*/
            border: 1px solid #ccc; /*Creates a solid border of 1px with color #ccc */
            padding:15px; /*Creates 15px of space between border and center*/
            background: #E6E6E6; /*Makes background of boxes that color*/
            margin-bottom:10px; /*Adds 10px of space to bottom of boxes*/
            border-radius: 5px; /*Makes border corner of boxes rounded*/
            transition: border-color 1s ease-in-out; /*Makes border color change after 1 second , ease-in-out makes it start slowly, accelerate and then slow down*/
           
        }}
    .inputbox:focus{{ /*When user clicks on the boxes*/
        border-color: blue; /*changes border color to blue*/
        outline: none; /*removes any outlines*/
    }}
    .inputbox::placeholder{{ /*Styles for the placeholder in the boxes*/
        font-family: Arial, Helvetica, sans-serif; 
        color:#8F8FA1; /*changes color of placeholder text*/
        font-weight: bold; /*makes placeholder bold*/
        font-size: 15px; /*makes placeholder font size 15px*/
    }}

    .forgot{{ /*Styles for elements with class="forgot"*/
        display: inline-block; /*displays container as inline-block */
        margin-left: 310px; /*Adds 310px of space to the left of the element*/
        margin-top: 10px; /*Adds 10px of space to the top of the element*/
        margin-bottom: 10px; /*Adds 10px of space to the bottom of the element*/
        font-size: 15px; /*Makes the text font size 15px*/
        font-family: Arial, Helvetica, sans-serif; 
        text-decoration: none; /*Removes any text decorations such as underline etc...*/
        color:black; /*makes text black*/
    }}
    .forgot:visited{{ /*Styles for when hyperlinks with the class="forgot" is visited*/
    color:black; /*makes link color black*/
    }}
    .button{{ /*Styles for the element with class="button"*/
        width: 435px; /*Makes width 435px*/
        border: 1px solid #ccc; /*Creates 1px of solid border with the color #ccc*/
        padding: 15px; /*Creates 15px of space between border and center*/
        border-radius: 5px; /*makes border corners rounded*/
        background: black; /*makes button background black*/
        color: white; /*makes text color white*/
        font-family: Arial, Helvetica, sans-serif; 
        font-weight: bold; /*makes text bold*/
        font-size: 15px; /*makes text font size 15px*/
        transition: background-color 0.5s ease-in-out; /*makes background color change 0.5seconds after hovering it*/
    }}
    .button:hover{{ /*styles for when button is hovered*/
        background-color: #403866; /*changes background color*/
    }}
    *{{ /*styles for everything*/
        padding: 0; /*resets padding*/
        margin:0; /*resets margin*/
        text-decoration: none; /*removes default text-decorations */
        list-style: none; /*removes list styles in lists such as bullet points*/
    }}
  
    body {{*Styles for everything in the body*/
        font-family: Facón; /*makes the font of the text*/
        background: #ffffff /*gives the background of the body the color #ffffff*/
    }}
  
    nav{{/*styles for everything in the <nav> tag*/
        background: #000000; /*Makes the background of the elements in the nav tag #000000*/
        height: 80%; /*Makes the height of the nav 80% of its containing elements */
        width:auto; /*tells nav to automatically adjust the width based on the contents inside*/
    }}
  
    label.logo{{ /*Style for labels with the class "logo"*/
        color: white; /*Makes the text of the label white*/
        font-size: 35px; /*Makes the text of the label 35px in font size*/
        line-height: 80px; /*sets the height of each line of text  to 80px*/
        padding: 0 100px; /*creates padding of 0px to top and bottom and 100px to left and right*/
    }}
  
    nav ul {{ /*Refers to the <ul> tags in the <nav> tags*/
        float: right; /*moves elements to right side of container so moves the ul to the right*/
        margin-right: 20px; /*Adds 20px of space to the right of the ul */
    }}
  
    nav ul li{{ /*Styles to the <li> tags inside <ul> tags that is inside the <nav> tag*/
        display: inline-block; /*Displays container as inline-block so element items are horizontally aligned with the same properties like height, etc.*/
        line-height: 80px; /*Sets the height of each line of text to 80px*/
        margin: 0 5px; /*Adds 0px of space to top and bottom and 5px to the left and right of the element*/
    }}
  
    nav ul li a{{ /*Refers to the li situation in the top one but if the li contains an <a> tag so this applies to hyperlinks in the li*/
        color: white; /*makes the hyperlink white*/
        font-size: 17px; /*makes the hyperlink 17px in font size*/
        border-radius:3px; /*Makes border corners of hyperlink rounded*/
        padding: 7px 13px; /*Creates padding of 7px to top and bottom and 13px to left and right sides of the hyperlinks*/
        text-transform: uppercase; /*Transforms the hyperlink into uppercase*/
    }}
  
    a.active, a:hover{{ /*Styles for hyperlink for when they are active meaning as soon as user clicks on it, and when they hover over the hyperlink*/
        background: #a1a1a1; /*makes the background #a1a1a1*/
        transition: .5s; /*makes the background change happen after 0.5seconds*/
    }}
    #loadingspinner{{ /*Styles for element with id "loadingspinner"*/
        position: fixed; /*keeps the position fixed on the screen so even if user scrolls up it still remains in the same position on the screen, so it goes up with the user*/
        top: 50%;  /*Centers element on the screen vertically*/
        left: 50%; /*Centers element on the screen horizontally*/
        /*Top and left 50% ensure that the top left of the loadingspinner is centered at the middle of the viewport initially*/
        display: none; /*Initially hides the element until adjusted later*/
        transform: translate(-50%, -50%); /*This centers the loadingspinner in the middle after it has its top left corner has been centered*/
        z-index: 1000; /* Ensure it's above other content */
    }}

    </style>
    </head>
    <body>
    <nav>
    <!-------------------------- Navigation Bar ------------------------>
    <label class="logo">GSO LAGO</label>
    <ul>
      <li><a href="Chatbot.html">Chatbot</a></li>
      <li><a href="mainpage.py">Home</a></li>
    </ul>
  </nav>
  <!--------------------------------------------------------------------->

    <div class="title">
        <h1 class="logintitle">LOGIN</h1>
    </div>
    <div class="inputboxes">
        <form action="login.py" method="post" id="loginForm"> <!--Has an id so that javascript can be used-->
            <input type="text" name="mID" class="inputbox" required placeholder="Membership ID" title="Enter a valid Membership ID"> <!--Takes mID from user-->
            <br>
            <input type="password" name="Password" class="inputbox" placeholder="Password" title="Password" required> <!--Takes password from user-->
            <br>
            <a href="passwordforget.html" class="forgot">Forgot Password?</a> <!--Link for if they want to reset their password-->
            <br>
            <div id="loadingspinner" style="display: none;"> <!--This div holds an id which is initially hidden-->
            <img src="pictures/spinning.gif" alt="loading"> <!--The div contains an image with the alternative specified to "loading" if picture doesnt load-->
            </div>
            <button type="submit" class="button">LOGIN</button>
        </form>
        {f'<div style="color: red;">{error_msg}</div>' if error_msg else ''} <!--Displays the error message if an error happens-->
    </div>
    </body>
    </html>
    <script>
    document.getElementById('loginForm').addEventListener("submit", function(event){{  //checks when user clicks submit
       document.getElementById('loadingspinner').style.display='block'; //makes loadingspinner visible
       document.getElementById('loginForm').style.pointerEvents='none';//this makes everything in the form unresponsive to mouse clicks, hover effects and any other pointer-related events.
       document.getElementById('loginForm').style.opacity='0.3';
       document.querySelector('input[type="submit"]').disabled = true; //just to ensure that no unexpected bug occurs this still works, this disable the submit button from working further
        }});
    </script>
    """)

    
def login(mID, password): #function to take mID and password and check if logins are successful or not

    try:
        cursor.execute("SELECT Password FROM user WHERE mID = %s", (mID,)) #executes query to check if mID entered by user exists and if password matches
        verify_result = cursor.fetchone()  # Fetch one result meaning that mID exists and is valid

        if verify_result and bcrypt.checkpw(password.encode('utf-8'), verify_result[0].encode('utf-8')):#bcrypt.checkpw checks if a given password matches a hashed password.
        #it first encodes the given password with utf-8 as it needs to be in bytes. verify_result[0] is the password retrieved its also encoded. 
        # Credentials are correct; so proceed with login
            token = generate_token() #creates token

            # Updates user session info in the database
            cursor.execute("UPDATE user SET Token = %s WHERE mID = %s", (token, mID)) #populates the token in the database where mID matches the users input
            conn.commit() #commits changes making it permanent

            # Sets cookie of token
            C["token"] = token #saves the token value in C["token"] so we can use it to remember the user.
                

            # Output cookies and redirect header
            print(C)
            print("Location: mainpage.py\n") #redirectes user to the main page with updated section indicating that they have logged in
            return True 
        else: #if password does not match:
            # Login failed
            return False 
    finally: # closes connection with database
        cursor.close()
        conn.close()

# Retrieve form data
form = cgi.FieldStorage()

if "mID" in form and "Password" in form: #checks if user entered both mID and Password
    mID= form.getvalue('mID') #collects mID value from user
    password = form.getvalue('Password') #collects password value from user

    if not login(mID, password): #if user login fails:
        display_login_page("Wrong Membership ID or Password. Please try again.") #calls function with error message
    else: #if user succeeds:
        print("Location: mainpage.py\n") #redirectes user to the main page with updated section indicating that they have logged in
else: #if user did not enter anything (so if user just enters the login page)
    try:
        C.load(os.environ["HTTP_COOKIE"]) #loads cookies from HTTP request headers into the simpleCookies which is in "C".
        #os.environ["HTTP_COOKIE"] retrieves value from the "HTTP_COOKIE" environment variable which is in the server side. 
        #which contains the cookie data sent by the client in the HTTP request headers.
        token = C.get("token").value if C.get("token") else None #gets the value of the cookie token and assigns it to token, if cookie token is empty then token=None.
        if token: #this means that cookie token is not empty
            # cookie Token exists, so fetch user data
            userdata = get_user_data_from_token(token) #userdata is then used to call the function 
            if userdata: #if token exist or is valid in database
                print("Location: mainpage.py\n") #redirectes user to the main page with updated section indicating that they have logged in
                print() #indicates that this is the end of the headers and start of the body
                conn.close() #closes database connection
                exit() #stops the program immediately
            else: #if token doesnt exist or is not valid:
                # Invalid token, redirect to login page
                display_login_page()
        else: #if cookie token is empty:
            # No token cookie, redirect to login page
            display_login_page()
    except KeyError:
        # Handle the case when HTTP_COOKIE is not set.
        display_login_page()







