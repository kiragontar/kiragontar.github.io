#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
import cgi
import cgitb

# Define gym data globally in this python dictionary
# (docs.python.org, n.d.)
power_zone_data_with_membership = {
    "Joining fee (one-off fee)": 30,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 13,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 19,
    "Anytime": 24,
    "Swimming pool (with gym m.)": 12.5,
    "Classes (with gym m.)": 0,
    "Massage therapy (with gym m.)": 25,
    "Physiotherapy (with gym m.)": 25
}

power_zone_data_without_membership = {
    "Joining fee (one-off fee)": 30,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 13,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 19,
    "Anytime": 24,
    "Swimming pool (without gym m.)": 20,
    "Classes (without gym m.)": 20,
    "Massage therapy (without gym m.)": 30,
    "Physiotherapy (without gym m.)": 30,
}

uGym_data_with_membership = {
    "Joining fee (one-off fee)": 10,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 16,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 21,
    "Anytime": 30,
    "Swimming pool (with gym m.)": 15,
    "Classes (with gym m.)": 10,
    "Massage therapy (with gym m.)": 25,
    "Physiotherapy (with gym m.)": 20
}

uGym_data_without_membership = {
    "Joining fee (one-off fee)": 10,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 16,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 21,
    "Anytime": 30,
    "Swimming pool (without gym m.)": 25,
    "Classes (without gym m.)": 20,
    "Massage therapy (without gym m.)": 30,
    "Physiotherapy (without gym m.)": 25
}

uGym_discount_data = {
    "discount_percent_young_adult_student": 20,
    "discount_percent_pensioners": 15
}

power_zone_discount_data = {
    "discount_percent_young_adult_student": 15,
    "discount_percent_pensioners": 20
}

# Process form data
form = cgi.FieldStorage()

# Get user data from the form
user_data = { # created this dictionary is created to store the form data from the gym form 
    "trainer_type": form.getvalue("trainer_type"), # obtaining data using the getvalue() method same for the following lines so we can know what values where submited and what were left empty
    "add_swimming_pool": form.getvalue("add_swimming_pool"),
    "add_classes": form.getvalue("add_classes"),
    "Massage_Therapy": form.getvalue("Massage_Therapy"),
    "Physiotherapy": form.getvalue("Physiotherapy"),
    "age": form.getvalue("age"),  
    "student": form.getvalue("student"),
    "subscribe": form.getvalue("subscribe")  
}

 # function that calculate the best price for the user with two parameters user_data, gym_data
def calculate_price(user_data, gym_data):
    price = 0 # start by assigning the the value 0 to the price 
    joining_fee = gym_data.get("Joining fee (one-off fee)", 0) # here the gym_data.get will go and get the price of the Joining fee (one-off fee) 
    price += joining_fee  # here we add the joining fee to the price withe the '+=' that mean 'x=x+y'
    
    if user_data["trainer_type"] == "super_off_peak": # here we go to the user_data dictionary and see if the trainer_type is empty or not if not 
        key = "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)" if user_data["subscribe"] == "yes" else "Super-off peak (without gym m.)"
        price += gym_data.get(key, 0)
    elif user_data["trainer_type"] == "off_peak":
        # Determine the key based on user's subscription status
        price += gym_data.get("Off-peak (12 - 2 pm & 8 - 11 pm)", 0) if user_data["subscribe"] == "yes" else gym_data.get("Off-peak (without gym m.)", 0)
    elif user_data["trainer_type"] == "anytime":
        
        price += gym_data.get("Anytime", 0) if user_data["subscribe"] == "yes" else gym_data.get("Anytime (without gym m.)", 0)

    # Check if the user wants to add a swimming pool and calculate the price accordingly
    if user_data["add_swimming_pool"] == "yes":
        
        price += gym_data.get("Swimming pool (with gym m.)", 0) if user_data["subscribe"] == "yes" else gym_data.get("Swimming pool (without gym m.)", 0)
    
    if user_data["add_classes"] == "yes":# Check if the user wants to add classes and calculate the price accordingly
        price += gym_data.get("Classes (with gym m.)", 0) if user_data["subscribe"] == "yes" else gym_data.get("Classes (without gym m.)", 0)

    return price

# created calculate_price_with_discount() with three parameters user_data, gym_data, discount_data 
def calculate_price_with_discount(user_data, gym_data, discount_data): 
    price = calculate_price(user_data, gym_data)  # called the calculate_price()
    
    age = int(user_data.get("age", 0))
    discount_percent = 0  # Initialize the discount_percent
    
    if age <= 25 or user_data.get("student", "") == "yes": # if user data "student" isnt empty or they are a from 16 to 25 i will get the discount_percent_young_adult_student from the dictionary
        discount_percent = discount_data.get("discount_percent_young_adult_student", 0)
    elif age >= 66:# if user data is bigger or aqual to 66 i will get the discount_percent_pensioners from the dictionary
        discount_percent = discount_data.get("discount_percent_pensioners", 0)
    
    # Apply discount
    price = price - (price * discount_percent) / 100

    if user_data.get("Massage_Therapy", "") == "yes":# Check if the user is interested in Massage Therapy and calculate the price accordingly
        key = "Massage therapy (with gym m.)" if user_data["subscribe"] == "yes" else "Massage therapy (without gym m.)"
        price += gym_data.get(key, 0) # Determine the key based on user's subscription status
    if user_data.get("Physiotherapy", "") == "yes":# Check if the user is interested in Physiotherapy and calculate the price accordingly
        key = "Physiotherapy (with gym m.)" if user_data["subscribe"] == "yes" else "Physiotherapy (without gym m.)"
        price += gym_data.get(key, 0) # Determine the key based on user's subscription status

    return price


#=============================================================================================


# Determine gym data based on the selected gym for Power Zone
if user_data["subscribe"] == "yes":
    gym_data_power_zone = power_zone_data_with_membership
else:
    gym_data_power_zone = power_zone_data_without_membership

# call the calculate the total price for Power Zone
price_power_zone = calculate_price_with_discount(user_data, gym_data_power_zone, power_zone_discount_data)

# Determine gym data based on the selected gym for uGym
if user_data["subscribe"] == "yes":
    gym_data_uGym = uGym_data_with_membership
else:
    gym_data_uGym = uGym_data_without_membership

# call the calculate the total price for uGym
price_uGym = calculate_price_with_discount(user_data, gym_data_uGym, uGym_discount_data)

# Determine which gym is the best based on price
best_gym = "Power Zone" if price_power_zone < price_uGym else "uGym"

#mickels adjustment:
if price_power_zone< price_uGym:
    best_price= price_power_zone
else:
    best_price=price_uGym

# HTML response with CSS included
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Gym Suggestion</title>")
print("<style>")
print("""
/* Define your CSS styles here */
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}
.container {
    max-width: 600px;
    margin: 20px auto;
    margin-top:6%;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
    color:#000000 ;
}

p {
    margin: 10px 0;
}

.button {
  width: 150px;
  margin-top: 20px;
  margin-left:180px;
  background-color: #000000; 
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display:flex;
  margin-top: 6%;
  font-size: 16px;
  cursor: pointer;
  border-radius: 8px;
}

.button:hover {
  background-color: #2f2f2f;
}

""")
print("</style>")
print("</head>")
print("<body>")
print("<div class='container'>")
print("<center><h2>Best Gym Suggestion</h2></center>")
print("<br>")
print("<p>The best gym for you based on your preferences is: {}</p>".format(best_gym))
print("<br>")
print("<p>The price for Power Zone is: &#163;{:.2f}</p>".format(price_power_zone))
print("<br>")
print("<p>The price for uGym is: &#163;{:.2f}</p>".format(price_uGym))
print("<br>")
#mickels adjustment
print("<p> If you want to know more about the GYM follow this link: ")
# Depending on the gym, link to the respective page
if best_gym == "Power Zone":
    print("<a href='power_zone.py'>{}</a>".format(best_gym))
else:
    print("<a href='u_gym.py'>{}</a>".format(best_gym))

print(f"""
<script>
localStorage.setItem('best_price', '{best_price}');
</script>
<p> If you want to Sign up and make an account click on the following button: <a href='index.html' class="button">Proceed To Sign Up</a></p>
""")
print("</p>")
print("</div>")
print("</body>")
print("</html>")
# docs.python.org. (n.d.). 5. Data Structures — Python 3.9.0 documentation. 
# [online] Available at: https://docs.python.org/3/tutorial/datastructures.html#dictionaries.

