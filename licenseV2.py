# Import modules
import requests
import time
import sys
import string
import argparse
import signal # To catch the KeyboardInterrupt when CTRL-C is run

#Parsing the command-line arguments
parser = argparse.ArgumentParser(
                    prog='licenseV2.py',
                    description='This code uses UK partial plates to convert that into potential plates. It then searches the DVLA API with that information.',
                    epilog='Created by: Haris Qazi. Assisted by: AccessOSINT.')
parser.add_argument("license", type=str)
parser.add_argument('--api', help='Use API Key. If no key is provided, it will not search DVLA database.') 
args = parser.parse_args()
# Plate Values
memory_tag =  list(string.ascii_uppercase)
memory_tag.remove("I")
memory_tag.remove("Q")
memory_tag.remove("Z")
third_number = ("0", "1", "2", "5", "6", "7")
# fourth number is done in the loops themselves
random_letter = list(string.ascii_uppercase)
random_letter.remove("I")
random_letter.remove("Q")

# The following follow a "waterfall effect". wildcards_plates -> wildcard_plates -> plates. The wildcard plates get placed on the top and then one by one the wildcards are removed.
wildcards_plates = [] # 3 wildcards -> which turn to 2
wildcard_plates = [] # 2 wildcards -> which turn to 1
plates = [] # Completed List; 1, which turn to 0
# Command Line Input
partial = args.license.upper().replace(" ", "")
# Gets the indexes of where wildcard characters are.
# uses list compression
indices = [i for i, char in enumerate(partial) if char == '?']
#count the amount of wildcards
wildcard = len(indices)
# Check
if args.license == "":
    print("No argument provided")
    exit()
elif len(partial) != 7:
    print("Size Incorrect")
    exit()
elif "?" not in partial:
    print("No Wildcards found")
    exit()
elif wildcard > 3 or wildcard < 1:
    print("Only 1 - 3 Wildcards Allowed")
    exit()
# ---------------------------------------------------------------------------------------------
def one_wildcard():
# Works for ?D51AAA and B?51AAA
    if indices[0] < 2:
        for letter in memory_tag:
            wildcards_plates.append(partial.replace("?", letter, 1))
    # BD?1AAA
    elif indices[0] == 2:
        for number in third_number:
            wildcards_plates.append(partial.replace("?", number, 1))

    # BD5?AAA
    elif indices[0] == 3:
        if partial[2] == "0":
            for number in range(2, 10):
                wildcards_plates.append(partial.replace("?", str(number), 1))
        elif partial[2] == "2" or partial[2] == "7":
            for number in range(1, 4): #Until February 2024
                wildcards_plates.append(partial.replace("?", number, 1))
        else:
            for number in list(string.digits): #could have done a set, but would be overkill
                wildcards_plates.append(partial.replace("?", number, 1))
    # BD51?AA and BD51A?A and BD51AA?
    elif indices[0] > 3:
        for letter in random_letter:
            wildcards_plates.append(partial.replace("?", letter, 1))
# ---------------------------------------------------------------------------------------------
def two_wildcards():
    for p in wildcards_plates:
        if indices[1] < 2:
            for letters in memory_tag:
                #print(p.replace("?", letters))
                wildcard_plates.append(p.replace("?", letters, 1))
        # BD?1AAA
        elif indices[1] == 2:
            for number in third_number:
                wildcard_plates.append(p.replace("?", number, 1))
        elif indices[1] == 3:
            if p[2] == "0":
                for number in range(2, 10):
                    wildcard_plates.append(p.replace("?", str(number), 1))
            elif p[2] == "2" or p[2] == "7":
                for number in range(1, 4): #Until February 2024
                    wildcard_plates.append(p.replace("?", str(number), 1))
            else:
                for number in list(string.digits): #could have done a set, but would be overkill
                    wildcard_plates.append(p.replace("?", number, 1))
        else:
            for letter in random_letter:
                wildcard_plates.append(p.replace("?", letter, 1))
# ---------------------------------------------------------------------------------------------
def three_wildcards():
    for p in wildcard_plates:
        if indices[2] < 2:
            for letters in memory_tag:
                #print(p.replace("?", letters))
                plates.append(p.replace("?", letters, 1))
        elif indices[2] == 2:
            for number in third_number:
                plates.append(p.replace("?", number, 1))
        elif indices[2] == 3:
            if p[2] == "0":
                for number in range(2, 10):
                    plates.append(p.replace("?", str(number), 1))
            elif p[2] == "2" or p[2] == "7":
                for number in range(1, 4): #Until February 2024
                    plates.append(p.replace("?", str(number), 1))
            else:
                for number in list(string.digits): #could have done a set, but would be overkill
                    plates.append(p.replace("?", number, 1))
        else:
            for letter in random_letter:
                plates.append(p.replace("?", letter, 1))        
# ---------------------------------------------------------------------------------------------
def api_request(reg_num):
    # Actual Environment
    #url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    # Test Environment
    url = 'https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    payload = "{\n\t\"registrationNumber\": \"%(reg)s\"\n}" % {'reg': reg_num} # String interpolation with %
    headers = {
    'x-api-key': args.api, #using the argument for --api
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    #Using print(response.text.encode('utf8')) outputs lines with b' which then needs .decode("utf-8") to fix
    print(response.text)
    #time.sleep(2) # 2 second time out to prevent flooding
# ---------------------------------------------------------------------------------------------
# Not Needed - felt like it would make the output clean
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt Error Caught')
    sys.exit(0)

def main():
    global plates
    signal.signal(signal.SIGINT, sigint_handler)
    if wildcard == 1:
        one_wildcard()
        plates = wildcards_plates
    elif wildcard == 2:
        one_wildcard()
        two_wildcards()
        plates = wildcard_plates
    else:
        one_wildcard()
        two_wildcards()
        three_wildcards()
        #plates = * not needed, as we are writing to plates variable directly
    # Check if API key is provided here
    if args.api is not None:
        for plate in plates:
            api_request(plate)
    else:
        for plate in plates:
            print(plate)

if __name__ == "__main__":
    main()