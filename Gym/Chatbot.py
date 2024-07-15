#!C:\Users\Hp\AppData\Local\Programs\Python\Python312\python.exe
#This my shebang
import cgi
import cgitb 
import re # Importing the 're' module for regular expressions to work with string searching and manipulation.
import random # Importing the 'random' module to enable random selection of responses.


cgitb.enable()  # Enable CGI error reporting

# Defining a function to calculate the probability of the user's message containing recognized words that I am using.
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    # Initializes "message_certainty" variable to 0 for calculating how much of the message matches recognized words.
    message_certainty = 0
     # Starts with the supposition that all required words are in the message.
    has_required_words = True

 # Prints for debugging purposes, showing the function's inputs and the initial certainty value.
    for word in user_message:
           # Loops ('for' and 'if') iterate through each word in the user's message and check if it matches any recognized words.
        if word in recognised_words:
               # 'message_certainty' count how many recognized words were found in the user's message.
            message_certainty += 1  # Increases certainty for each recognized word found.


    # Calculates what percentage of the recognized words were mentioned in the message.
    # 'message_certainty' is used in this case as nominator, it checks how much of the message matches recognized words.
    # 'recognised_words' is used in this case as denominator it calculates the proportion of recognized words.
    # 'float' this function converts the count and the total number of recognized words into floating numbers.
    percentage = float(message_certainty) / float(len(recognised_words))


# Checks if the message contains all required words.
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break   # Exits the loop early if any required word is missing.


# Determines if the message is relevant enough for a response.
    # 'has_required_words' indicates whether all required words are present in the user's message.
    # 'single_response' means that if the user's message contains at least one recognized word or meets other conditions specified by the function, it will return a response, even if not all required words are present.
    if has_required_words or single_response:
        return int(percentage * 100)   # Returns the match percentage as an integer.
    else:
        return 0   # Returns 0 if the message doesn't meet the criteria for response.

# 'check_all_messages' is a function that analyzes user messages and finds the best response.
def check_all_messages(message):
    highest_prob_list = {}   # Initializes an empty dictionary to store response probabilities.


    # Nested function for setting up responses and calculating their probabilities.
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        #nonlocal means that 'highest_prob_list' variable is not a local variable, nor it is a global variable.
        nonlocal highest_prob_list
        # Calculates the probability of a response being relevant and stores it.
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Setup potential responses with their triggers(When a user enters a keyword as an input, it can act as a trigger for the bot, helping it to provide the user with what they need) and requirements.
    response('Hello!', ['hello', 'hi', 'hey'], single_response=True)
    response('Yes sure. How can I help you ?', ['i', 'have', 'a', 'question', 'ask'], required_words=['question'])
    response("UGym and Power Zone operate 24/7.", ['What', 'are', 'operating', 'hours'], required_words=['hours'])

 # Identifies the response with the highest probability of being relevant.
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return best_match if highest_prob_list[best_match] > 0 else None

# Provides a random unknown response if no suitable answer is found.
def unknown():
     # Randomly selects a response from a predefined list.
    return random.choice(['Could you please re-phrase that?', "...", "Sounds about right", "What does that mean?"])

# Start processing the form data
print("Content-Type: text/plain;charset=utf-8")
print()

form = cgi.FieldStorage()
user_input = form.getvalue('user_input', '')

    # Converts the user's input into a list of words in lowercase for analysis.
    # r'\s+|[,;?!.-]\s*': This is the regular expression pattern used for splitting the string, 'r' is a raw string, it is treating as a backslash.
    # \s+: Checks one or more whitespace characters.
    # |: indicates"or".
    # [,;?!.-]\s*: This part matches any of the characters within the square brackets (, ; ? ! . -).
    # 're.split' splits the user input into substrings, and I used 're' in this part because I mentioned regular expressions'\s+|[,;?!.-]\s*'.
split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
 # Finds and returns the most appropriate response for the input message.
response = check_all_messages(split_message)
# If there is no response which means empty or false, it will be called the unknown function that contain random responses.
if not response:
    response = unknown()
# Print the response.
print(response)