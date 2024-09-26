#This program scraps all of the rankings of each character in a tier list
#The program prompts the user to pick which game they want the tier list of
# The user then inputs the character they want to know the rank of and the rank 
# is printed on the terminal

#This library lets you get asscess to a website's information
import requests 
#This library lets you scrap information from a website
from bs4 import BeautifulSoup as bs

url = "https://www.prydwen.gg"
check = False

#asks for which game you want to look at and convert the string into an integer
game = int(input("Pick a game. 1 for Nikke. 2 for Reverse 1999:"))

#asks for which character's ranking you want 
character = input("Give me a character:")

#This function checks if the website you are using allows you to scrap data
# This function takes the url and a boolean check variable

def canScrap(url, check):

    #This varible holds the url + /robots.txt which is a page that tells you if you can scrap their website
    checkUrl = url + "/robots.txt"

    #This makes a variable using the function in the requests library requests 
    # the variable holds all of the text on the page
    verification = requests.get(checkUrl)

    # this translates the text on the respective website's robot.txt page into html status code
    status = verification.status_code

    #This checks for 200 because 200 is html status code for successful access
    if status == 200:
        check = True
        print(str(check))

        #returns the robots text and bool value of check
        return verification.text, check
    
    else:
        return "No access " + str(status)
    

#intializes result with the robots text and check with the returned bool check value
result, check = canScrap(url, check)
print(result)

#changes url to specific tier list page on the website


#creates a dictionary kinda like a list 
url = {
    1: "https://www.prydwen.gg/nikke/tier-list",
    2: "https://www.prydwen.gg/re1999/tier-list/",
}

#this uses the bool check to see if the website allows scrap before continuing with scrapping

if check:
    #this function returns the tier of a character inputted 
    #this function takes a string of a url and character name
    def getRank(url, character):

        #scrap is an object that goes through the website using the requests library
        scrap = requests.get(url)

        #if scrap is success then continue. 200 is success in html status code
        if scrap.status_code == 200:

            #this makes a parser object using the BeautifulSoop library
            parser = bs(scrap.content, 'html.parser')

            #makes an array that stores all tier categories from the html
            allTiers = parser.find_all('div', class_='custom-tier')
            
            #run a for loop checking each individual letter tier
            for letter in allTiers:
                
                #makes an array that stores all of the letters
                rank = letter.find('span').text.strip()

                #makes an array that stores all of the character cards in each tier section
                characterCards = letter.find_all('div', class_='avatar-card')

                #for loop that goes through each individual card in the characterCards
                for card in characterCards:
                    
                    #extracts all of the names from the current card it is indexing and puts them into an array call characterNameTag
                    characterNameTag = card.find_all('span', class_='emp-name')


                #if the characterName extracted and its text stripped of white text matches the inputted character name continue
                # characterNameTag[0] is needed on the second condition because characterNameTag is a list so the computer doesn't 
                # know which index in the list it should be comparing with 
                # [0] will be the first and potientially the only character tag in the list which is the one we need in the case
                    if characterNameTag and characterNameTag[0].text.strip() == character:

                    #If this Character Card return the rank found 
                        return rank
            
                    
            return "Character does not exist or mistyped"
            
        else:
            return "Failed to scrap website"
        
else:
    print("Website does not allow scrapping")

#the .get(game) in url.get(game) gets the respective url in the url dictionary to pass to the getRank function
print(getRank(url.get(game), character))
