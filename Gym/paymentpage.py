#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb

form = cgi.FieldStorage()#parses form data submitted in a HTTP request. returns the submitted form fields and their values

value=form.getvalue('best_price') #retrieves best_price from the link used to take user to this page in index.py and assigns the price to value
display_value=f"&#163;{value}" #this is used to display the value with the pound sign before it and assigns it to display_value

html_paymentpage=f"""<!DOCTYPE html> 
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Page</title>

    <style>
     body{{/*Styles for everything in the body*/
      font-family: Arial, Helvetica, sans-serif;
      margin: 0; /*resets the margin and padding to 0 incase the default has some already*/
      padding: 0;
      box-shadow: border-box; /*tells the browser to include the padding and border in the elements total size */
     }}
     .mainbackground{{ /*Styles for element with the class="mainbackground"*/
      min-height: 100vh; /*min height is used to ensure that it still covers most of the page initially and if it needs to accommodate later*/
      width: 100%; /*make the elements width take all the page*/
      display: flex; /*displays container as a flexbox */
      flex-direction: column;/* orders the flex items as columns so they are vertically under each other*/
      background-image: url('pictures/backgroundpayment.avif'); /* Set the image as the background */
      background-size: cover; /* Cover the entire background */
      background-position: center; /* Center the background */
     }}
     .card{{ /*Styles for element with the class="card"*/
      width: 60%; /*makes it take 60% of its containing blocks width */
      margin: auto; /*automatically calculates and sets equal margins on all sides of the element, basically centering it horizontally.*/
      background: white; 
      align-self: center; /*centers this flex-item vertically*/
      top: 50%; /* positions the top part of the element at 50% of the containing elements height which is the mainbackground*/
      border-radius:15px;
      box-shadow: 4px 3px 20px #3535358c; /* creates a shadow with a horizontal offset of 4px, vertical offset of 3px. blur radius of 20px.*/
      display: flex;  /* the shadow has a color of #353535 with the opacity of 54% due to 8c*/
      flex-direction: row;/* makes the items ordered in rows*/
     }}
     .left-side{{ /*Styles for element with class="left-side"*/
      background: #162836; /*Makes background with the color #162836*/
      width:25%; /*makes it take up 25% of its containing blocks width*/
      display: inline-flex; /* makes it behave as an inline level element instead of a block level element but still has flexbox properties*/
      align-items: center; /* centers the flex item vertically*/
      justify-content: center; /* centers the flex item horizontally*/
      border-top-left-radius: 15px;  /*makes top left corner rounded*/
      border-bottom-left-radius: 15px; /*makes bottom left corner rounded*/
     }}
     .gympic{{ /*styles for element with class="gympic"*/
      object-fit: cover; /* makes sure the image covers the entire container*/
      width: 80%; /*Makes it take up 80% of its containing blocks width*/
      height:50%; /*makes it take up 50% of its containing blocks height*/
      border-radius:30%; /* to make the corners of the border*/
      
     }}
     .right-side{{ /*Styles for element with class="right-side"*/
      background-color: #ffffff; /*makes background color #ffffff*/
      width:35%; /*Makes it take up 35% of its containing block width*/
      padding: 1rem 2rem 3rem 3rem; /* another unit of measurement 1rem=16px */
     }}
     p{{ /*Styles for all <p> tags*/
      display: block; /*displays container as a block*/
      font-size: 18px; /*makes font size 18px*/
      font-weight: bold; /*makes text bold*/
      margin:12.5px; /*adds 12.5px of space to each direction of the p tag*/

     }}
     .inputbox{{ /*Styles for elements with class="inputbox"*/
      width:100%; /*makes it take up 100% of the containing blocks width*/
      padding:8px; /*Creates 8px of space between border and center*/
      border: none; /*removes any border*/
      border-bottom: 1.5px solid #ccc; /*creates a border with the bottom side only*/
      margin-bottom: 8px; /*Adds 8px of space to the bottom of the element*/
      border-radius: 5px; /*Makes corner of border rounded */
      font-family: Arial, Helvetica, sans-serif;
      font-size: 15px; /*makes text in box font size 15px*/
      font-weight: bold; /*makes text in box bold*/
      color: #615a5a; /*makes text in box this color*/
      outline: none; /*removes any outlines when user clicks on box*/
     }}
     .button{{ /*styles for elements with class="button"*/
      background: linear-gradient(135deg, #4e8cff 0%, #5effa1 100%); /*makes the background of the button. Linear gradient makes it so that two colors after each other can be used*/
      /*135deg means that the colors are 135degrees from each other. #4e8cff and #5effa1 are the two colors used. 0% and 100% indicate the starting points, 0% is at the start 100% is at the end  */
      padding: 8px; /*Creates 8px of space between border and center*/
      border: none; /*Removes any borders*/
      border-radius: 10px; /*Makes default border-corners rounded*/
      color: white; /*makes text inside button white*/
      font-weight: bold; /*makes text bold*/
      font-size: 14px; /*makes text 14px*/
      margin-top: 10px; /*adds 10px of space on top of the button*/
      width: 100%; /*makes button take 100% of the containing blocks width*/
      letter-spacing: 1px; /*makes 1px of space between each letter*/
     }}
     .button:hover{{ /*Styles for when user hovers over button*/
      transform: scale(1.05) translateY(-3px); /*This makes the button enlarged by 5% once its hovered on and will move it upwards by 3px*/
      box-shadow: 3px 3px 6px #38373785; /*shadows appear 3px above and below the button with a blur radius of 6px and a color*/
     }}
      

    </style>
</head>
    <body>
        <div class="mainbackground">
          <div class="card">
            <div class="left-side">
              <img src="pictures/gymbackground.jpg" class="gympic" alt="gym logo">
            </div>
            <div class="right-side">
              <form action="payment.py" method="post">
                <h1>Checkout</h1>
                <h2>Payment Information</h2>
                <p>Card Name</p>
                <input type="text" class="inputbox" name="cardname" pattern="[A-Za-z\s]+" placeholder="John Robert Doe" title="Please Enter Only Names" required>
                <p>Card Number</p>
                <input type="number" class="inputbox" name="cardnumber" id="cardnumber"  placeholder="1111-2222-3333-4444" required>
                <p>Exp Month</p>
                <input type="number" class="inputbox" name="expmonth" id="expmonth" placeholder="06(month in number)" required>
                <p>Exp Year</p>
                <input type="number" class="inputbox" name="expyear" id="expyear" placeholder="2024(year in number)" required>
                <p>CVV</p>
                <input type="number" class="inputbox" name="cvv" id="cvv"  placeholder="443" required>
                <p></p>
                <input type="hidden" name="total" value="{value}"> <!--Hides value from user as it is being passed to payment.py-->
                <button type="submit" class="button">Pay {display_value}</button> <!--Displays the total to be payed to the user-->
              </form>
            </div>
          </div>
        </div>

        
    </body>
    </html>
"""
print("Content-type: text/html\n")
print(html_paymentpage)

   