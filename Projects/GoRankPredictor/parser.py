# this library allows to save the parsered data
import csv

# This library allows to parse through strings using pattern
# recongition
import re

#This library deals with copy/paste system clipboard
import pyperclip

# using this library to create pause time for clipboard parser
import time


ocrData = {
    'winHi': [],
    'winLo':[],
    'lostHi':[],
    'lostLo':[],
    'rank':[]
}


def parseData(text):
    # r' means raw string
    # (\d+) represents an integer
    # the reset is what is possibily in front of the int
    winLostPattern = r'(上位プレーヤーに対する勝ち|上位プレーヤーに対する負け|下位プレーヤーに対する勝ち|下位プレーヤーに対する負け)(\d+)'

    # \d means int
    # +段 means an in followed by 段(dan)
    # then there is an | meaning that the number could be 
    # followed by a 段 or 級
    rankPattern = r'\[(\d+段|\d+級)\]'  # Matches [number段] or [number級]


    # extracts win/lost stat and appends ocrData map
    Match = re.findall(winLostPattern, text)
    # outcome = match[0]
    # value = match[1]

    for match in Match:
        if "上位プレーヤーに対する勝ち" in match[0]:
            ocrData['winHi'].append(int(match[1]))
        elif "上位プレーヤーに対する負け" in match[0]:
            ocrData['lostHi'].append(int(match[1]))
        elif "下位プレーヤーに対する勝ち" in match[0]:
            ocrData['winLo'].append(int(match[1]))
        elif "下位プレーヤーに対する負け" in match[0]:
            ocrData['lostLo'].append(int(match[1]))
        
    rankMatch = re.findall(rankPattern, text)
    if rankMatch:
        rankValue = int(rankMatch[0][0])
        if rankMatch[0][1] == '級':
            ocrData['rank'].append(- (rankValue))
        elif rankMatch[0][1] == '段':
            ocrData['rank'].append(rankValue)

def checkClipBoard():
    previousText = ""
    while True:

        # gets the content in the clipboard
        currentText = pyperclip.paste()

        if currentText != previousText:
            previousText = currentText

            # parse the text in the clipboard
            parseData(currentText)

            print("Updated OCR Data", ocrData)

            saveData()

        # makes the loop pause to decrease lag
        time.sleep(1)

def saveData():

    dataLength = min(len(ocrData['winHi']), len(ocrData['lostHi']), len(ocrData['winLo']), len(ocrData['lostLo']))

    # creates/opens parsedData.csv file and starts appending data
    # file is an object from csv
    with open('parsedData.csv', mode = 'a', newline='') as file:
        writer = csv.writer(file)
        # loops through each item in the 'winHi' list
        for i in range(dataLength):
            #writes the elements in each of the list to the csv file
            writer.writerow([
                ocrData['winHi'][i],
                ocrData['lostHi'][i],
                ocrData['winLo'][i],
                ocrData['lostLo'][i]
            ])

# checks if script is being run in itself
if __name__ == "__main__":
    checkClipBoard()

