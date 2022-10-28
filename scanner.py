import cv2
import pytesseract
from urllib.request import urlopen
import json


__author__ = "Nils van Witzenburg 500849196"
__version__ = 2


def start_up():
    """ 
    Prints necessary information to user 
    """
    print("|--------------------------------------------------------|")
    print("| Scan your Image or Text with this simple Python script |")
    print("| How to use the Image Function:                         |")
    print("| Path Example: C:\\Users\\NilsP\Desktop\\tekst.png         |")
    print("| Or 'tekst.png' if script in same directory             |")
    print("|--------------------------------------------------------|")

def text():
    """ 
    Checks if input contains word(s) from 'Blacklist.txt'
    Checks if input contains punctuation
    """
    foundFlags = []
    blockedPun = ['-']
    flag = 0
    text = input("Text: ")

    # Check if any of the blacklisted domains are in found text
    with open('blacklist.txt') as f:
            for line in f:
                    blacklistDomains = line.strip()
                    if text in blacklistDomains:
                            flag = 1
                            break       

    # Check if blockedPun is in Domain
    for i in text:
            for j in blockedPun:
                    if j in i:
                            flag = 1
                            break

    # Add found flag to list
    if flag == 1:
            foundMessage = f'WARNING: Potentially dangerous domain found > {text}'
            foundFlags.append(foundMessage)
    if flag == 0:
            print("Probably no Misspelled or Fraudulent Domain \u2713\n")

    # If flag found, print them        
    if len(foundFlags) >= 1:
            print(f"Found:\n{foundFlags}")
        
def image():
    """
    Scans all text of image
    Checks if image contains word(s) from 'Blacklist.txt'
    Checks if image contains punctuation (Email domain)
    Checks if image conrains a link 
    """
    # Location where Tesseract is installed (Required on Windows)
    # Example: r'C:\Users\NilsP\AppData\Local\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = ''

    foundFlags = []
    foundSpam = []

    blockedPun = ['-']
    urlFound = ['https', 'http']
    flag = 0
    flagUrl = 0
       

    # Scan image for text
    path = input("Path Image: ")
    img = cv2.imread(path)
    # Store all found text in 'text'
    text = pytesseract.image_to_string(img)
    # Only check text after @
    emailFound = text.split('@')[1]
    emailSplit = emailFound.split('.')[0]
        
    # Check if any of the blacklisted words are in found text
    with open('blacklist.txt') as f:
            for line in f:
                    blacklistDomains = line.strip()
                    for i in text:
                        for j in blacklistDomains:
                            if j in text:
                                flag = 1
                                break 

    # Check if blockedPun is in Domain
    for i in emailSplit:
            for j in blockedPun:
                    if j in i:
                            flag = 1
                            break

    # Check for links in the email
    for i in text:
            for j in urlFound:
                    if j in text:
                            flagUrl = 1
                            break

    # If flag or flagUrl found == 1 otherwise 0 
    if flag == 1:
            foundMessage = f"WARNING: Potentially dangerous domain found"
            foundFlags.append(foundMessage)      
    if flag == 0:
            print("Probably no Misspelled or Fraudulent Domain \u2713\n")

    if flagUrl == 1:
            warning = f"WARNING: Potentially dangerous link found"
            foundFlags.append(warning)

            # Remove any whitespace from text                               
            foundText = ("".join(text.split()))

            # Save url found without the https://
            allText = foundText.split("https://")[1]
            fullUrl = allText.split(' ')[0]

            # API key
            key = "GcN2FFKF1OtVJyl55l7quA3ZJSbSzdnW"
                
            # Do a JSON request and save found data
            request = f"https://ipqualityscore.com/api/json/url/GcN2FFKF1OtVJyl55l7quA3ZJSbSzdnW/{fullUrl}"
            response = urlopen(request)
            data_json = json.loads(response.read())
            spam = str(data_json['spamming'])
            malware = str(data_json['malware'])
            phishing = str(data_json['phishing'])
            foundSpam.append("Found Spam: " + spam)
            foundSpam.append("Found Malware: " + malware)
            foundSpam.append("Found Phishing " + phishing)
    if flagUrl == 0:
            print("No URL's found")

    # If flag found, print them
    if len(foundFlags) >= 1:
            print(f"Found:\n{foundFlags}")
                
    if len(foundSpam) >= 1:
            print(f"Checks:\n{foundSpam}")

    print("Do you want to see all found text of image? (Y/n)")
    answer = input()
    if answer == 'Y'.lower():
            print(f"**START**\n{text}\n**END**")


def option():
    """
    Asks user to scan text or image
    """
    print("Want to scan image or text? (I/t)")
    answer = input()
    if answer == 'I'.lower():
        image()
    if answer == 'T'.lower():
        text()
     
def main():
    """
    Start program with the necessary functions
    Provides user with extra information
    Asks user to run program again
    """
    start_up()
    option()

    print("\033[1m" + "PLEASE NOTE"+
    "\n- Double check the content of the email" +
    "\n- Don't click any links unless you trust the source" +
    "\n- Double check the email address" + 
    "\n- Script can false flag" + "\033[0m")

    print("Do you want to run the script again? (Y/n)")
    answer = input()
    if answer == 'Y'.lower():
        main()

if __name__ == '__main__':
    main()


