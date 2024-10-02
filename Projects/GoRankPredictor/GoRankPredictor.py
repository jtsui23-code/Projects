#This program will predict the rank of the Go player when given their win/lost ratio
# against higher and lower rank players

#numpy is a library used for effectivly dealing with arrays
import numpy as np 

#panda is used for data analysis 
import pandas as pd

# sk is a machine learning library
# train_test_split is specifically being used from the sk library 
# to split the data for training and testing
# if there was no split then the program could not improve at 
# making predictions of player ranks
from sklearn.model_selection import train_test_split

# this imports a model for making the prediction
# the difference between DecisionTreeRegressor and DecisionTreeClassifier is
# Regressor deals with numbers and decimals/continuous data
# classifier deals with categories int/discrete data
from sklearn.tree import DecisionTreeClassifier

# this library is for determining how good the predicitons are
# there is another library called Mean Squared Error which is used with 
# regressor or continuous data
from sklearn.metrics import accuracy_score

# set number of synthetic data
numSyntheticData = 1000
# creates range of [-25, -1] U [1, 9]
rankRange = list(range(-25, 0)) + list(range(1, 10))

data ={
# here are individual lists 
'winHi': [6, 3, 235, 97, 587,55, 114, 375, 421, 34,
           28, 162, 134, 1,31, 175,274,3, 562, 160,
            10, 372, 291, 16, 23, 1, 150, 139, 880,
            899,788, 3, 18,0, 138, 22, 71, 38,
            11, 521, 35, 6, 794, 101, 68, 409, 5,68, 
            864, 17, 109,18, 15,1125, 901, 1125,428,
            339,699,63,193,465,6,117,12,22,19,31,7,58,
            80,32,587,547,270,126,346,26,1,6,15,42,
            864,4,632,2,12,1059,156,56,71,15,187,426,
            741,290,381,14,8,335,41,823,182,218,],

'lostHi':[3, 5, 468, 158, 1158, 155, 273, 1411, 707,
          136, 42, 314, 228, 17, 42, 385,593,8, 988, 265,
          32, 952, 620, 35, 44, 3, 321, 304, 2070,
          1688, 1333, 7, 43, 3, 314, 23, 188, 62,
          19, 1007, 47, 21, 1363, 347, 127, 932, 9, 127,
          1956, 56, 236, 18, 44,1730, 1502,1730, 699,
          637,1424,131,486,826,14,184,51,47,40,46,33,93,
          127,58,1182,1053,421,111,539,60,6,13,5, 107,
          1956,21,1877,16,39,1821,265,116,130,23,356,
          828,1525,714,939,37,31,236,154,1798,582,521,
          ],

'winLo':[117, 130, 799, 354, 2250,234, 501, 23, 2403,
         26, 26, 208, 196, 6, 50, 324,495,68, 1142, 1776,
          52, 2345, 945, 104, 25, 12, 414, 193, 425,
          1566, 1147, 20, 55, 121, 170, 123, 148, 67,
           24, 891, 60, 28,1148, 168, 123,1132, 9, 123,
           884, 65, 4271,57, 115,1358, 1618, 1358, 2730,
           2485,1979,116,361,726,14,120,37,48,8,46,98,113,
           78,69,523,2444,3416,1918,3091,169,53,58,31,
           160,884,20,982,11,20,1381,134,145,247,373,
           249,356,1863,253,612,80,157,3797,659,1631,
           252,172,],

'lostLo':[12, 10, 438, 185, 1005,87, 187, 3, 1094,
          21, 6, 97, 89, 3, 16, 107, 211,49, 617, 635,
          10, 1331, 472, 16, 5, 1, 198, 82, 225,
          847, 623, 8, 17, 9, 63, 12, 60, 37, 10, 410,
          20, 11, 603, 55, 45, 353, 0, 45, 369, 20, 384,
            15, 31, 787, 979, 787,1143, 723,898, 59,123,
            381,6,55,11,22,4,22,47,45,28,11,223,956,893,
            387,1024,58,16,19,2,52,369,4,343,1,7,739,
            88,35,101,101,110,167,871,106,298,18,25,632,123,
            748,101,79,],

# to differienciate dan and kyu 
# dan is positive so 7 dan = 7
# kyu is represented as a negative number so 
# a 25 kyu is typed as -25

'rank': [7 ,7, -2, -3, -6, -2, -4, -10, -3,-25, -17,
         -18, -23, -19, -19, -16, -14,-11, -6, 5, 4,
         -1, -3, 3, 2, 4, 3, -13, -15, -13, -7, 2, 4,
         8, 8, 4, -16, -5, -6, -8, -21, -23, -19, -14,
         -15,-12,-20, -15,-14, -7, 6,3, 2, -3,-10, -3,
         -4, -5,-8, -13,-14,-13,-19,-17,-22,-25,-25,-25,
         -22,-23,-16,-17,-13,-4,-3,3,2,4,6,5,9,4,-14,-23,
         -16,-15,-16,-15,-19,-23,-1,2, -4,-6,-5,-8,-7,
         4,5,4,-2,-11,-13,-18,]
}

# this function recieves an int as the rank of the player
# and returns a synthetic win/lost ratio according to the
# player rank

def generateSynthetic(rank):
    if rank > 0:
        winHi = np.random.randint(5, 300)
        winLo = np.random.randint(100, 1000)
        losHi = np.random.randint(1, 100)
        losLo = np.random.randint(1, 50)
    else:
        winHi = np.random.randint(1, 100)
        winLo = np.random.randint(5, 300)
        losHi = np.random.randint(100, 1000)
        losLo = np.random.randint(1, 100)
    

    return winHi, winLo, losHi, losLo

# generates synthetic data 
#for i in range(numSyntheticData):
    rank = np.random.choice(rankRange)

    winHi, winLo, losHi, losLo = generateSynthetic(rank)

    data['winHi'].append(winHi)
    data['winLo'].append(winLo)
    data['lostHi'].append(losHi)
    data['lostLo'].append(losLo)
    data['rank'].append(rank)

# converts data map of player ranks and win/lost ratio
# to panda dataframe
dataFrame = pd.DataFrame(data)

# creating dependent and independent varaible for graph
x = dataFrame[['winHi', 'lostHi', 'winLo', 'lostLo']]
y = dataFrame['rank']

# test_size is how much of the data will be left over for testing 
# the performance of the program so in this case 0.2 means
# 20% of the data is for testing and 80% is for training
# random_test is a seed for this exact split which is useful 
# for debugging problems
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)

# creates model using the specific split seed 42
model = DecisionTreeClassifier(random_state=42)

# trains the model
model.fit(xTrain, yTrain)

# predicts the go player's rank according to test data on win/lost
predictedRank = model.predict(xTest)

# computes the accuracy of the prediction through
# comparison with the actual go player's rank
accuracy = accuracy_score(yTest, predictedRank)

print(len(data['winHi']))
print(len(data['lostHi']))
print(len(data['winLo']))
print(len(data['lostLo']))
print(len(data['rank']))