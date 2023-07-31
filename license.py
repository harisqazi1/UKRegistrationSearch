#!/usr/bin/python3
import string
import requests
import time

API_key = "API_KEY_HERE"
#format for vehicles is LLNN LLL (L=Letter; N=Number)
first_letter = list(string.ascii_uppercase)
#DVLA does not use I, Q, or Z in memory tags
first_letter.remove("I")
first_letter.remove("Q") #might have to remove
first_letter.remove("Z")
second_letter = list(string.ascii_uppercase)
second_letter.remove("I")
second_letter.remove("Q") #might have to remove
second_letter.remove("Z")
third_digit = list(string.digits)
third_digit.remove("3")
third_digit.remove("4")
third_digit.remove("8")
third_digit.remove("9")
fourth_digit = list(string.digits)
fifth_letter = list(string.ascii_uppercase)
sixth_letter = list(string.ascii_uppercase)
seventh_letter = list(string.ascii_uppercase)

#Tracking the amount of wildcards in the plate - max 3 currently
alphabet_wildcard = 0
number_wildcard = 0

# Can be used to output a list of all possible values as well - might have to dedup after 
def full():
    # license_plate = "@@$$@@@" #Removed space to make it easier to use with API; @ for letter, $ for number
    # used symbols to mitigate the issue of overwriting true positive license characters
    license_plate = "@@$$@@@" #All letters and numbers are unknown; NOT Recommended.
    for first in first_letter:
        for second in second_letter:
            for third in third_digit:
                for fourth in fourth_digit:
                    for fifth in fifth_letter: 
                        for sixth in sixth_letter: 
                            for seventh in seventh_letter: 
                                print(license_plate.replace("@", first, 1).replace("@", second, 1).replace("$", third, 1).replace("$", fourth, 1).replace("@", fifth, 1).replace("@", sixth, 1).replace("@", seventh, 1))

license_plate = "AA1$AAA" #Removed space to make it easier to use with API; @ for letter, $ for number

def format_check():
    #Simple check; can be expanded to check each position, but deemed not necessary
    if len(license_plate) != 7:
        print("License Plate Size Incorrect")
        exit()
    
def wildcards():
    # Using global to be able to modify the variables outside of the function
    global alphabet_wildcard
    global number_wildcard
    #Search for "@" and "$" in licence plate to see how many wildcards to work off of
    for index in license_plate:
        if index == "@":
            alphabet_wildcard += 1
        if index == "$":
            number_wildcard += 1

#Cue the API to output information regarding a specific registration number
def license_print():
    global alphabet_wildcard
    global number_wildcard
    # These do NOT account for the I,Q,Z not referenced in the memory tags - TLDR; extra output
    if alphabet_wildcard == 1 and number_wildcard == 0:
        for upper in list(string.ascii_uppercase):
            print("Post request submitted for: {}".format(license_plate.replace("@", upper)))
            api_request(license_plate.replace("@", upper))
    elif alphabet_wildcard == 0 and number_wildcard == 1:
        for digit in list(string.digits):
            print("Post request submitted for: {}".format(license_plate.replace("$", digit)))
            api_request(license_plate.replace("$", digit))
    elif alphabet_wildcard == 1 and number_wildcard == 1:
        for upper in list(string.ascii_uppercase):
            for digit in list(string.digits):
                print("Post request submitted for: {}".format(license_plate.replace("@", upper).replace("$", digit)))
                api_request(license_plate.replace("@", upper).replace("$", digit))
    elif alphabet_wildcard == 2 and number_wildcard == 1:
        for first in list(string.ascii_uppercase):
            for second in list(string.ascii_uppercase):
                for digit in list(string.digits):
                    print("Post request submitted for: {}".format(license_plate.replace("@", first, 1).replace("@", second,1).replace("$", digit)))
                    api_request(license_plate.replace("@", first, 1).replace("@", second,1).replace("$", digit))
    elif alphabet_wildcard == 1 and number_wildcard == 2:
        for upper in list(string.ascii_uppercase):
            for first in list(string.digits):
                for second in list(string.digits):
                    print("Post request submitted for: {}".format(license_plate.replace("@", upper, 1).replace("$", first,1).replace("$", second, 1)))
                    api_request(license_plate.replace("@", upper, 1).replace("$", first,1).replace("$", second, 1))
    elif alphabet_wildcard == 3 and number_wildcard == 0:
        for first in list(string.ascii_uppercase):
            for second in list(string.ascii_uppercase):
                for third in list(string.ascii_uppercase):
                    print("Post request submitted for: {}".format(license_plate.replace("@", first, 1).replace("@", second,1).replace("@", third, 1)))
                    api_request(license_plate.replace("@", first, 1).replace("@", second,1).replace("@", third, 1))
    elif alphabet_wildcard == 0 and number_wildcard == 3:
        for first in list(string.digits):
            for second in list(string.digits):
                for third in list(string.digits):
                    print("Post request submitted for: {}".format(license_plate.replace("$", first, 1).replace("$", second,1).replace("$", third, 1)))
                    api_request(license_plate.replace("$", first, 1).replace("$", second,1).replace("$", third, 1))
    #not working for some reason
    else:
        ("Currently not supported")
        exit()

def api_request(reg_num):
    # Actual Environment
    #url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    # Test Environment
    url = 'https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    payload = "{\n\t\"registrationNumber\": \"%(reg)s\"\n}" % {'reg': reg_num} # String interpolation with %
    headers = {
    'x-api-key': API_key,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    #Using print(response.text.encode('utf8')) outputs lines with b' which then needs .decode("utf-8") to fix
    print(response.text)
    time.sleep(2) # 2 second time out to prevent flooding
            
if __name__ == '__main__':
    format_check()
    #full()
    wildcards()
    license_print()
