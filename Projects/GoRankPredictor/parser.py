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
    # \d+ means any of these digits 0-9
    # ^\d+ means this is not a number in (^\d+)
    # so ([^\d+]) is the string or stuff infront of the win/lost 
    # integer
    winLostPattern = r'([^\d+])(\d+)'

    # (\w+) means any letter so for recongizing the name of player
    # \s* recongize any white spaces between string/int

    # \d means int
    # +段 means an in followed by 段(dan)
    # then there is an | meaning that the number could be 
    # followed by a 段 or 級
    rankPattern = r'(\w+)\s*\[([\d]+段|[\d]+級)\]'

    # extracts win/lost stat and appends ocrData map
    Match = re.findall(winLostPattern, text)
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
        if '級' in rankMatch[0][1]:
            ocrData['rank'].append(- (rankValue))
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

        # makes the loop pause to decrease lag
        time.sleep(1)

# checks if script is being run in itself
if __name__ == "__main__":
    checkClipBoard()

