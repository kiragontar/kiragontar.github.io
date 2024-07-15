#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb
import stripe #library used to process payments



stripe.api_key ="sk_test_51OfrgIKIMiCe8DLhNBbfYRwDM2Xaiqc0UJiST7QN91Yg9yn6fdRqWolGMLTHLESmxqCAXAkkr8Re15FK4NefTWTU00T8A6nnJG" #this is a test API key used for authenticating requests to Stripe API
print("Content-type: text/html\n") #prints http header indicating content type is HTML.


def generate_card_token(cardnumber, expmonth, expyear, cvv): #this function takes card details from user and stripe api generates a card token, which is a secure representation of the card details 
    try:#uses stripe api to create a new token representing the provided card details
        data = stripe.Token.create( #stripe.Token.create is called with a dictionary containing card details as its argument
            card={
                "number": str(cardnumber), #card number is converted into a string
                "exp_month": int(expmonth), #expmonth is converted into an integer
                "exp_year": int(expyear), #expyear is converted into an integer
                "cvc": str(cvv), #cvv is converted into a string
            })
        card_token = data['id'] #this retrieves the id of the generated card token and assigns it to card_token.
        return card_token #returns the card_token
    except stripe.error.CardError as e: # Handles cases with card errors (eg: card declined or invalid...), we can raise a specific exception and return False to indicate payment is unsuccessful
        # Handle card error
        print("Card error:", e)
        return None #returns None as card_token could not be generated
    except stripe.error.StripeError as e: #for any stripe errors that are not specifically a card error
        # Handle other Stripe errors
        print("Stripe error:", e) #prints error
        return None #returns None as card_token could not be generated

def create_payment_charge(tokenid, amount): #takes tokenid (token representing payment source) and amount(to pay) as parameters 
    try:
        amount_in_pence=round(float(amount)*100) # convert amount to pennies by multiplying by 100 and rounds to nearest number as stripe processes amounts in the smallest currency unit.
        payment = stripe.Charge.create(
            amount= amount_in_pence,   #amount to be paid
            currency='gbp', #currency in which it is paid
            description='Gym Membership', #description of payment
            source=tokenid, #token representing payment source
        )
        payment_check = payment['paid'] #the "payment" object represents the response from stripe API, After attempting to create a charge it contains information about the payment transcaction such as ID, amount, currency, status and payment source details.
        #it checks the "paid" attribute from the payment object and if paid is True payment is successful, otherwise it failed.
        return payment_check #returns the value of paid if it is false or true and decide if payment was successful or not.
    except stripe.error.CardError as e:
        # Handles cases with card errors (eg: card declined or invalid...), we can raise a specific exception and return False to indicate payment is unsuccessful
        print("Card error:", e)
        return False
    except stripe.error.StripeError as e: #for any stripe errors that are not specifically a card error 
        # Handle other Stripe errors
        print("Stripe error:", e)
        return False #to indicate payment is unsuccessful







        
cgitb.enable()
form=cgi.FieldStorage() #collects information from input of user
Name=form.getvalue('cardname') #collects card name
CNumber=form.getvalue('cardnumber') #collects card number
expmonth=form.getvalue('expmonth') #collects expiry month
expyear=form.getvalue('expyear') #collects expiry year
cvv=form.getvalue('cvv') #collects cvv value
total=form.getvalue('total') #collects total from hidden value in paymentpage.py
expmonth = int(expmonth) #converts the month to an integer
expyear = int(expyear) #converts the year into an integer

html_body='''
<!DOCTYPE html>
<html>
<head>
<title>Redirect Page</title>
<meta http-equiv="refresh" content="3;url=mainpage.py">
<body>
<p>Redirecting in 3 seconds...</p>
</body>
</head>
</html>
''' #payment confirmation page redirecting them to mainpage





try: 
    tokenid=generate_card_token(CNumber, expmonth, expyear, cvv)  #calls card token function with inputted arguments and assigns it to tokenid
    if create_payment_charge(tokenid, float(total)): #checks if payment is successful with the tokenid and total amount as arguments
        print("<p>Payment Successful</p>")  #displays confirmation of payment
        print(f"<p>Payment of &#163;{total} has been made.</p>")
        print(html_body)
        
    else: #if payment is unsuccessful
        print("<p>Payment Unsuccessful</p>") 

except Exception as e: #displays any errors:
    print("<p>" + str(e) + "</p>")